from .neo4j_driver import Neo4jDriver
import logging

class KnowledgeGraphManager:
    """知识图谱管理类"""

    def __init__(self):
        """初始化"""
        self.neo4j = Neo4jDriver()
    
    def get_course_knowledge_graph(self, course_id=None, course_code=None):
        """获取课程的知识图谱
        
        Args:
            course_id: 课程ID
            course_code: 课程代码
            
        Returns:
            dict: 包含节点和关系的知识图谱
        """
        if not course_id and not course_code:
            return {"error": "需要提供course_id或course_code"}
            
        parameters = {}
        
        if course_id:
            query = """
            MATCH (c:Course {course_id: $course_id})
            OPTIONAL MATCH (c)-[r1:CONTAINS]->(k:KnowledgePoint)
            OPTIONAL MATCH (c)-[r2:BUILDS]->(s:Skill)
            OPTIONAL MATCH (c)-[r3:PREREQUISITE_OF]->(pc:Course)
            OPTIONAL MATCH (nc:Course)-[r4:PREREQUISITE_OF]->(c)
            RETURN c, k, r1, s, r2, pc, r3, nc, r4
            """
            parameters["course_id"] = int(course_id)
        else:
            query = """
            MATCH (c:Course {course_code: $course_code})
            OPTIONAL MATCH (c)-[r1:CONTAINS]->(k:KnowledgePoint)
            OPTIONAL MATCH (c)-[r2:BUILDS]->(s:Skill)
            OPTIONAL MATCH (c)-[r3:PREREQUISITE_OF]->(pc:Course)
            OPTIONAL MATCH (nc:Course)-[r4:PREREQUISITE_OF]->(c)
            RETURN c, k, r1, s, r2, pc, r3, nc, r4
            """
            parameters["course_code"] = course_code
        
        results = self.neo4j.run_query(query, parameters)
        
        if not results:
            return {"nodes": [], "relationships": []}
        
        # 处理结果
        nodes = {}
        relationships = []
        
        for record in results:
            # 处理主课程
            course = record.get("c")
            if course and course.id not in nodes:
                nodes[course.id] = {
                    "id": course.id,
                    "labels": list(course.labels),
                    "properties": dict(course)
                }
            
            # 处理知识点
            knowledge = record.get("k")
            if knowledge and knowledge.id not in nodes:
                nodes[knowledge.id] = {
                    "id": knowledge.id,
                    "labels": list(knowledge.labels),
                    "properties": dict(knowledge)
                }
                
                # 添加关系
                r1 = record.get("r1")
                if r1:
                    relationships.append({
                        "id": r1.id,
                        "type": r1.type,
                        "start": r1.start_node.id,
                        "end": r1.end_node.id,
                        "properties": dict(r1)
                    })
            
            # 处理技能
            skill = record.get("s")
            if skill and skill.id not in nodes:
                nodes[skill.id] = {
                    "id": skill.id,
                    "labels": list(skill.labels),
                    "properties": dict(skill)
                }
                
                # 添加关系
                r2 = record.get("r2")
                if r2:
                    relationships.append({
                        "id": r2.id,
                        "type": r2.type,
                        "start": r2.start_node.id,
                        "end": r2.end_node.id,
                        "properties": dict(r2)
                    })
            
            # 处理后续课程
            post_course = record.get("pc")
            if post_course and post_course.id not in nodes:
                nodes[post_course.id] = {
                    "id": post_course.id,
                    "labels": list(post_course.labels),
                    "properties": dict(post_course)
                }
                
                # 添加关系
                r3 = record.get("r3")
                if r3:
                    relationships.append({
                        "id": r3.id,
                        "type": r3.type,
                        "start": r3.start_node.id,
                        "end": r3.end_node.id,
                        "properties": dict(r3)
                    })
            
            # 处理先修课程
            pre_course = record.get("nc")
            if pre_course and pre_course.id not in nodes:
                nodes[pre_course.id] = {
                    "id": pre_course.id,
                    "labels": list(pre_course.labels),
                    "properties": dict(pre_course)
                }
                
                # 添加关系
                r4 = record.get("r4")
                if r4:
                    relationships.append({
                        "id": r4.id,
                        "type": r4.type,
                        "start": r4.start_node.id,
                        "end": r4.end_node.id,
                        "properties": dict(r4)
                    })
        
        return {
            "nodes": list(nodes.values()),
            "relationships": relationships
        }
    
    def get_career_path(self, career_name):
        """获取特定职业的路径图谱
        
        Args:
            career_name: 职业名称
            
        Returns:
            dict: 包含路径的知识图谱
        """
        query = """
        MATCH (c:Career {name: $career_name})
        OPTIONAL MATCH (c)-[r1:REQUIRES]->(s:Skill)
        OPTIONAL MATCH (course:Course)-[r2:BUILDS]->(s)
        OPTIONAL MATCH (course)-[r3:BELONGS_TO]->(m:Major)
        RETURN c, s, r1, course, r2, m, r3
        """
        
        results = self.neo4j.run_query(query, {"career_name": career_name})
        
        if not results:
            return {"nodes": [], "relationships": []}
        
        # 处理结果
        nodes = {}
        relationships = []
        
        for record in results:
            # 处理职业
            career = record.get("c")
            if career and career.id not in nodes:
                nodes[career.id] = {
                    "id": career.id,
                    "labels": list(career.labels),
                    "properties": dict(career)
                }
            
            # 处理技能
            skill = record.get("s")
            if skill and skill.id not in nodes:
                nodes[skill.id] = {
                    "id": skill.id,
                    "labels": list(skill.labels),
                    "properties": dict(skill)
                }
                
                # 添加关系
                r1 = record.get("r1")
                if r1:
                    relationships.append({
                        "id": r1.id,
                        "type": r1.type,
                        "start": r1.start_node.id,
                        "end": r1.end_node.id,
                        "properties": dict(r1)
                    })
            
            # 处理课程
            course = record.get("course")
            if course and course.id not in nodes:
                nodes[course.id] = {
                    "id": course.id,
                    "labels": list(course.labels),
                    "properties": dict(course)
                }
                
                # 添加关系
                r2 = record.get("r2")
                if r2:
                    relationships.append({
                        "id": r2.id,
                        "type": r2.type,
                        "start": r2.start_node.id,
                        "end": r2.end_node.id,
                        "properties": dict(r2)
                    })
            
            # 处理专业
            major = record.get("m")
            if major and major.id not in nodes:
                nodes[major.id] = {
                    "id": major.id,
                    "labels": list(major.labels),
                    "properties": dict(major)
                }
                
                # 添加关系
                r3 = record.get("r3")
                if r3:
                    relationships.append({
                        "id": r3.id,
                        "type": r3.type,
                        "start": r3.start_node.id,
                        "end": r3.end_node.id,
                        "properties": dict(r3)
                    })
        
        return {
            "nodes": list(nodes.values()),
            "relationships": relationships
        }
    
    def get_learning_path(self, major_name, semester_count=8):
        """获取特定专业的学习路径
        
        Args:
            major_name: 专业名称
            semester_count: 学期数量
            
        Returns:
            dict: 按学期组织的课程推荐
        """
        query = """
        MATCH (m:Major {name: $major_name})<-[:BELONGS_TO]-(c:Course)
        OPTIONAL MATCH (c)-[:PREREQUISITE_OF*0..3]->(other:Course)-[:BELONGS_TO]->(m)
        WITH c, COLLECT(other) AS dependencies
        RETURN c.course_id AS course_id, c.course_name AS course_name, 
               c.course_code AS course_code, c.credit AS credit,
               c.course_type AS course_type, c.prerequisite AS prerequisite,
               SIZE(dependencies) AS dependency_count
        ORDER BY dependency_count
        """
        
        results = self.neo4j.run_query(query, {"major_name": major_name})
        
        if not results:
            return {"error": "未找到相关专业或课程"}
        
        # 处理结果
        courses = []
        for record in results:
            courses.append({
                "course_id": record["course_id"],
                "course_name": record["course_name"],
                "course_code": record["course_code"],
                "credit": record["credit"],
                "course_type": record["course_type"],
                "prerequisite": record["prerequisite"],
                "dependency_count": record["dependency_count"]
            })
        
        # 按学期分配课程
        semesters = {}
        for i in range(1, semester_count + 1):
            semesters[f"学期{i}"] = []
        
        # 简单的贪心分配算法
        current_semester = 1
        courses_per_semester = len(courses) // semester_count + 1
        
        for course in courses:
            if len(semesters[f"学期{current_semester}"]) >= courses_per_semester:
                current_semester = min(current_semester + 1, semester_count)
            
            semesters[f"学期{current_semester}"].append(course)
        
        return {
            "major": major_name,
            "semesters": semesters
        }
    
    def search_knowledge_graph(self, keyword):
        """搜索知识图谱
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            dict: 搜索结果
        """
        query = """
        MATCH (n)
        WHERE toLower(n.name) CONTAINS toLower($keyword)
           OR (n:Course AND (toLower(n.course_name) CONTAINS toLower($keyword) 
                           OR toLower(n.course_code) CONTAINS toLower($keyword)))
           OR (n:KnowledgePoint AND toLower(n.content) CONTAINS toLower($keyword))
        RETURN n, labels(n) AS node_type
        LIMIT 20
        """
        
        results = self.neo4j.run_query(query, {"keyword": keyword})
        
        if not results:
            return {"results": []}
        
        search_results = []
        for record in results:
            node = record["n"]
            node_type = record["node_type"][0] if record["node_type"] else "Unknown"
            
            properties = dict(node)
            
            search_results.append({
                "id": node.id,
                "type": node_type,
                "properties": properties
            })
        
        return {"results": search_results} 