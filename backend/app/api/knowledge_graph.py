from flask import request, jsonify
from flask_jwt_extended import jwt_required
from . import api_bp
from ..models import Course

# 静态展开数据（知识点 + 技能），无需 Neo4j
MOCK_EXPAND = {
    'CS101': {
        'nodes': [
            {'id': 'kp_1', 'label': '计算机历史', 'content': '计算机发展历史，从机械计算设备到现代计算机的演变过程。', 'difficulty': 1, 'node_type': 'KnowledgePoint'},
            {'id': 'kp_2', 'label': '计算机硬件基础', 'content': '计算机硬件组成，包括CPU、内存、存储设备和输入输出设备等。', 'difficulty': 1, 'node_type': 'KnowledgePoint'},
            {'id': 'kp_3', 'label': '计算机软件基础', 'content': '计算机软件分类，包括系统软件和应用软件。', 'difficulty': 1, 'node_type': 'KnowledgePoint'},
        ],
        'edges': [
            {'from': 'CS101', 'to': 'kp_1', 'relation': 'CONTAINS'},
            {'from': 'CS101', 'to': 'kp_2', 'relation': 'CONTAINS'},
            {'from': 'CS101', 'to': 'kp_3', 'relation': 'CONTAINS'},
        ]
    },
    'CS102': {
        'nodes': [
            {'id': 'kp_4', 'label': '变量与数据类型', 'content': '编程语言中的变量概念和基本数据类型，如整型、浮点型、字符型等。', 'difficulty': 1, 'node_type': 'KnowledgePoint'},
            {'id': 'kp_5', 'label': '控制结构', 'content': '程序的基本控制结构，包括顺序、分支和循环结构。', 'difficulty': 2, 'node_type': 'KnowledgePoint'},
            {'id': 'kp_6', 'label': '函数与模块化', 'content': '函数的定义、调用和参数传递，以及模块化编程思想。', 'difficulty': 2, 'node_type': 'KnowledgePoint'},
            {'id': 'skill_1', 'label': '编程基础', 'description': '掌握基本编程语法和逻辑思维', 'node_type': 'Skill'},
        ],
        'edges': [
            {'from': 'CS102', 'to': 'kp_4', 'relation': 'CONTAINS'},
            {'from': 'CS102', 'to': 'kp_5', 'relation': 'CONTAINS'},
            {'from': 'CS102', 'to': 'kp_6', 'relation': 'CONTAINS'},
            {'from': 'CS102', 'to': 'skill_1', 'relation': 'BUILDS'},
        ]
    },
    'CS201': {
        'nodes': [
            {'id': 'kp_7', 'label': '数组', 'content': '数组的定义、特性和基本操作，包括一维数组和多维数组。', 'difficulty': 2, 'node_type': 'KnowledgePoint'},
            {'id': 'kp_8', 'label': '链表', 'content': '链表的结构、类型和基本操作，包括单链表、双链表和循环链表。', 'difficulty': 2, 'node_type': 'KnowledgePoint'},
            {'id': 'kp_9', 'label': '栈和队列', 'content': '栈和队列的概念、特性和实现方法。', 'difficulty': 2, 'node_type': 'KnowledgePoint'},
            {'id': 'kp_10', 'label': '树', 'content': '树的基本概念、二叉树、二叉搜索树和平衡树等。', 'difficulty': 3, 'node_type': 'KnowledgePoint'},
            {'id': 'kp_11', 'label': '图', 'content': '图的基本概念、存储结构和遍历算法。', 'difficulty': 3, 'node_type': 'KnowledgePoint'},
            {'id': 'skill_2', 'label': '数据结构应用', 'description': '能够选择合适的数据结构解决实际问题', 'node_type': 'Skill'},
        ],
        'edges': [
            {'from': 'CS201', 'to': 'kp_7', 'relation': 'CONTAINS'},
            {'from': 'CS201', 'to': 'kp_8', 'relation': 'CONTAINS'},
            {'from': 'CS201', 'to': 'kp_9', 'relation': 'CONTAINS'},
            {'from': 'CS201', 'to': 'kp_10', 'relation': 'CONTAINS'},
            {'from': 'CS201', 'to': 'kp_11', 'relation': 'CONTAINS'},
            {'from': 'CS201', 'to': 'skill_2', 'relation': 'BUILDS'},
        ]
    },
    'CS301': {
        'nodes': [
            {'id': 'kp_12', 'label': '算法复杂度分析', 'content': '时间复杂度和空间复杂度的概念和计算方法。', 'difficulty': 3, 'node_type': 'KnowledgePoint'},
            {'id': 'kp_13', 'label': '排序算法', 'content': '常见排序算法，如冒泡排序、插入排序、快速排序等。', 'difficulty': 3, 'node_type': 'KnowledgePoint'},
            {'id': 'kp_14', 'label': '分治策略', 'content': '分治算法的基本思想和应用。', 'difficulty': 3, 'node_type': 'KnowledgePoint'},
            {'id': 'kp_15', 'label': '动态规划', 'content': '动态规划的基本思想和应用，包括最优子结构和重叠子问题。', 'difficulty': 4, 'node_type': 'KnowledgePoint'},
            {'id': 'skill_3', 'label': '算法设计', 'description': '掌握常见算法设计范式，具备算法分析能力', 'node_type': 'Skill'},
        ],
        'edges': [
            {'from': 'CS301', 'to': 'kp_12', 'relation': 'CONTAINS'},
            {'from': 'CS301', 'to': 'kp_13', 'relation': 'CONTAINS'},
            {'from': 'CS301', 'to': 'kp_14', 'relation': 'CONTAINS'},
            {'from': 'CS301', 'to': 'kp_15', 'relation': 'CONTAINS'},
            {'from': 'CS301', 'to': 'skill_3', 'relation': 'BUILDS'},
        ]
    },
    'CS302': {
        'nodes': [
            {'id': 'kp_16', 'label': '进程与线程', 'content': '操作系统中进程和线程的概念、调度与同步机制。', 'difficulty': 3, 'node_type': 'KnowledgePoint'},
            {'id': 'kp_17', 'label': '内存管理', 'content': '虚拟内存、分页和分段等内存管理技术。', 'difficulty': 3, 'node_type': 'KnowledgePoint'},
            {'id': 'kp_18', 'label': '文件系统', 'content': '文件系统的组织结构、存储管理和访问控制。', 'difficulty': 3, 'node_type': 'KnowledgePoint'},
            {'id': 'skill_4', 'label': '系统编程', 'description': '具备操作系统级别的编程能力', 'node_type': 'Skill'},
        ],
        'edges': [
            {'from': 'CS302', 'to': 'kp_16', 'relation': 'CONTAINS'},
            {'from': 'CS302', 'to': 'kp_17', 'relation': 'CONTAINS'},
            {'from': 'CS302', 'to': 'kp_18', 'relation': 'CONTAINS'},
            {'from': 'CS302', 'to': 'skill_4', 'relation': 'BUILDS'},
        ]
    },
    'CS303': {
        'nodes': [
            {'id': 'kp_19', 'label': 'TCP/IP协议', 'content': 'TCP/IP协议族的层次结构和各层协议的功能。', 'difficulty': 3, 'node_type': 'KnowledgePoint'},
            {'id': 'kp_20', 'label': 'Socket编程', 'content': '基于Socket的网络编程模型和常见网络应用开发。', 'difficulty': 3, 'node_type': 'KnowledgePoint'},
            {'id': 'kp_21', 'label': '网络安全基础', 'content': '常见网络攻击手段和防御措施，加密与认证技术。', 'difficulty': 4, 'node_type': 'KnowledgePoint'},
            {'id': 'skill_5', 'label': '网络编程', 'description': '能够开发基于网络的分布式应用', 'node_type': 'Skill'},
        ],
        'edges': [
            {'from': 'CS303', 'to': 'kp_19', 'relation': 'CONTAINS'},
            {'from': 'CS303', 'to': 'kp_20', 'relation': 'CONTAINS'},
            {'from': 'CS303', 'to': 'kp_21', 'relation': 'CONTAINS'},
            {'from': 'CS303', 'to': 'skill_5', 'relation': 'BUILDS'},
        ]
    },
    'CS304': {
        'nodes': [
            {'id': 'kp_22', 'label': '关系模型', 'content': '关系数据库的基本概念，包括关系、属性、键等。', 'difficulty': 2, 'node_type': 'KnowledgePoint'},
            {'id': 'kp_23', 'label': 'SQL语言', 'content': '结构化查询语言，包括DDL、DML、DCL等。', 'difficulty': 2, 'node_type': 'KnowledgePoint'},
            {'id': 'kp_24', 'label': '数据库设计', 'content': 'ER模型、范式理论和数据库设计方法。', 'difficulty': 3, 'node_type': 'KnowledgePoint'},
            {'id': 'skill_6', 'label': '数据库设计', 'description': '具备数据库建模和优化能力', 'node_type': 'Skill'},
        ],
        'edges': [
            {'from': 'CS304', 'to': 'kp_22', 'relation': 'CONTAINS'},
            {'from': 'CS304', 'to': 'kp_23', 'relation': 'CONTAINS'},
            {'from': 'CS304', 'to': 'kp_24', 'relation': 'CONTAINS'},
            {'from': 'CS304', 'to': 'skill_6', 'relation': 'BUILDS'},
        ]
    },
    'CS401': {
        'nodes': [
            {'id': 'kp_25', 'label': '软件生命周期', 'content': '软件开发的需求、设计、实现、测试和维护阶段。', 'difficulty': 2, 'node_type': 'KnowledgePoint'},
            {'id': 'kp_26', 'label': '设计模式', 'content': '常见面向对象设计模式，如工厂、单例、观察者等。', 'difficulty': 3, 'node_type': 'KnowledgePoint'},
            {'id': 'kp_27', 'label': '软件测试', 'content': '单元测试、集成测试和系统测试的方法与工具。', 'difficulty': 3, 'node_type': 'KnowledgePoint'},
            {'id': 'skill_7', 'label': '软件开发', 'description': '具备完整软件工程项目的开发能力', 'node_type': 'Skill'},
        ],
        'edges': [
            {'from': 'CS401', 'to': 'kp_25', 'relation': 'CONTAINS'},
            {'from': 'CS401', 'to': 'kp_26', 'relation': 'CONTAINS'},
            {'from': 'CS401', 'to': 'kp_27', 'relation': 'CONTAINS'},
            {'from': 'CS401', 'to': 'skill_7', 'relation': 'BUILDS'},
        ]
    },
    'CS402': {
        'nodes': [
            {'id': 'kp_28', 'label': '机器学习基础', 'content': '监督学习、无监督学习和强化学习的基本概念。', 'difficulty': 3, 'node_type': 'KnowledgePoint'},
            {'id': 'kp_29', 'label': '特征工程', 'content': '数据预处理、特征提取和特征选择的方法。', 'difficulty': 3, 'node_type': 'KnowledgePoint'},
            {'id': 'kp_30', 'label': '模型评估', 'content': '交叉验证、混淆矩阵、ROC曲线等评估方法。', 'difficulty': 3, 'node_type': 'KnowledgePoint'},
            {'id': 'skill_8', 'label': 'AI应用开发', 'description': '能够构建和部署机器学习模型', 'node_type': 'Skill'},
        ],
        'edges': [
            {'from': 'CS402', 'to': 'kp_28', 'relation': 'CONTAINS'},
            {'from': 'CS402', 'to': 'kp_29', 'relation': 'CONTAINS'},
            {'from': 'CS402', 'to': 'kp_30', 'relation': 'CONTAINS'},
            {'from': 'CS402', 'to': 'skill_8', 'relation': 'BUILDS'},
        ]
    },
    'CS403': {
        'nodes': [
            {'id': 'kp_31', 'label': '神经网络结构', 'content': '前馈神经网络、卷积神经网络和循环神经网络的结构与原理。', 'difficulty': 4, 'node_type': 'KnowledgePoint'},
            {'id': 'kp_32', 'label': '反向传播', 'content': '梯度下降和反向传播算法的数学原理。', 'difficulty': 4, 'node_type': 'KnowledgePoint'},
            {'id': 'kp_33', 'label': '深度学习框架', 'content': 'PyTorch/TensorFlow的使用方法和模型训练流程。', 'difficulty': 3, 'node_type': 'KnowledgePoint'},
            {'id': 'skill_8b', 'label': 'AI应用开发', 'description': '能够构建和部署深度学习模型', 'node_type': 'Skill'},
        ],
        'edges': [
            {'from': 'CS403', 'to': 'kp_31', 'relation': 'CONTAINS'},
            {'from': 'CS403', 'to': 'kp_32', 'relation': 'CONTAINS'},
            {'from': 'CS403', 'to': 'kp_33', 'relation': 'CONTAINS'},
            {'from': 'CS403', 'to': 'skill_8b', 'relation': 'BUILDS'},
        ]
    },
    'CS404': {
        'nodes': [
            {'id': 'kp_34', 'label': 'NLP基础', 'content': '自然语言处理的基本任务，包括分词、词性标注和命名实体识别。', 'difficulty': 3, 'node_type': 'KnowledgePoint'},
            {'id': 'kp_35', 'label': 'Transformer架构', 'content': 'Self-Attention机制和Transformer模型的结构与原理。', 'difficulty': 4, 'node_type': 'KnowledgePoint'},
            {'id': 'kp_36', 'label': '大语言模型', 'content': 'GPT、BERT等预训练语言模型的原理与应用。', 'difficulty': 4, 'node_type': 'KnowledgePoint'},
            {'id': 'skill_8c', 'label': 'AI应用开发', 'description': '能够开发自然语言处理应用', 'node_type': 'Skill'},
        ],
        'edges': [
            {'from': 'CS404', 'to': 'kp_34', 'relation': 'CONTAINS'},
            {'from': 'CS404', 'to': 'kp_35', 'relation': 'CONTAINS'},
            {'from': 'CS404', 'to': 'kp_36', 'relation': 'CONTAINS'},
            {'from': 'CS404', 'to': 'skill_8c', 'relation': 'BUILDS'},
        ]
    },
    'CS405': {
        'nodes': [
            {'id': 'kp_37', 'label': '渲染管线', 'content': '图形渲染管线的各个阶段，包括顶点处理、光栅化和片元处理。', 'difficulty': 4, 'node_type': 'KnowledgePoint'},
            {'id': 'kp_38', 'label': '着色器编程', 'content': 'GLSL/HLSL着色器语言的语法和常见特效实现。', 'difficulty': 4, 'node_type': 'KnowledgePoint'},
            {'id': 'kp_39', 'label': '3D变换', 'content': '平移、旋转、缩放的矩阵表示和坐标系变换。', 'difficulty': 3, 'node_type': 'KnowledgePoint'},
            {'id': 'skill_9', 'label': '图形渲染', 'description': '具备三维图形编程和实时渲染开发能力', 'node_type': 'Skill'},
        ],
        'edges': [
            {'from': 'CS405', 'to': 'kp_37', 'relation': 'CONTAINS'},
            {'from': 'CS405', 'to': 'kp_38', 'relation': 'CONTAINS'},
            {'from': 'CS405', 'to': 'kp_39', 'relation': 'CONTAINS'},
            {'from': 'CS405', 'to': 'skill_9', 'relation': 'BUILDS'},
        ]
    },
}


@api_bp.route('/knowledge_graph/all_courses', methods=['GET'])
@jwt_required()
def get_all_courses_graph():
    """获取全部课程节点及先修关系，从 SQLite 读取，无需 Neo4j"""
    courses = Course.query.all()

    nodes = []
    edges = []
    seen_edges = set()

    for course in courses:
        nodes.append({
            "id": course.course_code,
            "label": course.course_name,
            "credit": course.credit,
            "course_type": course.course_type,
            "department": course.department,
            "description": course.description,
            "prerequisite": course.prerequisite,
            "node_type": "Course"
        })

        if course.prerequisite:
            prereq_codes = [c.strip() for c in course.prerequisite.split(',')]
            for prereq_code in prereq_codes:
                edge_key = f"{prereq_code}->{course.course_code}"
                if edge_key not in seen_edges:
                    seen_edges.add(edge_key)
                    edges.append({
                        "from": prereq_code,
                        "to": course.course_code,
                        "relation": "PREREQUISITE_OF"
                    })

    return jsonify({"nodes": nodes, "edges": edges}), 200


@api_bp.route('/knowledge_graph/expand/<string:course_code>', methods=['GET'])
@jwt_required()
def expand_course_node(course_code):
    """展开课程节点，返回知识点和技能子节点（静态数据）"""
    data = MOCK_EXPAND.get(course_code)
    if not data:
        return jsonify({"nodes": [], "edges": []}), 200
    return jsonify(data), 200


@api_bp.route('/knowledge_graph/course/<int:course_id>', methods=['GET'])
@jwt_required()
def get_course_knowledge_graph(course_id):
    """获取课程知识图谱（按 ID）"""
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"nodes": [], "edges": []}), 200
    data = MOCK_EXPAND.get(course.course_code, {"nodes": [], "edges": []})
    return jsonify(data), 200


@api_bp.route('/knowledge_graph/course/code/<string:course_code>', methods=['GET'])
@jwt_required()
def get_course_knowledge_graph_by_code(course_code):
    """根据课程代码获取知识图谱"""
    data = MOCK_EXPAND.get(course_code, {"nodes": [], "edges": []})
    return jsonify(data), 200


@api_bp.route('/knowledge_graph/career/<string:career_name>', methods=['GET'])
@jwt_required()
def get_career_path(career_name):
    """获取职业路径"""
    return jsonify({"nodes": [], "relationships": []}), 200


@api_bp.route('/knowledge_graph/learning_path/<string:major_name>', methods=['GET'])
@jwt_required()
def get_learning_path(major_name):
    """获取专业学习路径"""
    return jsonify({"major": major_name, "semesters": {}}), 200


@api_bp.route('/knowledge_graph/search', methods=['GET'])
@jwt_required()
def search_knowledge_graph():
    """搜索课程（从 SQLite 查询）"""
    keyword = request.args.get('keyword', '')
    if not keyword:
        return jsonify({"error": "缺少搜索关键词"}), 400

    courses = Course.query.filter(
        Course.course_name.contains(keyword) |
        Course.course_code.contains(keyword) |
        Course.description.contains(keyword)
    ).limit(20).all()

    results = [{"id": c.course_code, "type": "Course", "properties": c.to_dict()} for c in courses]
    return jsonify({"results": results}), 200
