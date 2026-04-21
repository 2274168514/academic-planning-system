from .. import db
from datetime import datetime
import bcrypt
from flask_jwt_extended import create_access_token

class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=True)
    major = db.Column(db.String(100), nullable=True)
    grade = db.Column(db.String(20), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    last_login_time = db.Column(db.DateTime, nullable=True)
    avatar = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    
    # 关系
    study_plans = db.relationship('StudyPlan', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    learning_records = db.relationship('LearningRecord', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        """设置密码，自动加密"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password):
        """验证密码"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def generate_auth_token(self):
        """生成JWT token"""
        return create_access_token(identity=self.user_id)
    
    def update_last_login(self):
        """更新最后登录时间"""
        self.last_login_time = datetime.now()
        db.session.commit()
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'major': self.major,
            'grade': self.grade,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None,
            'last_login_time': self.last_login_time.strftime('%Y-%m-%d %H:%M:%S') if self.last_login_time else None,
            'avatar': self.avatar
        } 