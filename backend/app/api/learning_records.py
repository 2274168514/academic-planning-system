from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import api_bp
from ..models import LearningRecord, Course
from .. import db
from datetime import datetime

@api_bp.route('/learning_records', methods=['GET'])
@jwt_required()
def get_learning_records():
    """获取用户的所有学习记录"""
    user_id = get_jwt_identity()
    
    # 筛选条件
    status = request.args.get('status')
    course_id = request.args.get('course_id')
    
    query = LearningRecord.query.filter_by(user_id=user_id)
    
    if status:
        query = query.filter_by(status=status)
    
    if course_id:
        query = query.filter_by(course_id=course_id)
    
    records = query.order_by(LearningRecord.start_time.desc()).all()
    
    return jsonify({
        "records": [record.to_dict() for record in records]
    }), 200


@api_bp.route('/learning_records/<int:record_id>', methods=['GET'])
@jwt_required()
def get_learning_record(record_id):
    """获取指定学习记录详情"""
    user_id = get_jwt_identity()
    
    record = LearningRecord.query.filter_by(record_id=record_id, user_id=user_id).first()
    
    if not record:
        return jsonify({"error": "学习记录不存在"}), 404
    
    return jsonify({
        "record": record.to_dict()
    }), 200


@api_bp.route('/learning_records', methods=['POST'])
@jwt_required()
def create_learning_record():
    """创建新的学习记录"""
    user_id = get_jwt_identity()
    data = request.json
    
    # 验证必要字段
    if 'course_id' not in data:
        return jsonify({"error": "缺少课程ID"}), 400
    
    # 验证课程存在
    course = Course.query.get(data['course_id'])
    if not course:
        return jsonify({"error": "课程不存在"}), 404
    
    # 检查是否已有进行中的记录
    existing = LearningRecord.query.filter_by(
        user_id=user_id,
        course_id=data['course_id'],
        status='in_progress'
    ).first()
    
    if existing:
        return jsonify({
            "error": "已有进行中的学习记录",
            "record": existing.to_dict()
        }), 409
    
    # 创建记录
    record = LearningRecord(
        user_id=user_id,
        course_id=data['course_id'],
        notes=data.get('notes')
    )
    
    if 'start_time' in data:
        try:
            record.start_time = datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            pass
    
    db.session.add(record)
    db.session.commit()
    
    return jsonify({
        "message": "学习记录创建成功",
        "record": record.to_dict()
    }), 201


@api_bp.route('/learning_records/<int:record_id>', methods=['PUT'])
@jwt_required()
def update_learning_record(record_id):
    """更新学习记录"""
    user_id = get_jwt_identity()
    data = request.json
    
    record = LearningRecord.query.filter_by(record_id=record_id, user_id=user_id).first()
    
    if not record:
        return jsonify({"error": "学习记录不存在"}), 404
    
    # 更新字段
    if 'notes' in data:
        record.notes = data['notes']
    
    if 'status' in data and data['status'] == 'completed' and record.status != 'completed':
        record.status = 'completed'
        record.finish_time = datetime.now()
        
        if 'score' in data:
            try:
                record.score = float(data['score'])
            except (ValueError, TypeError):
                pass
    
    db.session.commit()
    
    return jsonify({
        "message": "学习记录更新成功",
        "record": record.to_dict()
    }), 200


@api_bp.route('/learning_records/<int:record_id>', methods=['DELETE'])
@jwt_required()
def delete_learning_record(record_id):
    """删除学习记录"""
    user_id = get_jwt_identity()
    
    record = LearningRecord.query.filter_by(record_id=record_id, user_id=user_id).first()
    
    if not record:
        return jsonify({"error": "学习记录不存在"}), 404
    
    db.session.delete(record)
    db.session.commit()
    
    return jsonify({
        "message": "学习记录删除成功"
    }), 200


@api_bp.route('/learning_records/<int:record_id>/complete', methods=['POST'])
@jwt_required()
def complete_learning_record(record_id):
    """完成学习记录"""
    user_id = get_jwt_identity()
    data = request.json
    
    record = LearningRecord.query.filter_by(record_id=record_id, user_id=user_id).first()
    
    if not record:
        return jsonify({"error": "学习记录不存在"}), 404
    
    if record.status == 'completed':
        return jsonify({"error": "学习记录已完成"}), 400
    
    # 完成学习
    score = data.get('score')
    if score is not None:
        try:
            score = float(score)
        except (ValueError, TypeError):
            score = None
    
    record.complete(score)
    
    return jsonify({
        "message": "学习记录已标记为完成",
        "record": record.to_dict()
    }), 200


@api_bp.route('/learning_progress', methods=['GET'])
@jwt_required()
def get_learning_progress():
    """获取用户的学习进度统计"""
    user_id = get_jwt_identity()
    
    progress = LearningRecord.get_user_progress(user_id)
    
    return jsonify({
        "progress": progress
    }), 200 