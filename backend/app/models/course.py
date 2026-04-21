from .. import db

class Course(db.Model):
    """课程模型"""
    __tablename__ = 'courses'
    
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_name = db.Column(db.String(100), nullable=False, index=True)
    course_code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    credit = db.Column(db.Float, nullable=False)
    course_type = db.Column(db.String(20), nullable=False)  # 必修/选修
    department = db.Column(db.String(100), nullable=False)
    prerequisite = db.Column(db.String(255), nullable=True)  # 先修课程，用逗号分隔课程代码
    description = db.Column(db.Text, nullable=True)
    
    # 关系
    plan_details = db.relationship('PlanDetail', backref='course', lazy='dynamic')
    learning_records = db.relationship('LearningRecord', backref='course', lazy='dynamic')
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'course_code': self.course_code,
            'credit': self.credit,
            'course_type': self.course_type,
            'department': self.department,
            'prerequisite': self.prerequisite,
            'description': self.description
        }
    
    @staticmethod
    def get_prerequisites(course_code):
        """获取先修课程列表"""
        course = Course.query.filter_by(course_code=course_code).first()
        if not course or not course.prerequisite:
            return []
        
        prereq_codes = [code.strip() for code in course.prerequisite.split(',')]
        prereq_courses = Course.query.filter(Course.course_code.in_(prereq_codes)).all()
        return prereq_courses 