from flask import request, jsonify
from flask_jwt_extended import jwt_required
from . import api_bp
from ..knowledge_graph import KnowledgeGraphManager

kg_manager = KnowledgeGraphManager()


@api_bp.route('/knowledge_graph/all_courses', methods=['GET'])
@jwt_required()
def get_all_courses_graph():
    """获取全部课程节点及先修关系，用于全图渲染"""
    query = """
    MATCH (c:Course)
    OPTIONAL MATCH (c)-[r:PREREQUISITE_OF]->(c2:Course)
    RETURN
        c.course_code   AS code,
        c.course_name   AS name,
        c.credit        AS credit,
        c.course_type   AS course_type,
        c.department    AS department,
        c.description   AS description,
        c.prerequisite  AS prerequisite,
        c2.course_code  AS to_code
    """
    records = kg_manager.neo4j.run_query(query)
    if records is None:
        return jsonify({"error": "Neo4j 查询失败"}), 500

    nodes_map = {}
    edges = []
    seen_edges = set()

    for rec in records:
        code = rec["code"]
        if code and code not in nodes_map:
            nodes_map[code] = {
                "id": code,
                "label": rec["name"] or code,
                "credit": rec["credit"],
                "course_type": rec["course_type"],
                "department": rec["department"],
                "description": rec["description"],
                "prerequisite": rec["prerequisite"],
                "node_type": "Course"
            }
        to_code = rec["to_code"]
        if to_code:
            edge_key = f"{code}->{to_code}"
            if edge_key not in seen_edges:
                seen_edges.add(edge_key)
                edges.append({"from": code, "to": to_code, "relation": "PREREQUISITE_OF"})

    return jsonify({"nodes": list(nodes_map.values()), "edges": edges}), 200


@api_bp.route('/knowledge_graph/expand/<string:course_code>', methods=['GET'])
@jwt_required()
def expand_course_node(course_code):
    """展开课程节点，返回其知识点和技能子节点"""
    query = """
    MATCH (c:Course {course_code: $code})
    OPTIONAL MATCH (c)-[:CONTAINS]->(k:KnowledgePoint)
    OPTIONAL MATCH (c)-[:BUILDS]->(s:Skill)
    RETURN
        c.course_code AS code,
        k.id          AS kp_id,
        k.name        AS kp_name,
        k.content     AS kp_content,
        k.difficulty  AS kp_difficulty,
        s.id          AS skill_id,
        s.name        AS skill_name,
        s.description AS skill_desc
    """
    records = kg_manager.neo4j.run_query(query, {"code": course_code})
    if records is None:
        return jsonify({"error": "Neo4j 查询失败"}), 500

    kp_nodes = {}
    skill_nodes = {}
    edges = []

    for rec in records:
        kp_id = rec["kp_id"]
        if kp_id and kp_id not in kp_nodes:
            node_id = f"kp_{kp_id}"
            kp_nodes[kp_id] = {
                "id": node_id,
                "label": rec["kp_name"] or f"知识点{kp_id}",
                "content": rec["kp_content"],
                "difficulty": rec["kp_difficulty"],
                "node_type": "KnowledgePoint"
            }
            edges.append({"from": course_code, "to": node_id, "relation": "CONTAINS"})

        skill_id = rec["skill_id"]
        if skill_id and skill_id not in skill_nodes:
            node_id = f"skill_{skill_id}"
            skill_nodes[skill_id] = {
                "id": node_id,
                "label": rec["skill_name"] or f"技能{skill_id}",
                "description": rec["skill_desc"],
                "node_type": "Skill"
            }
            edges.append({"from": course_code, "to": node_id, "relation": "BUILDS"})

    return jsonify({
        "nodes": list(kp_nodes.values()) + list(skill_nodes.values()),
        "edges": edges
    }), 200

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