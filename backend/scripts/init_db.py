import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 加载环境变量
load_dotenv()

from app import create_app, db
from app.models import User, Course, StudyPlan, PlanDetail, LearningRecord

def create_sample_data():
    """创建示例数据"""
    print("创建示例数据...")
    
    # 创建用户
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@example.com',
            major='计算机科学与技术',
            grade='大三',
            phone='13800138000'
        )
        admin.password = 'admin123'
        db.session.add(admin)
        print("创建用户: admin")
    
    # 创建课程
    courses_data = [
        {
            'course_name': '计算机导论',
            'course_code': 'CS101',
            'credit': 3.0,
            'course_type': '必修',
            'department': '计算机科学与技术',
            'prerequisite': '',
            'description': '计算机科学的基础课程，介绍计算机的基本概念、原理和应用。'
        },
        {
            'course_name': '程序设计基础',
            'course_code': 'CS102',
            'credit': 4.0,
            'course_type': '必修',
            'department': '计算机科学与技术',
            'prerequisite': '',
            'description': '介绍基本的程序设计概念和方法，使用C/C++语言。'
        },
        {
            'course_name': '数据结构',
            'course_code': 'CS201',
            'credit': 4.0,
            'course_type': '必修',
            'department': '计算机科学与技术',
            'prerequisite': 'CS102',
            'description': '介绍基本的数据结构和算法，包括数组、链表、栈、队列、树、图等。'
        },
        {
            'course_name': '算法设计与分析',
            'course_code': 'CS301',
            'credit': 3.0,
            'course_type': '必修',
            'department': '计算机科学与技术',
            'prerequisite': 'CS201',
            'description': '介绍常见的算法设计技术和分析方法，包括分治、动态规划、贪心等。'
        },
        {
            'course_name': '操作系统',
            'course_code': 'CS302',
            'credit': 4.0,
            'course_type': '必修',
            'department': '计算机科学与技术',
            'prerequisite': 'CS201',
            'description': '介绍操作系统的基本概念、原理和实现方法。'
        },
        {
            'course_name': '计算机网络',
            'course_code': 'CS303',
            'credit': 3.0,
            'course_type': '必修',
            'department': '计算机科学与技术',
            'prerequisite': 'CS101',
            'description': '介绍计算机网络的基本概念、原理和协议。'
        },
        {
            'course_name': '数据库系统',
            'course_code': 'CS304',
            'credit': 4.0,
            'course_type': '必修',
            'department': '计算机科学与技术',
            'prerequisite': 'CS201',
            'description': '介绍数据库系统的基本概念、原理和实现方法。'
        },
        {
            'course_name': '软件工程',
            'course_code': 'CS401',
            'credit': 3.0,
            'course_type': '必修',
            'department': '计算机科学与技术',
            'prerequisite': 'CS304',
            'description': '介绍软件开发的原则、方法和工具。'
        },
        {
            'course_name': '人工智能',
            'course_code': 'CS402',
            'credit': 3.0,
            'course_type': '选修',
            'department': '计算机科学与技术',
            'prerequisite': 'CS301',
            'description': '介绍人工智能的基本概念、原理和应用。'
        },
        {
            'course_name': '机器学习',
            'course_code': 'CS403',
            'credit': 3.0,
            'course_type': '选修',
            'department': '计算机科学与技术',
            'prerequisite': 'CS402',
            'description': '介绍机器学习的基本概念、原理和算法。'
        },
        {
            'course_name': '深度学习',
            'course_code': 'CS404',
            'credit': 3.0,
            'course_type': '选修',
            'department': '计算机科学与技术',
            'prerequisite': 'CS403',
            'description': '介绍深度学习的基本概念、原理和模型。'
        },
        {
            'course_name': '计算机图形学',
            'course_code': 'CS405',
            'credit': 3.0,
            'course_type': '选修',
            'department': '计算机科学与技术',
            'prerequisite': 'CS201',
            'description': '介绍计算机图形学的基本概念、原理和算法。'
        }
    ]
    
    for course_data in courses_data:
        course = Course.query.filter_by(course_code=course_data['course_code']).first()
        if not course:
            course = Course(**course_data)
            db.session.add(course)
            print(f"创建课程: {course_data['course_name']}")
    
    # 创建学习计划
    plan = StudyPlan.query.filter_by(user_id=1, plan_name='我的本科学习计划').first()
    if not plan and admin.user_id:
        plan = StudyPlan(
            user_id=admin.user_id,
            plan_name='我的本科学习计划',
            description='计算机科学与技术专业本科四年学习计划'
        )
        db.session.add(plan)
        db.session.flush()  # 获取plan_id
        
        # 添加计划详情
        details_data = [
            {'course_code': 'CS101', 'semester': '大一上学期', 'priority': 1},
            {'course_code': 'CS102', 'semester': '大一上学期', 'priority': 2},
            {'course_code': 'CS201', 'semester': '大一下学期', 'priority': 1},
            {'course_code': 'CS301', 'semester': '大二上学期', 'priority': 1},
            {'course_code': 'CS302', 'semester': '大二上学期', 'priority': 2},
            {'course_code': 'CS303', 'semester': '大二下学期', 'priority': 1},
            {'course_code': 'CS304', 'semester': '大二下学期', 'priority': 2},
            {'course_code': 'CS401', 'semester': '大三上学期', 'priority': 1},
            {'course_code': 'CS402', 'semester': '大三上学期', 'priority': 2},
            {'course_code': 'CS403', 'semester': '大三下学期', 'priority': 1},
            {'course_code': 'CS404', 'semester': '大四上学期', 'priority': 1},
            {'course_code': 'CS405', 'semester': '大四上学期', 'priority': 2}
        ]
        
        for detail_data in details_data:
            course = Course.query.filter_by(course_code=detail_data['course_code']).first()
            if course:
                detail = PlanDetail(
                    plan_id=plan.plan_id,
                    course_id=course.course_id,
                    semester=detail_data['semester'],
                    priority=detail_data['priority']
                )
                db.session.add(detail)
                print(f"添加计划详情: {detail_data['course_code']} - {detail_data['semester']}")
    
    # 创建学习记录
    if admin.user_id:
        # 计算机导论
        course = Course.query.filter_by(course_code='CS101').first()
        if course and not LearningRecord.query.filter_by(user_id=admin.user_id, course_id=course.course_id).first():
            record = LearningRecord(
                user_id=admin.user_id,
                course_id=course.course_id,
                start_time=datetime(2021, 9, 1),
                finish_time=datetime(2022, 1, 15),
                score=95.0,
                status='completed',
                notes='第一学期学习，课程内容简单易懂，对计算机基础知识有了系统了解。'
            )
            db.session.add(record)
            print(f"添加学习记录: {course.course_name} - completed")
        
        # 程序设计基础
        course = Course.query.filter_by(course_code='CS102').first()
        if course and not LearningRecord.query.filter_by(user_id=admin.user_id, course_id=course.course_id).first():
            record = LearningRecord(
                user_id=admin.user_id,
                course_id=course.course_id,
                start_time=datetime(2021, 9, 1),
                finish_time=datetime(2022, 1, 15),
                score=88.0,
                status='completed',
                notes='学习了C/C++基础，编写了多个小程序，提升了编程能力。'
            )
            db.session.add(record)
            print(f"添加学习记录: {course.course_name} - completed")
        
        # 数据结构
        course = Course.query.filter_by(course_code='CS201').first()
        if course and not LearningRecord.query.filter_by(user_id=admin.user_id, course_id=course.course_id).first():
            record = LearningRecord(
                user_id=admin.user_id,
                course_id=course.course_id,
                start_time=datetime(2022, 2, 20),
                finish_time=datetime(2022, 6, 30),
                score=85.0,
                status='completed',
                notes='学习了各种数据结构及其实现，难度较大但收获很多。'
            )
            db.session.add(record)
            print(f"添加学习记录: {course.course_name} - completed")
        
        # 算法设计与分析
        course = Course.query.filter_by(course_code='CS301').first()
        if course and not LearningRecord.query.filter_by(user_id=admin.user_id, course_id=course.course_id).first():
            record = LearningRecord(
                user_id=admin.user_id,
                course_id=course.course_id,
                start_time=datetime(2022, 9, 1),
                status='in_progress',
                notes='正在学习各种算法设计技术，课程难度较大。'
            )
            db.session.add(record)
            print(f"添加学习记录: {course.course_name} - in_progress")
    
    db.session.commit()
    print("示例数据创建完成!")

def init_db():
    """初始化数据库"""
    app = create_app('development')
    
    with app.app_context():
        print("创建数据库表...")
        db.create_all()
        
        create_sample_data()

if __name__ == '__main__':
    init_db() 