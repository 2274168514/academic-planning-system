from flask import Blueprint

api_bp = Blueprint('api', __name__)

from . import auth, users, courses, study_plans, learning_records, ai_assistant, knowledge_graph 