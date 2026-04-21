# 学习规划系统后端

## 配置说明

### 环境变量配置

系统使用环境变量进行配置，可以通过`.env`文件或者直接设置系统环境变量。

#### 创建.env文件

在backend目录下创建`.env`文件，内容如下：

```
# 基本配置
SECRET_KEY=development_secret_key
FLASK_ENV=development
PORT=5000

# JWT配置
JWT_SECRET_KEY=your_jwt_secret_key_here

# DeepSeek API配置
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions
DEEPSEEK_MODEL=deepseek-chat
```

### DeepSeek API配置

需要配置以下环境变量以连接DeepSeek API:

1. `DEEPSEEK_API_KEY`: 你的DeepSeek API密钥，通常以`sk-`开头
2. `DEEPSEEK_API_URL`: DeepSeek API的完整URL，包括端点
3. `DEEPSEEK_MODEL`: 要使用的模型名称

### 获取DeepSeek API密钥

要获取DeepSeek API密钥，请按照以下步骤操作：

1. 访问 [DeepSeek官网](https://deepseek.com/)
2. 注册/登录账号
3. 在账户设置或API部分找到并创建API密钥
4. 复制生成的密钥，它应该以`sk-`开头

### 验证配置

启动后端服务后，可以通过访问以下URL验证API配置：

```
http://localhost:5000/api/ai/status
```

此接口将返回API连接状态和任何需要解决的配置问题。

## 故障排除

如果AI助手无法正常工作，请检查：

1. 查看应用日志 (`backend/app.log`)
2. 确认DeepSeek API密钥是否有效
3. 检查网络连接是否能访问DeepSeek API
4. 验证API URL和模型名称是否正确

常见错误：
- "API请求失败"：通常表示API密钥无效或URL不正确
- "无法连接到服务器"：网络连接问题或API域名无法解析
- "模型不存在"：指定的模型名称错误

### 其他问题？

如有其他技术问题，请联系系统管理员。 