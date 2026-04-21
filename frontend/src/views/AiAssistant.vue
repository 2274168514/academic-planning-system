<template>
  <div class="ai-assistant-container">
    <h1 class="page-title">AI学习助手</h1>
    
    <div class="api-status" v-if="serviceStatus !== 'ok'">
      <div v-if="serviceStatus === 'checking'" class="status-checking">
        <i class="el-icon-loading"></i> 正在检查AI助手服务状态...
      </div>
      <div v-if="serviceStatus === 'error'" class="status-error">
        <i class="el-icon-warning"></i> AI助手服务异常，请联系管理员
        <el-button type="text" @click="retryConnection" size="small">重试连接</el-button>
      </div>
      <div v-if="serviceStatus === 'warning'" class="status-warning">
        <i class="el-icon-warning"></i> AI助手服务存在潜在问题，功能可能受限
      </div>
    </div>
    
    <div class="assistant-content">
      <div class="chat-panel">
        <div class="chat-header">
          <div class="assistant-info">
            <div class="assistant-avatar">
              <img src="https://via.placeholder.com/40" alt="AI助手" />
            </div>
            <div class="assistant-name">DeepSeek学习顾问 <span class="status-badge online">在线</span></div>
          </div>
          <div class="assistant-actions">
            <el-dropdown>
              <el-button type="text" icon="el-icon-more"></el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="clearChat">清空对话</el-dropdown-item>
                  <el-dropdown-item>导出记录</el-dropdown-item>
                  <el-dropdown-item>助手设置</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
        
        <div class="chat-body" ref="chatContainer">
          <div class="chat-welcome" v-if="messages.length <= 1">
            <div class="welcome-icon">
              <i class="el-icon-s-opportunity"></i>
            </div>
            <h2>欢迎使用DeepSeek AI学习助手</h2>
            <p>我可以帮助你解答学习中的问题、推荐学习资料、制定学习计划等</p>
          </div>
          
          <div class="chat-messages">
            <div v-for="(message, index) in messages" :key="index" 
              :class="['message', message.from === 'ai' ? 'ai-message' : 'user-message']">
              <div class="message-avatar">
                <img 
                  :src="message.from === 'ai' ? 'https://via.placeholder.com/32' : 'https://via.placeholder.com/32?text=U'" 
                  :alt="message.from === 'ai' ? 'AI' : '用户'" 
                />
              </div>
              <div class="message-content">
                <div class="message-text" v-html="formatMessage(message.text)"></div>
                <div class="message-time">{{ message.time }}</div>
              </div>
            </div>
            
            <div v-if="thinking" class="message ai-message thinking">
              <div class="message-avatar">
                <img src="https://via.placeholder.com/32" alt="AI" />
              </div>
              <div class="message-content">
                <div class="thinking-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="chat-footer">
          <div class="suggestion-chips" v-if="suggestions.length > 0">
            <div 
              v-for="(suggestion, index) in suggestions" 
              :key="index" 
              class="suggestion-chip"
              @click="selectSuggestion(suggestion)"
            >
              {{ suggestion }}
            </div>
          </div>
          
          <div class="message-input-container">
            <el-input
              type="textarea"
              :rows="2"
              v-model="userInput"
              placeholder="输入你的问题..."
              :disabled="thinking"
              auto-complete="off"
              @keyup.enter.native="sendMessage"
            ></el-input>
            
            <div class="input-actions">
              <el-button type="primary" icon="el-icon-s-promotion" :disabled="thinking || !userInput.trim()" @click="sendMessage">发送</el-button>
            </div>
          </div>
        </div>
      </div>
      
      <div class="resource-panel">
        <div class="panel-section">
          <div class="section-header">
            <h3>常见问题</h3>
            <el-button type="text">查看全部</el-button>
          </div>
          <div class="faq-list">
            <div v-for="(faq, index) in faqs" :key="index" class="faq-item" @click="askFaq(faq.question)">
              <div class="faq-question">{{ faq.question }}</div>
              <div class="faq-meta">{{ faq.category }}</div>
            </div>
          </div>
        </div>
        
        <div class="panel-section">
          <div class="section-header">
            <h3>相关资源</h3>
          </div>
          <div class="resource-list">
            <div v-for="(resource, index) in relatedResources" :key="index" class="resource-item">
              <div class="resource-icon" :class="resource.type">
                <i :class="getResourceIcon(resource.type)"></i>
              </div>
              <div class="resource-info">
                <div class="resource-title">{{ resource.title }}</div>
                <div class="resource-meta">{{ resource.source }}</div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="panel-section">
          <div class="section-header">
            <h3>我的历史会话</h3>
          </div>
          <div class="history-list">
            <div v-for="(history, index) in chatHistory" :key="index" class="history-item">
              <div class="history-title">{{ history.title }}</div>
              <div class="history-meta">
                <span>{{ history.date }}</span>
                <span>{{ history.messageCount }}条消息</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { aiApi } from '../utils/api'
import { ElMessage } from 'element-plus'

export default {
  name: "AiAssistant",
  data() {
    return {
      userInput: '',
      thinking: false,
      messages: [
        {
          from: 'ai',
          text: '你好！我是DeepSeek学习助手，有什么我可以帮助你的？你可以问我关于课程内容的问题，或者需要制定学习计划、推荐学习资料等。',
          time: this.formatTime(new Date())
        }
      ],
      suggestions: [
        '如何提高学习效率？',
        '帮我推荐数据结构的学习资料',
        '我需要一个计算机网络的学习计划',
        '解释一下TCP/IP协议'
      ],
      faqs: [
        { question: '如何选择合适的选修课？', category: '学业规划' },
        { question: '如何准备期末考试？', category: '学习方法' },
        { question: '如何平衡学习和生活？', category: '时间管理' },
        { question: '如何提高编程能力？', category: '技能提升' }
      ],
      relatedResources: [
        { type: 'document', title: '高效学习方法指南', source: '学习中心' },
        { type: 'video', title: '数据结构与算法入门', source: '计算机科学课程' },
        { type: 'course', title: '计算机网络原理', source: '推荐课程' },
        { type: 'article', title: '如何准备技术面试', source: '职业规划' }
      ],
      chatHistory: [
        { title: '学习计划制定', date: '2023-05-10', messageCount: 12 },
        { title: '数据结构问题解答', date: '2023-05-08', messageCount: 8 },
        { title: '算法复杂度分析', date: '2023-05-05', messageCount: 15 }
      ],
      serviceStatus: 'checking'
    }
  },
  mounted() {
    this.scrollToBottom();
    this.checkAiServiceStatus();
  },
  updated() {
    this.scrollToBottom();
  },
  methods: {
    async sendMessage() {
      if (!this.userInput.trim() || this.thinking) return;
      
      // 检查服务状态
      if (this.serviceStatus === 'error') {
        ElMessage.warning('AI助手服务当前不可用，请稍后再试');
        return;
      }
      
      // 添加用户消息
      this.messages.push({
        from: 'user',
        text: this.userInput,
        time: this.formatTime(new Date())
      });
      
      const question = this.userInput;
      this.userInput = '';
      this.thinking = true;
      
      // 最大重试次数
      const maxRetries = 2;
      let retries = 0;
      let success = false;
      
      while (retries <= maxRetries && !success) {
        try {
          // 准备聊天历史
          const chatHistory = this.messages
            .filter(m => m.from !== 'system')
            .map(m => ({
              content: m.text,
              role: m.from === 'ai' ? 'assistant' : 'user'
            }));
          
          // 调用后端API
          const response = await aiApi.chat({
            message: question,
            chat_history: chatHistory.slice(0, -1) // 不包括刚刚添加的消息
          });
          
          // 添加AI回复
          this.thinking = false;
          
          if (response.error) {
            throw new Error(response.error);
          }
          
          this.messages.push({
            from: 'ai',
            text: response.response || '抱歉，我无法理解您的问题，请尝试重新表述。',
            time: this.formatTime(new Date())
          });
          
          // 更新建议问题
          this.updateSuggestions(question);
          success = true;
        } catch (error) {
          retries++;
          console.error(`AI响应错误(尝试${retries}/${maxRetries}):`, error);
          
          // 最后一次尝试失败才显示错误
          if (retries > maxRetries) {
            this.thinking = false;
            
            // 添加错误消息
            this.messages.push({
              from: 'ai',
              text: '抱歉，服务出现了问题，请稍后再试。',
              time: this.formatTime(new Date())
            });
            
            let errorMsg = '无法连接到AI助手，请稍后再试';
            if (error.response && error.response.data && error.response.data.error) {
              errorMsg = `连接错误: ${error.response.data.error}`;
            }
            
            ElMessage.error(errorMsg);
            
            // 服务可能有问题，重新检查状态
            this.checkAiServiceStatus();
          } else {
            // 等待一段时间后重试
            await new Promise(resolve => setTimeout(resolve, 1000));
          }
        }
      }
    },
    
    clearChat() {
      this.messages = [{
        from: 'ai',
        text: '你好！我是DeepSeek学习助手，有什么我可以帮助你的？',
        time: this.formatTime(new Date())
      }];
      this.suggestions = [
        '如何提高学习效率？',
        '帮我推荐数据结构的学习资料',
        '我需要一个计算机网络的学习计划',
        '解释一下TCP/IP协议'
      ];
    },
    
    formatTime(date) {
      const hours = date.getHours().toString().padStart(2, '0');
      const minutes = date.getMinutes().toString().padStart(2, '0');
      return `${hours}:${minutes}`;
    },
    
    scrollToBottom() {
      if (this.$refs.chatContainer) {
        this.$nextTick(() => {
          this.$refs.chatContainer.scrollTop = this.$refs.chatContainer.scrollHeight;
        });
      }
    },
    
    formatMessage(text) {
      // 简单的消息格式化，支持基本HTML
      return text;
    },
    
    updateSuggestions(question) {
      // 根据当前对话内容更新建议问题
      if (question.includes('学习效率')) {
        this.suggestions = [
          '如何运用番茄工作法？',
          '有什么好的记忆方法？',
          '如何保持专注力？',
          '如何制定学习计划？'
        ];
      } else if (question.includes('数据结构')) {
        this.suggestions = [
          '如何学习算法复杂度分析？',
          '树结构有哪些应用场景？',
          '如何准备数据结构的考试？',
          '有哪些数据结构的练习题？'
        ];
      } else if (question.includes('学习计划')) {
        this.suggestions = [
          '如何安排复习时间？',
          '怎样跟踪学习进度？',
          '如何处理学习中的困难？',
          '有什么好的学习资源推荐？'
        ];
      } else if (question.includes('TCP/IP') || question.includes('协议')) {
        this.suggestions = [
          '三次握手和四次挥手的过程是什么？',
          'TCP和UDP有什么区别？',
          'HTTP协议的工作原理是什么？',
          '网络安全有哪些常见问题？'
        ];
      }
    },
    
    selectSuggestion(suggestion) {
      this.userInput = suggestion;
      this.sendMessage();
    },
    
    askFaq(question) {
      this.userInput = question;
      this.sendMessage();
    },
    
    getResourceIcon(type) {
      const icons = {
        'document': 'el-icon-document',
        'video': 'el-icon-video-camera',
        'course': 'el-icon-reading',
        'article': 'el-icon-edit-outline'
      };
      return icons[type] || 'el-icon-document';
    },
    
    // 检查AI服务状态
    async checkAiServiceStatus() {
      try {
        const response = await aiApi.checkStatus();
        if (response.status === 'error') {
          ElMessage.error(`AI助手服务错误: ${response.message}`);
          this.serviceStatus = 'error';
        } else if (response.status === 'warning') {
          ElMessage.warning(`AI助手服务警告: ${response.message}`);
          this.serviceStatus = 'warning';
        } else {
          console.log('AI助手服务正常');
          this.serviceStatus = 'ok';
        }
      } catch (error) {
        console.error('检查AI服务状态失败:', error);
        ElMessage.error('无法连接到AI助手服务，请检查网络连接或联系管理员');
        this.serviceStatus = 'error';
      }
    },
    
    // 重试连接
    async retryConnection() {
      this.serviceStatus = 'checking';
      await this.checkAiServiceStatus();
    }
  }
}
</script>

<style scoped>
.ai-assistant-container {
  padding: 20px;
}

.page-title {
  margin-bottom: 24px;
  font-size: 24px;
  color: #333;
}

.assistant-content {
  display: flex;
  gap: 20px;
  height: calc(100vh - 160px);
}

.chat-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.resource-panel {
  width: 300px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  overflow-y: auto;
}

.chat-header {
  padding: 15px 20px;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.assistant-info {
  display: flex;
  align-items: center;
}

.assistant-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 12px;
}

.assistant-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.assistant-name {
  font-size: 16px;
  font-weight: 600;
}

.status-badge {
  display: inline-block;
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 10px;
  margin-left: 8px;
  font-weight: normal;
}

.status-badge.online {
  background-color: #67C23A;
  color: white;
}

.chat-body {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.chat-welcome {
  text-align: center;
  padding: 30px 0;
}

.welcome-icon {
  font-size: 48px;
  color: #409EFF;
  margin-bottom: 15px;
}

.chat-welcome h2 {
  font-size: 20px;
  margin-bottom: 10px;
}

.chat-welcome p {
  color: #666;
  max-width: 400px;
  margin: 0 auto;
}

.chat-messages {
  margin-top: 20px;
}

.message {
  display: flex;
  margin-bottom: 20px;
}

.message-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 12px;
  flex-shrink: 0;
}

.message-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.message-content {
  max-width: 70%;
}

.ai-message .message-content {
  background-color: #f5f7fa;
  border-radius: 0 8px 8px 8px;
  padding: 12px 16px;
}

.user-message {
  flex-direction: row-reverse;
}

.user-message .message-avatar {
  margin-right: 0;
  margin-left: 12px;
}

.user-message .message-content {
  background-color: #ecf5ff;
  border-radius: 8px 0 8px 8px;
  padding: 12px 16px;
}

.message-text {
  color: #333;
  word-break: break-word;
}

.message-time {
  font-size: 12px;
  color: #999;
  margin-top: 6px;
  text-align: right;
}

/* 思考中动画 */
.thinking-indicator {
  display: flex;
  align-items: center;
  padding: 10px;
}

.thinking-indicator span {
  display: inline-block;
  width: 8px;
  height: 8px;
  margin: 0 2px;
  background-color: #ccc;
  border-radius: 50%;
  animation: thinking 1.4s infinite ease-in-out both;
}

.thinking-indicator span:nth-child(1) {
  animation-delay: -0.32s;
}

.thinking-indicator span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes thinking {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

.chat-footer {
  padding: 15px;
  border-top: 1px solid #f0f0f0;
}

.suggestion-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 10px;
}

.suggestion-chip {
  background-color: #f0f7ff;
  color: #409EFF;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.suggestion-chip:hover {
  background-color: #ecf5ff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.message-input-container {
  display: flex;
  gap: 10px;
}

.message-input-container .el-input {
  flex: 1;
}

.input-actions {
  display: flex;
  align-items: flex-end;
}

/* 资源面板样式 */
.panel-section {
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
}

.panel-section:last-child {
  border-bottom: none;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.section-header h3 {
  font-size: 16px;
  margin: 0;
  color: #333;
}

.faq-list, .resource-list, .history-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.faq-item, .resource-item, .history-item {
  padding: 10px;
  border-radius: 4px;
  background-color: #f5f7fa;
  cursor: pointer;
  transition: all 0.3s;
}

.faq-item:hover, .resource-item:hover, .history-item:hover {
  background-color: #ecf5ff;
}

.faq-question, .resource-title, .history-title {
  font-size: 14px;
  margin-bottom: 5px;
  color: #333;
}

.faq-meta, .resource-meta, .history-meta {
  font-size: 12px;
  color: #999;
}

.history-meta {
  display: flex;
  justify-content: space-between;
}

.resource-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.resource-icon {
  width: 32px;
  height: 32px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: white;
}

.resource-icon.document {
  background-color: #67C23A;
}

.resource-icon.video {
  background-color: #E6A23C;
}

.resource-icon.course {
  background-color: #409EFF;
}

.resource-icon.article {
  background-color: #F56C6C;
}

.resource-info {
  flex: 1;
}

/* 响应式调整 */
@media (max-width: 1200px) {
  .resource-panel {
    width: 250px;
  }
}

@media (max-width: 992px) {
  .assistant-content {
    flex-direction: column;
    height: auto;
  }
  
  .chat-panel {
    height: 60vh;
  }
  
  .resource-panel {
    width: 100%;
    height: auto;
  }
}

.api-status {
  padding: 10px;
  margin-bottom: 15px;
  border-radius: 4px;
  text-align: center;
}

.status-checking {
  background-color: #E6F7FF;
  color: #1890ff;
}

.status-error {
  background-color: #FFF2F0;
  color: #ff4d4f;
}

.status-warning {
  background-color: #FFFBE6;
  color: #faad14;
}
</style>
