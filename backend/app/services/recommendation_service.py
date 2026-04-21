import logging
from ..models import Course, LearningRecord, User, StudyPlan
from .. import db
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class RecommendationService:
    """推荐服务类，用于生成个性化推荐"""

    def __init__(self):
        """初始化"""
        pass
    
    def recommend_courses(self, user_id, limit=10):
        """为用户推荐课程
        
        Args:
            user_id: 用户ID
            limit: 推荐数量限制
            
        Returns:
            list: 推荐课程列表
        """
        user = User.query.get(user_id)
        if not user:
            return {"error": "用户不存在"}
        
        # 获取用户已学课程
        learned_courses = LearningRecord.query.filter_by(user_id=user_id).all()
        learned_course_ids = [record.course_id for record in learned_courses]
        
        # 获取用户专业
        major = user.major
        
        # 基于专业推荐
        if major:
            # 获取该专业的热门课程
            major_courses = Course.query.filter(
                Course.department.like(f"%{major}%"),
                ~Course.course_id.in_(learned_course_ids) if learned_course_ids else True
            ).limit(limit).all()
            
            if major_courses:
                return [course.to_dict() for course in major_courses]
        
        # 如果没有专业或专业课程为空，返回通用推荐
        general_courses = Course.query.filter(
            ~Course.course_id.in_(learned_course_ids) if learned_course_ids else True
        ).order_by(db.func.random()).limit(limit).all()
        
        return [course.to_dict() for course in general_courses]
    
    def recommend_based_on_completed(self, user_id, limit=5):
        """基于已完成课程推荐后续课程
        
        Args:
            user_id: 用户ID
            limit: 推荐数量限制
            
        Returns:
            list: 推荐课程列表
        """
        # 获取用户已完成的课程
        completed_records = LearningRecord.query.filter_by(
            user_id=user_id,
            status='completed'
        ).all()
        
        if not completed_records:
            return []
        
        # 获取已完成课程的ID
        completed_course_ids = [record.course_id for record in completed_records]
        
        # 获取这些课程
        completed_courses = Course.query.filter(Course.course_id.in_(completed_course_ids)).all()
        
        # 收集推荐结果
        recommendations = []
        
        # 基于先修课程关系推荐
        for course in completed_courses:
            # 找出以当前课程为先修课的课程
            if not course.prerequisite:
                continue
                
            # 解析先修课程代码
            next_courses = []
            course_code = course.course_code
            
            # 查找以本课程为先修课的课程
            potential_next_courses = Course.query.filter(
                Course.prerequisite.like(f"%{course_code}%")
            ).all()
            
            for next_course in potential_next_courses:
                if next_course.course_id not in completed_course_ids and next_course not in next_courses:
                    next_courses.append(next_course)
            
            recommendations.extend(next_courses)
            
            if len(recommendations) >= limit:
                break
        
        # 如果推荐不足，添加同一领域的其他课程
        if len(recommendations) < limit:
            # 获取用户已学课程的部门/领域
            departments = set()
            for course in completed_courses:
                departments.add(course.department)
            
            # 查找同领域但未学习的课程
            additional_courses = Course.query.filter(
                Course.department.in_(departments),
                ~Course.course_id.in_(completed_course_ids),
                ~Course.course_id.in_([c.course_id for c in recommendations])
            ).order_by(db.func.random()).limit(limit - len(recommendations)).all()
            
            recommendations.extend(additional_courses)
        
        return [course.to_dict() for course in recommendations[:limit]]
    
    def recommend_study_plan(self, user_id, semester_count=8):
        """推荐学习计划
        
        Args:
            user_id: 用户ID
            semester_count: 学期数量
            
        Returns:
            dict: 学习计划
        """
        user = User.query.get(user_id)
        if not user:
            return {"error": "用户不存在"}
        
        # 获取用户专业
        major = user.major
        if not major:
            return {"error": "用户未设置专业，无法生成计划"}
        
        # 获取该专业的所有课程
        courses = Course.query.filter(Course.department.like(f"%{major}%")).all()
        
        if not courses:
            return {"error": f"未找到与{major}专业相关的课程"}
        
        # 获取用户已学课程
        learned_course_ids = [
            record.course_id for record in 
            LearningRecord.query.filter_by(user_id=user_id).all()
        ]
        
        # 过滤掉已学课程
        courses = [c for c in courses if c.course_id not in learned_course_ids]
        
        # 课程分类：必修和选修
        required_courses = [c for c in courses if c.course_type == '必修']
        elective_courses = [c for c in courses if c.course_type == '选修']
        
        # 创建学期计划
        semesters = {}
        for i in range(1, semester_count + 1):
            semesters[f"学期{i}"] = []
        
        # 为必修课确定前序依赖关系
        dependencies = {}
        for course in required_courses:
            dependencies[course.course_id] = []
            if course.prerequisite:
                prerequisite_codes = [code.strip() for code in course.prerequisite.split(',')]
                for code in prerequisite_codes:
                    for c in required_courses:
                        if c.course_code == code:
                            dependencies[course.course_id].append(c.course_id)
        
        # 确定课程学习顺序
        course_order = []
        visited = set()
        
        def dfs(course_id):
            if course_id in visited:
                return
            visited.add(course_id)
            for dep in dependencies.get(course_id, []):
                dfs(dep)
            course_order.append(course_id)
        
        for course in required_courses:
            dfs(course.course_id)
        
        # 按学期分配必修课
        courses_per_semester = len(course_order) // semester_count + 1
        current_semester = 1
        
        for course_id in course_order:
            course = next((c for c in required_courses if c.course_id == course_id), None)
            if not course:
                continue
                
            if len(semesters[f"学期{current_semester}"]) >= courses_per_semester:
                current_semester = min(current_semester + 1, semester_count)
            
            semesters[f"学期{current_semester}"].append(course.to_dict())
        
        # 分配选修课
        elective_per_semester = 2  # 每学期2门选修
        for i in range(1, semester_count + 1):
            semester_key = f"学期{i}"
            # 如果当前学期课程已经很多，减少选修数
            available_slots = max(0, elective_per_semester - max(0, len(semesters[semester_key]) - courses_per_semester))
            
            if available_slots > 0 and elective_courses:
                # 选择当前学期的选修课
                semester_electives = elective_courses[:available_slots]
                elective_courses = elective_courses[available_slots:]
                
                for course in semester_electives:
                    semesters[semester_key].append(course.to_dict())
        
        return {
            "major": major,
            "semesters": semesters
        } 