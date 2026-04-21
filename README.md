# 大学生学业规划系统

基于知识图谱的大学生学业规划平台，结合人工智能问答和数据可视化技术，为用户提供个性化的学习规划方案和知识结构展示。

## 技术栈

- **前端**：Vue.js 3、Element Plus、ECharts、Vis.js
- **后端**：Python 3.8+、Flask、Flask-RESTful
- **数据库**：MySQL 8.0+、Neo4j 4.4+
- **AI引擎**：基于微调的DeepSeek API
- **检索增强生成(RAG)**：LangChain框架

## 项目结构

```
academic_planning_system/
├── backend/                    # 后端代码
│   ├── app/                    # Flask应用
│   │   ├── __init__.py         # 应用初始化
│   │   ├── config.py           # 配置文件
│   │   ├── models/             # 数据模型
│   │   ├── api/                # API接口
│   │   ├── services/           # 业务逻辑
│   │   ├── utils/              # 工具函数
│   │   └── knowledge_graph/    # 知识图谱相关
│   ├── migrations/             # 数据库迁移
│   ├── requirements.txt        # 依赖包
│   ├── run.py                  # 启动脚本
│   └── tests/                  # 测试代码
├── frontend/                   # 前端代码
│   ├── public/                 # 静态资源
│   ├── src/                    # 源代码
│   │   ├── assets/             # 图片等资源
│   │   ├── components/         # 通用组件
│   │   ├── views/              # 页面组件
│   │   ├── router/             # 路由配置
│   │   ├── store/              # 状态管理
│   │   ├── api/                # API调用
│   │   ├── utils/              # 工具函数
│   │   ├── App.vue             # 主组件
│   │   └── main.js             # 入口文件
│   ├── package.json            # 依赖配置
│   └── vue.config.js           # Vue配置
├── docker/                     # Docker配置
│   ├── docker-compose.yml      # 容器编排
│   ├── Dockerfile.backend      # 后端Dockerfile
│   └── Dockerfile.frontend     # 前端Dockerfile
├── scripts/                    # 脚本文件
│   ├── setup.sh                # 安装脚本
│   ├── init_db.py              # 数据库初始化
│   └── init_kg.py              # 知识图谱初始化
└── README.md                   # 项目说明
```

## 快速开始

### 环境要求

- Python 3.8+
- Node.js 14+
- MySQL 8.0+
- Neo4j 4.4+
- Docker & Docker Compose (可选)

### 方法一：本地开发环境

1. **克隆项目**

```bash
git clone https://github.com/2274168514/academic-planning-system.git
cd academic-planning-system
```

2. **后端配置**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

创建配置文件 `.env`：

```
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URI=mysql+pymysql://username:password@localhost/academic_planning
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
DEEPSEEK_API_KEY=your_api_key
SECRET_KEY=your_secret_key
```

3. **初始化数据库**

```bash
python scripts/init_db.py  # 初始化MySQL数据库
python scripts/init_kg.py  # 初始化Neo4j知识图谱
```

4. **启动后端**

```bash
flask run --host=0.0.0.0 --port=5000
```

5. **前端配置**

```bash
cd ../frontend
npm install
```

6. **启动前端**

```bash
npm run serve
```

访问 `http://localhost:8080` 即可打开应用。

### 方法二：Docker部署

1. **创建项目目录并下载代码**

```bash
mkdir academic-planning-system
cd academic-planning-system
# 下载项目文件 (或者使用git clone)
```

2. **配置环境变量**

创建 `.env` 文件：

```
MYSQL_ROOT_PASSWORD=rootpassword
MYSQL_DATABASE=academic_planning
MYSQL_USER=username
MYSQL_PASSWORD=password
NEO4J_AUTH=neo4j/password
DEEPSEEK_API_KEY=your_api_key
SECRET_KEY=your_secret_key
```

3. **启动Docker容器**

```bash
docker-compose up -d
```

访问 `http://localhost:8080` 即可打开应用。

## 功能模块

- 用户认证：注册、登录、密码重置
- 学业规划：个性化学习计划制定、学期课程安排
- 知识图谱：课程知识图谱可视化、知识点关联展示
- AI问答：基于RAG的智能问答、学业规划咨询
- 学习资源：课程资料推荐、优质学习材料分享
- 学习进度：课程学习进度监控、学习效果评估
- 社区交流：学习经验分享、学习伙伴匹配
- 数据分析：学习数据可视化、能力评估报告

## 许可证

MIT 