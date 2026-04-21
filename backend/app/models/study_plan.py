from .. import db
from datetime import datetime

class StudyPlan(db.Model):
    """学习计划模型"""
    __tablename__ = 'study_plans'
    
    plan_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    plan_name = db.Column(db.String(100), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    plan_status = db.Column(db.String(20), default='active')  # active, archived, deleted
    description = db.Column(db.Text, nullable=True)
    
    # 关系
    details = db.relationship('PlanDetail', backref='plan', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'plan_id': self.plan_id,
            'user_id': self.user_id,
            'plan_name': self.plan_name,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S'),
            'plan_status': self.plan_status,
            'description': self.description
        }
    
    def to_dict_with_details(self):
        """转换为带详情的字典格式"""
        plan_dict = self.to_dict()
        plan_dict['details'] = [detail.to_dict() for detail in self.details.order_by(PlanDetail.semester)]
        return plan_dict


class PlanDetail(db.Model):
    """计划详情模型"""
    __tablename__ = 'plan_details'
    
    detail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('study_plans.plan_id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    priority = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'detail_id': self.detail_id,
            'plan_id': self.plan_id,
            'course_id': self.course_id,
            'course': self.course.to_dict() if self.course else None,
            'semester': self.semester,
            'priority': self.priority,
            'status': self.status
        } 