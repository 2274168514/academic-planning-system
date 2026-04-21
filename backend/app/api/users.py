from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import api_bp
from ..models import User
from .. import db

@api_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """获取指定用户信息"""
    current_user_id = get_jwt_identity()
    
    # 只允许获取自己的信息
    if current_user_id != user_id:
        return jsonify({"error": "无权查看其他用户信息"}), 403
    
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "用户不存在"}), 404
    
    return jsonify({
        "user": user.to_dict()
    }), 200


@api_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """更新用户信息"""
    current_user_id = get_jwt_identity()
    
    # 只允许修改自己的信息
    if current_user_id != user_id:
        return jsonify({"error": "无权修改其他用户信息"}), 403
    
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "用户不存在"}), 404
    
    data = request.json
    
    # 更新可修改的字段
    if 'email' in data and data['email'] != user.email:
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "邮箱已被使用"}), 409
        user.email = data['email']
    
    if 'phone' in data:
        user.phone = data['phone']
    
    if 'major' in data:
        user.major = data['major']
    
    if 'grade' in data:
        user.grade = data['grade']
    
    if 'avatar' in data:
        user.avatar = data['avatar']
    
    # 如果要修改密码，需要验证旧密码
    if 'password' in data and 'old_password' in data:
        if not user.verify_password(data['old_password']):
            return jsonify({"error": "旧密码错误"}), 401
        user.password = data['password']
    
    db.session.commit()
    
    return jsonify({
        "message": "用户信息更新成功",
        "user": user.to_dict()
    }), 200


@api_bp.route('/users/change_password', methods=['POST'])
@jwt_required()
def change_password():
    """修改密码"""
    user_id = get_jwt_identity()
    data = request.json
    
    # 验证必要字段
    if not all(k in data for k in ('old_password', 'new_password')):
        return jsonify({"error": "缺少必要字段"}), 400
    
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "用户不存在"}), 404
    
    # 验证旧密码
    if not user.verify_password(data['old_password']):
        return jsonify({"error": "旧密码错误"}), 401
    
    # 设置新密码
    user.password = data['new_password']
    db.session.commit()
    
    return jsonify({
        "message": "密码修改成功"
    }), 200 