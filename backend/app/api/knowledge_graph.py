from flask import request, jsonify
from flask_jwt_extended import jwt_required
from . import api_bp
from ..knowledge_graph import KnowledgeGraphManager

kg_manager = KnowledgeGraphManager()

@api_bp.route('/knowledge_graph/course/<int:course_id>', methods=['GET'])
@jwt_required()
def get_course_knowledge_graph(course_id):
    """获取课程知识图谱"""
    graph = kg_manager.get_course_knowledge_graph(course_id=course_id)
    
    return jsonify(graph), 200


@api_bp.route('/knowledge_graph/course/code/<string:course_code>', methods=['GET'])
@jwt_required()
def get_course_knowledge_graph_by_code(course_code):
    """根据课程代码获取知识图谱"""
    graph = kg_manager.get_course_knowledge_graph(course_code=course_code)
    
    return jsonify(graph), 200


@api_bp.route('/knowledge_graph/career/<string:career_name>', methods=['GET'])
@jwt_required()
def get_career_path(career_name):
    """获取职业路径"""
    graph = kg_manager.get_career_path(career_name)
    
    return jsonify(graph), 200


@api_bp.route('/knowledge_graph/learning_path/<string:major_name>', methods=['GET'])
@jwt_required()
def get_learning_path(major_name):
    """获取专业学习路径"""
    semester_count = request.args.get('semester_count', 8, type=int)
    path = kg_manager.get_learning_path(major_name, semester_count)
    
    return jsonify(path), 200


@api_bp.route('/knowledge_graph/search', methods=['GET'])
@jwt_required()
def search_knowledge_graph():
    """搜索知识图谱"""
    keyword = request.args.get('keyword', '')
    if not keyword:
        return jsonify({"error": "缺少搜索关键词"}), 400
    
    results = kg_manager.search_knowledge_graph(keyword)
    
    return jsonify(results), 200 