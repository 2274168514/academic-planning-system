from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import api_bp
from ..models import StudyPlan, PlanDetail, Course
from .. import db

@api_bp.route('/study_plans', methods=['GET'])
@jwt_required()
def get_study_plans():
    """获取用户的所有学习计划"""
    user_id = get_jwt_identity()
    
    plans = StudyPlan.query.filter_by(user_id=user_id).order_by(StudyPlan.update_time.desc()).all()
    
    return jsonify({
        "plans": [plan.to_dict() for plan in plans]
    }), 200


@api_bp.route('/study_plans/<int:plan_id>', methods=['GET'])
@jwt_required()
def get_study_plan(plan_id):
    """获取指定学习计划详情"""
    user_id = get_jwt_identity()
    
    plan = StudyPlan.query.filter_by(plan_id=plan_id, user_id=user_id).first()
    
    if not plan:
        return jsonify({"error": "学习计划不存在"}), 404
    
    return jsonify({
        "plan": plan.to_dict_with_details()
    }), 200


@api_bp.route('/study_plans', methods=['POST'])
@jwt_required()
def create_study_plan():
    """创建新的学习计划"""
    user_id = get_jwt_identity()
    data = request.json
    
    # 验证必要字段
    if 'plan_name' not in data:
        return jsonify({"error": "缺少计划名称"}), 400
    
    # 创建计划
    plan = StudyPlan(
        user_id=user_id,
        plan_name=data['plan_name'],
        description=data.get('description')
    )
    
    db.session.add(plan)
    db.session.commit()
    
    # 如果提供了课程，添加到计划中
    if 'courses' in data and isinstance(data['courses'], list):
        for course_data in data['courses']:
            if not all(k in course_data for k in ('course_id', 'semester')):
                continue
            
            # 验证课程存在
            course = Course.query.get(course_data['course_id'])
            if not course:
                continue
            
            detail = PlanDetail(
                plan_id=plan.plan_id,
                course_id=course_data['course_id'],
                semester=course_data['semester'],
                priority=course_data.get('priority', 0),
                status=course_data.get('status', 'pending')
            )
            
            db.session.add(detail)
        
        db.session.commit()
    
    return jsonify({
        "message": "学习计划创建成功",
        "plan": plan.to_dict_with_details()
    }), 201


@api_bp.route('/study_plans/<int:plan_id>', methods=['PUT'])
@jwt_required()
def update_study_plan(plan_id):
    """更新学习计划"""
    user_id = get_jwt_identity()
    data = request.json
    
    plan = StudyPlan.query.filter_by(plan_id=plan_id, user_id=user_id).first()
    
    if not plan:
        return jsonify({"error": "学习计划不存在"}), 404
    
    # 更新基本信息
    if 'plan_name' in data:
        plan.plan_name = data['plan_name']
    
    if 'description' in data:
        plan.description = data['description']
    
    if 'plan_status' in data:
        plan.plan_status = data['plan_status']
    
    db.session.commit()
    
    return jsonify({
        "message": "学习计划更新成功",
        "plan": plan.to_dict()
    }), 200


@api_bp.route('/study_plans/<int:plan_id>', methods=['DELETE'])
@jwt_required()
def delete_study_plan(plan_id):
    """删除学习计划"""
    user_id = get_jwt_identity()
    
    plan = StudyPlan.query.filter_by(plan_id=plan_id, user_id=user_id).first()
    
    if not plan:
        return jsonify({"error": "学习计划不存在"}), 404
    
    db.session.delete(plan)
    db.session.commit()
    
    return jsonify({
        "message": "学习计划删除成功"
    }), 200


@api_bp.route('/study_plans/<int:plan_id>/details', methods=['POST'])
@jwt_required()
def add_plan_detail(plan_id):
    """向计划添加课程"""
    user_id = get_jwt_identity()
    data = request.json
    
    plan = StudyPlan.query.filter_by(plan_id=plan_id, user_id=user_id).first()
    
    if not plan:
        return jsonify({"error": "学习计划不存在"}), 404
    
    # 验证必要字段
    if not all(k in data for k in ('course_id', 'semester')):
        return jsonify({"error": "缺少必要字段"}), 400
    
    # 验证课程存在
    course = Course.query.get(data['course_id'])
    if not course:
        return jsonify({"error": "课程不存在"}), 404
    
    # 检查是否已添加
    existing = PlanDetail.query.filter_by(
        plan_id=plan_id,
        course_id=data['course_id']
    ).first()
    
    if existing:
        return jsonify({"error": "该课程已在计划中"}), 409
    
    # 添加课程
    detail = PlanDetail(
        plan_id=plan_id,
        course_id=data['course_id'],
        semester=data['semester'],
        priority=data.get('priority', 0),
        status=data.get('status', 'pending')
    )
    
    db.session.add(detail)
    db.session.commit()
    
    return jsonify({
        "message": "课程添加成功",
        "detail": detail.to_dict()
    }), 201


@api_bp.route('/study_plans/<int:plan_id>/details/<int:detail_id>', methods=['PUT'])
@jwt_required()
def update_plan_detail(plan_id, detail_id):
    """更新计划中的课程"""
    user_id = get_jwt_identity()
    data = request.json
    
    # 验证计划存在且属于当前用户
    plan = StudyPlan.query.filter_by(plan_id=plan_id, user_id=user_id).first()
    if not plan:
        return jsonify({"error": "学习计划不存在"}), 404
    
    # 获取计划详情
    detail = PlanDetail.query.filter_by(detail_id=detail_id, plan_id=plan_id).first()
    if not detail:
        return jsonify({"error": "课程不存在于该计划中"}), 404
    
    # 更新字段
    if 'semester' in data:
        detail.semester = data['semester']
    
    if 'priority' in data:
        detail.priority = data['priority']
    
    if 'status' in data:
        detail.status = data['status']
    
    db.session.commit()
    
    return jsonify({
        "message": "课程更新成功",
        "detail": detail.to_dict()
    }), 200


@api_bp.route('/study_plans/<int:plan_id>/details/<int:detail_id>', methods=['DELETE'])
@jwt_required()
def delete_plan_detail(plan_id, detail_id):
    """从计划中删除课程"""
    user_id = get_jwt_identity()
    
    # 验证计划存在且属于当前用户
    plan = StudyPlan.query.filter_by(plan_id=plan_id, user_id=user_id).first()
    if not plan:
        return jsonify({"error": "学习计划不存在"}), 404
    
    # 获取计划详情
    detail = PlanDetail.query.filter_by(detail_id=detail_id, plan_id=plan_id).first()
    if not detail:
        return jsonify({"error": "课程不存在于该计划中"}), 404
    
    db.session.delete(detail)
    db.session.commit()
    
    return jsonify({
        "message": "课程从计划中移除成功"
    }), 200 