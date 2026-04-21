from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import api_bp
from ..models import User
from .. import db

@api_bp.route('/auth/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.json
    
    # 验证必要字段
    if not all(k in data for k in ('username', 'password', 'email')):
        return jsonify({"error": "缺少必要字段"}), 400
    
    # 检查用户名或邮箱是否已存在
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "用户名已存在"}), 409
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "邮箱已存在"}), 409
    
    # 创建新用户
    user = User(
        username=data['username'],
        email=data['email'],
        phone=data.get('phone'),
        major=data.get('major'),
        grade=data.get('grade')
    )
    user.password = data['password']  # 会自动加密
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        "message": "注册成功",
        "user": user.to_dict()
    }), 201


@api_bp.route('/auth/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.json
    
    # 验证必要字段
    if not all(k in data for k in ('username', 'password')):
        return jsonify({"error": "缺少用户名或密码"}), 400
    
    # 查找用户
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return jsonify({"error": "用户不存在"}), 404
    
    # 验证密码
    if not user.verify_password(data['password']):
        return jsonify({"error": "密码错误"}), 401
    
    # 更新登录时间
    user.update_last_login()
    
    # 生成token
    token = user.generate_auth_token()
    
    return jsonify({
        "message": "登录成功",
        "token": token,
        "user": user.to_dict()
    }), 200


@api_bp.route('/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """获取用户资料"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "用户不存在"}), 404
    
    return jsonify({
        "user": user.to_dict()
    }), 200


@api_bp.route('/auth/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """更新用户资料"""
    user_id = get_jwt_identity()
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
        "message": "资料更新成功",
        "user": user.to_dict()
    }), 200 