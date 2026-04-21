from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .config import config
import os

# 初始化数据库
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_name='default'):
    """
    工厂函数，创建应用实例
    :param config_name: 配置名称
    :return: 应用实例
    """
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
    jwt.init_app(app)
    
    # 注册蓝图
    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # 创建上传目录
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    # 注册错误处理
    register_error_handlers(app)
    
    return app

def register_error_handlers(app):
    """注册错误处理函数"""
    @app.errorhandler(404)
    def page_not_found(e):
        return {'error': 'Not Found'}, 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return {'error': 'Internal Server Error'}, 500 