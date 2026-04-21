#!/bin/bash

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# 输出标题函数
function print_header() {
    echo -e "\n${YELLOW}$1${NC}"
}

print_header "学业规划系统后端安装脚本"
print_header "==================================="

# 检查Python是否安装
if command -v python3 &>/dev/null; then
    echo -e "${GREEN}Python已安装: $(python3 --version)${NC}"
else
    echo -e "${RED}未找到Python3，请先安装Python 3.8+${NC}"
    exit 1
fi

# 检查pip是否安装
if command -v pip3 &>/dev/null; then
    echo -e "${GREEN}pip已安装: $(pip3 --version)${NC}"
else
    echo -e "${RED}未找到pip3，请先安装pip${NC}"
    exit 1
fi

# 创建虚拟环境
print_header "创建Python虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 安装依赖
print_header "安装Python依赖..."
pip3 install --upgrade pip
pip3 install -r requirements.txt

# 创建配置文件
print_header "创建配置文件..."
if [ ! -f .env ]; then
    cat > .env << EOF
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URI=mysql+pymysql://username:password@localhost/academic_planning
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
DEEPSEEK_API_KEY=your_api_key
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(16))')
EOF
    echo -e "${GREEN}配置文件.env已创建，请根据实际情况修改配置${NC}"
else
    echo -e "${YELLOW}配置文件.env已存在，跳过创建${NC}"
fi

# 创建上传目录
print_header "创建上传目录..."
mkdir -p uploads

print_header "后端环境设置完成!"
echo -e "${GREEN}请根据实际情况修改.env配置文件${NC}"
echo -e "${YELLOW}确保MySQL和Neo4j数据库已正确配置${NC}"
echo -e "${YELLOW}初始化数据库请运行: python scripts/init_db.py${NC}"
echo -e "${YELLOW}初始化知识图谱请运行: python scripts/init_kg.py${NC}"
echo -e "${YELLOW}启动后端服务请运行: flask run --host=0.0.0.0 --port=5000${NC}" 