import os
import sys
from dotenv import load_dotenv
import logging

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 加载环境变量
load_dotenv()

from app import create_app
from app.knowledge_graph import Neo4jDriver
from app.models import Course

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def init_knowledge_graph():
    """初始化知识图谱"""
    logger.info("连接Neo4j数据库...")
    neo4j = Neo4jDriver()
    if not neo4j.test_connection():
        logger.error("Neo4j连接失败!")
        return
    logger.info("连接成功!")
    # 创建约束
    logger.info("创建约束...")
    constraints = [
        "CREATE CONSTRAINT course_id IF NOT EXISTS FOR (c:Course) REQUIRE c.course_id IS UNIQUE",
        "CREATE CONSTRAINT course_code IF NOT EXISTS FOR (c:Course) REQUIRE c.course_code IS UNIQUE",
        "CREATE CONSTRAINT knowledge_point_id IF NOT EXISTS FOR (k:KnowledgePoint) REQUIRE k.id IS UNIQUE",
        "CREATE CONSTRAINT skill_id IF NOT EXISTS FOR (s:Skill) REQUIRE s.id IS UNIQUE",
        "CREATE CONSTRAINT career_id IF NOT EXISTS FOR (c:Career) REQUIRE c.id IS UNIQUE",
        "CREATE CONSTRAINT major_id IF NOT EXISTS FOR (m:Major) REQUIRE m.id IS UNIQUE"
    ]
    for constraint in constraints:
        try:
            neo4j.run_query(constraint)
        except Exception as e:
            logger.warning(f"创建约束失败: {str(e)}")
    # 清空数据库
    logger.info("清空知识图谱数据...")
    neo4j.run_query("MATCH (n) DETACH DELETE n")
    # 创建课程节点
    logger.info("创建课程节点...")
    courses = Course.query.all()
    for course in courses:
        query = """
        CREATE (c:Course {
            course_id: $course_id,
            course_code: $course_code,
            course_name: $course_name,
            credit: $credit,
            course_type: $course_type,
            department: $department,
            prerequisite: $prerequisite,
            description: $description
        })
        """
        params = {
            'course_id': course.course_id,
            'course_code': course.course_code,
            'course_name': course.course_name,
            'credit': course.credit,
            'course_type': course.course_type,
            'department': course.department,
            'prerequisite': course.prerequisite,
            'description': course.description
        }
        neo4j.run_query(query, params)
        logger.info(f"创建课程节点: {course.course_name}")
    # 创建知识点节点
    logger.info("创建知识点节点...")
    knowledge_points = [
        # 计算机导论相关知识点
        {'id': 1, 'name': '计算机历史', 'course_code': 'CS101', 'content': '计算机发展历史，从机械计算设备到现代计算机的演变过程。'},
        {'id': 2, 'name': '计算机硬件基础', 'course_code': 'CS101', 'content': '计算机硬件组成，包括CPU、内存、存储设备和输入输出设备等。'},
        {'id': 3, 'name': '计算机软件基础', 'course_code': 'CS101', 'content': '计算机软件分类，包括系统软件和应用软件。'},
        
        # 程序设计基础相关知识点
        {'id': 4, 'name': '变量与数据类型', 'course_code': 'CS102', 'content': '编程语言中的变量概念和基本数据类型，如整型、浮点型、字符型等。'},
        {'id': 5, 'name': '控制结构', 'course_code': 'CS102', 'content': '程序的基本控制结构，包括顺序、分支和循环结构。'},
        {'id': 6, 'name': '函数与模块化', 'course_code': 'CS102', 'content': '函数的定义、调用和参数传递，以及模块化编程思想。'},
        
        # 数据结构相关知识点
        {'id': 7, 'name': '数组', 'course_code': 'CS201', 'content': '数组的定义、特性和基本操作，包括一维数组和多维数组。'},
        {'id': 8, 'name': '链表', 'course_code': 'CS201', 'content': '链表的结构、类型和基本操作，包括单链表、双链表和循环链表。'},
        {'id': 9, 'name': '栈和队列', 'course_code': 'CS201', 'content': '栈和队列的概念、特性和实现方法。'},
        {'id': 10, 'name': '树', 'course_code': 'CS201', 'content': '树的基本概念、二叉树、二叉搜索树和平衡树等。'},
        {'id': 11, 'name': '图', 'course_code': 'CS201', 'content': '图的基本概念、存储结构和遍历算法。'},
        
        # 算法设计与分析相关知识点
        {'id': 12, 'name': '算法复杂度分析', 'course_code': 'CS301', 'content': '时间复杂度和空间复杂度的概念和计算方法。'},
        {'id': 13, 'name': '排序算法', 'course_code': 'CS301', 'content': '常见排序算法，如冒泡排序、插入排序、快速排序等。'},
        {'id': 14, 'name': '搜索算法', 'course_code': 'CS301', 'content': '常见搜索算法，如顺序搜索、二分搜索、深度优先搜索和广度优先搜索等。'},
        {'id': 15, 'name': '分治策略', 'course_code': 'CS301', 'content': '分治算法的基本思想和应用。'},
        {'id': 16, 'name': '动态规划', 'course_code': 'CS301', 'content': '动态规划的基本思想和应用，包括最优子结构和重叠子问题。'},
        {'id': 17, 'name': '贪心算法', 'course_code': 'CS301', 'content': '贪心算法的基本思想和应用。'}
    ]
    
    for kp in knowledge_points:
        query = """
        MATCH (c:Course {course_code: $course_code})
        CREATE (k:KnowledgePoint {id: $id, name: $name, content: $content})
        CREATE (c)-[:CONTAINS]->(k)
        """
        
        neo4j.run_query(query, kp)
        logger.info(f"创建知识点节点: {kp['name']}")
    
    # 创建技能节点
    logger.info("创建技能节点...")
    skills = [
        {'id': 1, 'name': '编程基础', 'course_codes': ['CS102']},
        {'id': 2, 'name': '数据结构应用', 'course_codes': ['CS201']},
        {'id': 3, 'name': '算法设计', 'course_codes': ['CS301']},
        {'id': 4, 'name': '系统编程', 'course_codes': ['CS302']},
        {'id': 5, 'name': '网络编程', 'course_codes': ['CS303']},
        {'id': 6, 'name': '数据库设计', 'course_codes': ['CS304']},
        {'id': 7, 'name': '软件开发', 'course_codes': ['CS401']},
        {'id': 8, 'name': 'AI应用开发', 'course_codes': ['CS402', 'CS403', 'CS404']},
        {'id': 9, 'name': '图形渲染', 'course_codes': ['CS405']}
    ]
    
    for skill in skills:
        # 创建技能节点
        query = """
        CREATE (s:Skill {id: $id, name: $name})
        """
        
        neo4j.run_query(query, {'id': skill['id'], 'name': skill['name']})
        
        # 建立与课程的关系
        for course_code in skill['course_codes']:
            query = """
            MATCH (c:Course {course_code: $course_code})
            MATCH (s:Skill {id: $skill_id})
            CREATE (c)-[:BUILDS]->(s)
            """
            
            neo4j.run_query(query, {'course_code': course_code, 'skill_id': skill['id']})
        
        logger.info(f"创建技能节点: {skill['name']}")
    
    # 创建专业节点
    logger.info("创建专业节点...")
    majors = [
        {'id': 1, 'name': '计算机科学与技术', 'course_codes': ['CS101', 'CS102', 'CS201', 'CS301', 'CS302', 'CS303', 'CS304', 'CS401']},
        {'id': 2, 'name': '软件工程', 'course_codes': ['CS101', 'CS102', 'CS201', 'CS301', 'CS304', 'CS401']},
        {'id': 3, 'name': '人工智能', 'course_codes': ['CS101', 'CS102', 'CS201', 'CS301', 'CS302', 'CS402', 'CS403', 'CS404']}
    ]
    
    for major in majors:
        # 创建专业节点
        query = """
        CREATE (m:Major {id: $id, name: $name})
        """
        
        neo4j.run_query(query, {'id': major['id'], 'name': major['name']})
        
        # 建立与课程的关系
        for course_code in major['course_codes']:
            query = """
            MATCH (c:Course {course_code: $course_code})
            MATCH (m:Major {id: $major_id})
            CREATE (c)-[:BELONGS_TO]->(m)
            """
            
            neo4j.run_query(query, {'course_code': course_code, 'major_id': major['id']})
        
        logger.info(f"创建专业节点: {major['name']}")
    
    # 创建职业节点
    logger.info("创建职业节点...")
    careers = [
        {'id': 1, 'name': '软件开发工程师', 'skill_ids': [1, 2, 3, 7]},
        {'id': 2, 'name': '数据库工程师', 'skill_ids': [1, 2, 6]},
        {'id': 3, 'name': '系统架构师', 'skill_ids': [3, 4, 7]},
        {'id': 4, 'name': '人工智能工程师', 'skill_ids': [1, 2, 3, 8]},
        {'id': 5, 'name': '游戏开发工程师', 'skill_ids': [1, 2, 3, 9]}
    ]
    
    for career in careers:
        # 创建职业节点
        query = """
        CREATE (c:Career {id: $id, name: $name})
        """
        
        neo4j.run_query(query, {'id': career['id'], 'name': career['name']})
        
        # 建立与技能的关系
        for skill_id in career['skill_ids']:
            query = """
            MATCH (s:Skill {id: $skill_id})
            MATCH (c:Career {id: $career_id})
            CREATE (c)-[:REQUIRES]->(s)
            """
            
            neo4j.run_query(query, {'skill_id': skill_id, 'career_id': career['id']})
        
        logger.info(f"创建职业节点: {career['name']}")
    
    # 建立课程之间的先修关系
    logger.info("建立课程先修关系...")
    for course in courses:
        if course.prerequisite:
            prereq_codes = [code.strip() for code in course.prerequisite.split(',')]
            for prereq_code in prereq_codes:
                query = """
                MATCH (c1:Course {course_code: $prereq_code})
                MATCH (c2:Course {course_code: $course_code})
                CREATE (c1)-[:PREREQUISITE_OF]->(c2)
                """
                
                neo4j.run_query(query, {'prereq_code': prereq_code, 'course_code': course.course_code})
                logger.info(f"建立先修关系: {prereq_code} -> {course.course_code}")
    
    # 建立专业与职业的关系
    logger.info("建立专业与职业的关系...")
    major_careers = [
        {'major_id': 1, 'career_ids': [1, 2, 3, 4, 5]},
        {'major_id': 2, 'career_ids': [1, 3]},
        {'major_id': 3, 'career_ids': [4, 5]}
    ]
    
    for mc in major_careers:
        for career_id in mc['career_ids']:
            query = """
            MATCH (m:Major {id: $major_id})
            MATCH (c:Career {id: $career_id})
            CREATE (m)-[:LEADS_TO]->(c)
            """
            
            neo4j.run_query(query, {'major_id': mc['major_id'], 'career_id': career_id})
            logger.info(f"建立专业与职业关系: 专业{mc['major_id']} -> 职业{career_id}")
    
    logger.info("知识图谱初始化完成!")

if __name__ == '__main__':
    app = create_app('development')
    with app.app_context():
        init_knowledge_graph() 