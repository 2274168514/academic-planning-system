from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import api_bp
from ..models import User
import logging
import json

def get_ai_service():
    from ..services import AIService
    return AIService()

def get_recommendation_service():
    from ..services.recommendation_service import RecommendationService
    return RecommendationService()

@api_bp.route('/ai/status', methods=['GET'])
def check_ai_status():
    """检查AI助手服务状态"""
    try:
        # 检查各种配置
        api_key = current_app.config.get('DEEPSEEK_API_KEY')
        api_url = current_app.config.get('DEEPSEEK_API_URL')
        model_name = current_app.config.get('DEEPSEEK_MODEL')
        
        config_status = {
            "api_key": bool(api_key),
            "api_url": bool(api_url),
            "model_name": bool(model_name)
        }
        
        # 记录配置检查结果
        logging.info(f"AI状态检查 - 配置状态: {json.dumps(config_status)}")
        
        if not api_key:
            return jsonify({
                "status": "error",
                "message": "DeepSeek API密钥未配置",
                "config_status": config_status,
                "action_required": "请配置DEEPSEEK_API_KEY环境变量"
            }), 500
            
        # 检查API密钥格式
        if not api_key.startswith('sk-'):
            return jsonify({
                "status": "warning",
                "message": "DeepSeek API密钥格式可能不正确，正确的格式应以'sk-'开头",
                "config_status": config_status,
                "action_required": "请检查DEEPSEEK_API_KEY格式"
            }), 200
            
        # 测试API连接
        ai_service = get_ai_service()
        test_result = ai_service.test_connection()
        
        logging.info(f"AI状态检查 - 测试结果: {json.dumps(test_result)}")
        
        if test_result['status'] == 'error':
            return jsonify({
                "status": "error",
                "message": test_result['message'],
                "details": test_result.get('details', ''),
                "config_status": config_status,
                "action_required": "请检查网络连接和API配置"
            }), 500
            
        # 一切正常
        return jsonify({
            "status": "ok",
            "message": "AI助手服务配置正常",
            "api_url": api_url,
            "model": model_name,
            "test_result": test_result['message'],
            "config_status": config_status
        })
    except Exception as e:
        logging.error(f"检查AI状态时出错: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"检查服务状态时出错: {str(e)}"
        }), 500

@api_bp.route('/ai/chat', methods=['POST'])
@jwt_required()
def chat():
    """AI聊天接口"""
    user_id = get_jwt_identity()
    data = request.json
    
    if 'message' not in data:
        return jsonify({"error": "缺少消息内容"}), 400
    
    user_message = data['message']
    chat_history = data.get('chat_history', [])
    
    try:
        # 调用AI服务
        response = get_ai_service().academic_planning_chat(user_message, chat_history)
        
        return jsonify({
            "response": response
        }), 200
    except Exception as e:
        logging.error(f"AI聊天处理错误: {str(e)}")
        return jsonify({
            "error": f"处理请求时出错: {str(e)}"
        }), 500


@api_bp.route('/ai/study_plan', methods=['POST'])
@jwt_required()
def generate_study_plan():
    """生成学习计划"""
    user_id = get_jwt_identity()
    data = request.json
    
    # 获取用户信息
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "用户不存在"}), 404
    
    # 获取请求参数
    major = data.get('major') or user.major
    if not major:
        return jsonify({"error": "缺少专业信息"}), 400
        
    interests = data.get('interests', '')
    career_goals = data.get('career_goals', '')
    current_semester = data.get('current_semester', 1)
    
    # 调用AI服务生成计划
    plan = get_ai_service().generate_study_plan(major, interests, career_goals, current_semester)
    
    return jsonify(plan), 200


@api_bp.route('/ai/recommend_courses', methods=['GET'])
@jwt_required()
def recommend_courses():
    """推荐课程"""
    user_id = get_jwt_identity()
    limit = request.args.get('limit', 10, type=int)
    
    # 调用推荐服务
    recommendations = get_recommendation_service().recommend_courses(user_id, limit)
    
    return jsonify({
        "recommendations": recommendations
    }), 200


@api_bp.route('/ai/recommend_next_courses', methods=['GET'])
@jwt_required()
def recommend_next_courses():
    """基于已完成课程推荐后续课程"""
    user_id = get_jwt_identity()
    limit = request.args.get('limit', 5, type=int)
    
    # 调用推荐服务
    recommendations = get_recommendation_service().recommend_based_on_completed(user_id, limit)
    
    return jsonify({
        "recommendations": recommendations
    }), 200


@api_bp.route('/ai/recommend_study_plan', methods=['GET'])
@jwt_required()
def recommend_study_plan():
    """推荐学习计划"""
    user_id = get_jwt_identity()
    semester_count = request.args.get('semester_count', 8, type=int)
    
    # 调用推荐服务
    plan = get_recommendation_service().recommend_study_plan(user_id, semester_count)
    
    return jsonify(plan), 200 