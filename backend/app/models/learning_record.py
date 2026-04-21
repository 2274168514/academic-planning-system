from .. import db
from datetime import datetime

class LearningRecord(db.Model):
    """学习记录模型"""
    __tablename__ = 'learning_records'
    
    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.now)
    finish_time = db.Column(db.DateTime, nullable=True)
    score = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(20), default='in_progress')  # in_progress, completed
    notes = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'record_id': self.record_id,
            'user_id': self.user_id,
            'course_id': self.course_id,
            'course': self.course.to_dict() if self.course else None,
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'finish_time': self.finish_time.strftime('%Y-%m-%d %H:%M:%S') if self.finish_time else None,
            'score': self.score,
            'status': self.status,
            'notes': self.notes
        }
    
    def complete(self, score=None):
        """完成学习"""
        self.status = 'completed'
        self.finish_time = datetime.now()
        if score is not None:
            self.score = score
        db.session.commit()
        
    @staticmethod
    def get_user_progress(user_id):
        """获取用户的学习进度统计"""
        from .course import Course
        
        total_courses = LearningRecord.query.filter_by(user_id=user_id).count()
        completed_courses = LearningRecord.query.filter_by(user_id=user_id, status='completed').count()
        
        # 按课程类型统计
        course_stats = {}
        records = LearningRecord.query.filter_by(user_id=user_id).all()
        for record in records:
            course = Course.query.get(record.course_id)
            if not course:
                continue
                
            course_type = course.course_type
            if course_type not in course_stats:
                course_stats[course_type] = {'total': 0, 'completed': 0}
            
            course_stats[course_type]['total'] += 1
            if record.status == 'completed':
                course_stats[course_type]['completed'] += 1
        
        return {
            'total_courses': total_courses,
            'completed_courses': completed_courses,
            'completion_rate': (completed_courses / total_courses * 100) if total_courses > 0 else 0,
            'course_stats': course_stats
        } 