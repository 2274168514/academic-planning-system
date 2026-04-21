from flask import request, jsonify
from flask_jwt_extended import jwt_required
from . import api_bp
from ..models import Course
from .. import db

@api_bp.route('/courses', methods=['GET'])
@jwt_required()
def get_courses():
    """获取所有课程"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # 筛选条件
    department = request.args.get('department')
    course_type = request.args.get('course_type')
    search = request.args.get('search')
    
    query = Course.query
    
    if department:
        query = query.filter_by(department=department)
    
    if course_type:
        query = query.filter_by(course_type=course_type)
    
    if search:
        query = query.filter(
            db.or_(
                Course.course_name.like(f'%{search}%'),
                Course.course_code.like(f'%{search}%'),
                Course.description.like(f'%{search}%')
            )
        )
    
    pagination = query.paginate(page=page, per_page=per_page)
    courses = pagination.items
    
    return jsonify({
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": page,
        "per_page": per_page,
        "courses": [course.to_dict() for course in courses]
    }), 200


@api_bp.route('/courses/<int:course_id>', methods=['GET'])
@jwt_required()
def get_course(course_id):
    """获取指定课程详情"""
    course = Course.query.get(course_id)
    
    if not course:
        return jsonify({"error": "课程不存在"}), 404
    
    # 获取先修课程信息
    prereq_courses = []
    if course.prerequisite:
        prereq_codes = [code.strip() for code in course.prerequisite.split(',')]
        prereq_courses = Course.query.filter(Course.course_code.in_(prereq_codes)).all()
    
    course_dict = course.to_dict()
    course_dict['prerequisite_courses'] = [c.to_dict() for c in prereq_courses]
    
    return jsonify({
        "course": course_dict
    }), 200


@api_bp.route('/courses/departments', methods=['GET'])
@jwt_required()
def get_departments():
    """获取所有院系"""
    departments = db.session.query(Course.department).distinct().all()
    departments = [d[0] for d in departments]
    
    return jsonify({
        "departments": departments
    }), 200


@api_bp.route('/courses/types', methods=['GET'])
@jwt_required()
def get_course_types():
    """获取所有课程类型"""
    course_types = db.session.query(Course.course_type).distinct().all()
    course_types = [t[0] for t in course_types]
    
    return jsonify({
        "course_types": course_types
    }), 200


@api_bp.route('/courses/prerequisites/<int:course_id>', methods=['GET'])
@jwt_required()
def get_prerequisites(course_id):
    """获取指定课程的先修课程"""
    course = Course.query.get(course_id)
    
    if not course:
        return jsonify({"error": "课程不存在"}), 404
    
    prereq_courses = []
    if course.prerequisite:
        prereq_codes = [code.strip() for code in course.prerequisite.split(',')]
        prereq_courses = Course.query.filter(Course.course_code.in_(prereq_codes)).all()
    
    return jsonify({
        "prerequisite_courses": [course.to_dict() for course in prereq_courses]
    }), 200 