import requests
import json
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

class AIService:
    """AI服务类，用于处理与DeepSeek API的交互"""

    def __init__(self):
        """初始化"""
        from flask import current_app
        # 从应用配置获取API设置
        self.api_key = current_app.config.get('DEEPSEEK_API_KEY')
        self.api_url = current_app.config.get('DEEPSEEK_API_URL')
        self.model_name = current_app.config.get('DEEPSEEK_MODEL')
        
        self.embeddings = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")
        self.vector_store = None
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        logging.info(f"AI服务初始化，API URL: {self.api_url}, 模型: {self.model_name}")

    def get_headers(self):
        """获取API请求头"""
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def chat_completion(self, messages, temperature=0.7, max_tokens=1000):
        """调用DeepSeek聊天接口
        
        Args:
            messages: 对话消息列表
            temperature: 温度参数
            max_tokens: 最大生成token数
            
        Returns:
            dict: API响应
        """
        if not self.api_key:
            logging.error("API密钥未配置")
            return {"error": "未配置DeepSeek API密钥"}
        
        # 构建请求数据
        data = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            # 添加日志以便调试
            logging.info(f"正在调用DeepSeek API: {self.api_url}")
            logging.info(f"请求头: {json.dumps({'Authorization': 'Bearer sk-***'})}")
            logging.info(f"请求数据: {json.dumps(data, ensure_ascii=False)}")
            
            # 发送请求到DeepSeek API
            response = requests.post(
                self.api_url, 
                headers=self.get_headers(), 
                json=data,
                timeout=30  # 设置30秒超时
            )
            
            # 记录响应状态和内容
            logging.info(f"API响应状态码: {response.status_code}")
            
            try:
                response_text = response.text
                response_json = response.json()
                logging.info(f"API响应内容: {json.dumps(response_json)[:200]}...")
            except:
                response_text = response.text
                logging.warning(f"API响应不是有效JSON: {response_text[:200]}...")
                return {"error": f"API返回无效JSON: {response_text[:100]}..."}
                
            if response.status_code != 200:
                logging.error(f"API请求失败: {response.status_code}, {response_text}")
                return {"error": f"API请求失败，状态码: {response.status_code}, 响应: {response_text[:100]}..."}
                
            return response_json
        except requests.exceptions.Timeout:
            logging.error("DeepSeek API请求超时")
            return {"error": "API请求超时，请稍后再试"}
        except requests.exceptions.ConnectionError as e:
            logging.error(f"DeepSeek API连接错误: {str(e)}")
            return {"error": f"无法连接到API服务器: {str(e)}"}
        except Exception as e:
            logging.error(f"DeepSeek API调用失败: {str(e)}")
            return {"error": f"API调用失败: {str(e)}"}
            
    def academic_planning_chat(self, user_message, chat_history=None):
        """学业规划聊天
        
        Args:
            user_message: 用户消息
            chat_history: 聊天历史记录
            
        Returns:
            str: AI响应
        """
        # 初始化系统提示
        system_message = {
            "role": "system", 
            "content": """你是一个专业的学业顾问和学习助手，专注于帮助大学生解决学习问题、规划学习路径。
            你应该：
            1. 提供准确、实用的学习建议
            2. 根据学生的专业和兴趣推荐适合的学习资源
            3. 帮助学生制定合理的学习计划
            4. 解答学生关于课程内容的疑问
            5. 给出提高学习效率的方法

            请保持回答简洁、专业、友好。如果问题超出你的知识范围，请诚实说明并提供相关建议。"""
        }
        
        # 构建消息列表
        messages = [system_message]
        
        # 添加聊天历史，确保格式正确
        if chat_history:
            for message in chat_history:
                role = message.get('role')
                content = message.get('content')
                if role and content and role in ['user', 'assistant', 'system']:
                    messages.append({"role": role, "content": content})
        
        # 添加用户消息
        messages.append({"role": "user", "content": user_message})
        
        # 调用API
        response = self.chat_completion(messages, temperature=0.7)
        
        # 提取回复
        if "error" in response:
            logging.error(f"处理DeepSeek响应出错: {response['error']}")
            return f"抱歉，出现了错误: {response['error']}"
            
        try:
            # 解析模型响应格式
            if 'choices' in response and len(response['choices']) > 0:
                message = response['choices'][0].get('message')
                if message and 'content' in message:
                    return message['content']
            
            # 如果响应格式不符合预期
            logging.warning(f"响应格式不符合预期: {json.dumps(response, ensure_ascii=False)}")
            return "抱歉，无法获取到有效回复，请稍后再试。"
        except (KeyError, IndexError) as e:
            logging.error(f"解析DeepSeek响应出错: {str(e)}")
            return "抱歉，无法获取到有效回复，请稍后再试。"
    
    def create_knowledge_base(self, documents):
        """创建知识库
        
        Args:
            documents: 文档列表
            
        Returns:
            bool: 是否成功
        """
        # 切分文档
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        texts = text_splitter.split_documents(documents)
        
        try:
            # 创建向量存储
            self.vector_store = FAISS.from_documents(texts, self.embeddings)
            return True
        except Exception as e:
            logging.error(f"创建知识库失败: {str(e)}")
            return False
    
    def rag_query(self, query, chat_history=None):
        """基于RAG的查询
        
        Args:
            query: 查询内容
            chat_history: 聊天历史
            
        Returns:
            str: 回答结果
        """
        if not self.vector_store:
            return "知识库尚未初始化"
        
        try:
            # 创建检索链
            retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
            
            # 使用简单的检索
            docs = retriever.get_relevant_documents(query)
            
            # 构建上下文
            context = "\n\n".join([doc.page_content for doc in docs])
            
            # 构造提示
            system_prompt = f"""请基于以下参考资料回答用户的问题。如果参考资料中没有相关信息，请明确告知用户你无法回答，不要编造信息。

参考资料:
{context}

请确保回答准确、相关且有用。"""
            
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # 添加历史对话
            if chat_history:
                messages.extend(chat_history)
            
            # 添加用户最新消息
            messages.append({"role": "user", "content": query})
            
            # 调用API
            response = self.chat_completion(messages)
            
            if "error" in response:
                return f"抱歉，服务出现了问题：{response['error']}"
            
            try:
                return response["choices"][0]["message"]["content"]
            except (KeyError, IndexError):
                return "抱歉，无法生成回复。"
                
        except Exception as e:
            logging.error(f"RAG查询失败: {str(e)}")
            return f"查询处理失败: {str(e)}"
    
    def generate_study_plan(self, major, interests, career_goals, current_semester=1):
        """生成学习计划
        
        Args:
            major: 专业
            interests: 兴趣
            career_goals: 职业目标
            current_semester: 当前学期
            
        Returns:
            dict: 学习计划
        """
        prompt = f"""请为一名{major}专业的大学生制定详细的学习计划。

学生信息:
- 专业: {major}
- 兴趣: {interests}
- 职业目标: {career_goals}
- 当前学期: {current_semester}

请提供以下内容:
1. 总体学习目标
2. 按学期划分的课程推荐（从当前学期开始）
3. 每个课程的学习要点
4. 额外的学习建议
5. 与职业目标相关的技能发展建议

请以结构化的JSON格式返回，格式如下:
{{
  "overall_goals": "总体学习目标",
  "semesters": [
    {{
      "semester": "学期号",
      "courses": [
        {{
          "name": "课程名称",
          "key_points": ["要点1", "要点2"],
          "credits": 学分数
        }}
      ]
    }}
  ],
  "additional_advice": "额外建议",
  "career_development": ["建议1", "建议2"]
}}

确保计划符合教育规律和专业课程体系，切实可行。"""
        
        messages = [
            {"role": "system", "content": "你是一个专业的学业规划顾问，擅长为大学生制定个性化学习计划。"},
            {"role": "user", "content": prompt}
        ]
        
        # 调用API
        response = self.chat_completion(messages, temperature=0.3, max_tokens=2000)
        
        if "error" in response:
            return {"error": response["error"]}
            
        try:
            content = response['choices'][0]['message']['content']
            # 提取JSON
            try:
                json_content = json.loads(content)
                return json_content
            except json.JSONDecodeError:
                # 如果不是有效JSON，尝试提取JSON部分
                import re
                json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
                if json_match:
                    try:
                        return json.loads(json_match.group(1))
                    except json.JSONDecodeError:
                        return {"error": "无法解析返回的JSON格式数据"}
                else:
                    return {"error": "无法提取返回的JSON格式数据"}
        except (KeyError, IndexError) as e:
            return {"error": f"解析DeepSeek响应出错: {str(e)}"}

    def test_connection(self):
        """测试与DeepSeek API的连接
        
        Returns:
            dict: 测试结果
        """
        try:
            # 简单的测试消息
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, are you working?"}
            ]
            
            # 输出详细配置信息
            logging.info(f"测试连接 - API URL: {self.api_url}")
            logging.info(f"测试连接 - 模型: {self.model_name}")
            logging.info(f"测试连接 - API密钥前缀: {self.api_key[:5]}...")
            
            # 设置较短的超时时间，避免长时间等待
            response = requests.post(
                self.api_url, 
                headers=self.get_headers(), 
                json={
                    "model": self.model_name,
                    "messages": messages,
                    "max_tokens": 10,  # 请求较少的token以加快响应
                    "temperature": 0.2
                },
                timeout=5  # 5秒超时
            )
            
            logging.info(f"测试连接 - 响应状态码: {response.status_code}")
            logging.info(f"测试连接 - 响应内容: {response.text[:200]}")
            
            if response.status_code == 200:
                return {
                    "status": "success",
                    "message": "API连接测试成功",
                    "details": response.text[:100]
                }
            else:
                return {
                    "status": "error",
                    "message": f"API连接测试失败，状态码: {response.status_code}",
                    "details": response.text
                }
        except requests.exceptions.Timeout:
            return {
                "status": "error",
                "message": "API请求超时，请检查网络连接"
            }
        except requests.exceptions.ConnectionError as e:
            return {
                "status": "error",
                "message": f"无法连接到API服务器: {str(e)}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"测试连接时发生错误: {str(e)}"
            } 