<template>
  <div class="profile-container">
    <h1 class="page-title">个人中心</h1>
    
    <div class="profile-content">
      <div class="profile-left">
        <div class="user-card">
          <div class="avatar-container">
            <img src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png" class="user-avatar" />
            <div class="change-avatar">
              <i class="el-icon-camera"></i>
            </div>
          </div>
          <h2 class="user-name">张三</h2>
          <p class="user-role">计算机科学专业</p>
          <p class="user-id">学号: 2023102445</p>
          <div class="user-stat">
            <div class="stat-item">
              <div class="stat-value">8</div>
              <div class="stat-label">课程</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">36</div>
              <div class="stat-label">技能</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">85%</div>
              <div class="stat-label">完成率</div>
            </div>
          </div>
        </div>
        
        <div class="achievement-section">
          <h3 class="section-title">
            <i class="el-icon-trophy"></i>
            成就徽章
          </h3>
          <div class="badge-list">
            <div class="badge-item">
              <div class="badge-icon gold">
                <i class="el-icon-star-on"></i>
              </div>
              <div class="badge-name">学习达人</div>
            </div>
            <div class="badge-item">
              <div class="badge-icon silver">
                <i class="el-icon-time"></i>
              </div>
              <div class="badge-name">坚持不懈</div>
            </div>
            <div class="badge-item">
              <div class="badge-icon bronze">
                <i class="el-icon-medal"></i>
              </div>
              <div class="badge-name">助人为乐</div>
            </div>
            <div class="badge-item locked">
              <div class="badge-icon">
                <i class="el-icon-lock"></i>
              </div>
              <div class="badge-name">未解锁</div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="profile-right">
        <el-tabs v-model="activeTab" class="profile-tabs">
          <el-tab-pane label="基本信息" name="basic">
            <el-form :model="userInfo" label-width="100px">
              <el-form-item label="姓名">
                <el-input v-model="userInfo.name" placeholder="请输入姓名"></el-input>
              </el-form-item>
              <el-form-item label="学号">
                <el-input v-model="userInfo.studentId" placeholder="请输入学号" disabled></el-input>
              </el-form-item>
              <el-form-item label="邮箱">
                <el-input v-model="userInfo.email" placeholder="请输入邮箱"></el-input>
              </el-form-item>
              <el-form-item label="手机号">
                <el-input v-model="userInfo.phone" placeholder="请输入手机号"></el-input>
              </el-form-item>
              <el-form-item label="专业">
                <el-select v-model="userInfo.major" placeholder="请选择专业">
                  <el-option label="计算机科学与技术" value="计算机科学与技术"></el-option>
                  <el-option label="软件工程" value="软件工程"></el-option>
                  <el-option label="人工智能" value="人工智能"></el-option>
                  <el-option label="数据科学" value="数据科学"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="年级">
                <el-select v-model="userInfo.grade" placeholder="请选择年级">
                  <el-option label="大一" value="大一"></el-option>
                  <el-option label="大二" value="大二"></el-option>
                  <el-option label="大三" value="大三"></el-option>
                  <el-option label="大四" value="大四"></el-option>
                  <el-option label="研一" value="研一"></el-option>
                  <el-option label="研二" value="研二"></el-option>
                  <el-option label="研三" value="研三"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="个人简介">
                <el-input type="textarea" v-model="userInfo.bio" rows="4" placeholder="请输入个人简介"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary">保存修改</el-button>
                <el-button>取消</el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
          
          <el-tab-pane label="学习统计" name="statistics">
            <div class="stat-grid">
              <div class="stat-box">
                <h4>学习时长</h4>
                <div class="stat-chart">图表占位</div>
              </div>
              <div class="stat-box">
                <h4>知识覆盖</h4>
                <div class="stat-chart">图表占位</div>
              </div>
              <div class="stat-box">
                <h4>学习活跃度</h4>
                <div class="stat-chart">图表占位</div>
              </div>
              <div class="stat-box">
                <h4>技能雷达</h4>
                <div class="stat-chart">图表占位</div>
              </div>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="账号安全" name="security">
            <div class="security-item">
              <div class="security-info">
                <h4>修改密码</h4>
                <p>定期修改密码有助于保障账号安全</p>
              </div>
              <el-button size="small">修改密码</el-button>
            </div>
            
            <div class="security-item">
              <div class="security-info">
                <h4>绑定手机</h4>
                <p>已绑定：138****6789</p>
              </div>
              <el-button size="small">修改绑定</el-button>
            </div>
            
            <div class="security-item">
              <div class="security-info">
                <h4>绑定邮箱</h4>
                <p>已绑定：exa****@example.com</p>
              </div>
              <el-button size="small">修改绑定</el-button>
            </div>
            
            <div class="security-item">
              <div class="security-info">
                <h4>登录设备管理</h4>
                <p>查看和管理您的登录设备</p>
              </div>
              <el-button size="small">查看设备</el-button>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "UserProfile",
  data() {
    return {
      activeTab: 'basic',
      userInfo: {
        name: '张三',
        studentId: '2023102445',
        email: 'example@example.com',
        phone: '13812345678',
        major: '计算机科学与技术',
        grade: '大三',
        bio: '热爱学习和探索新知识，对人工智能和数据科学特别感兴趣。'
      }
    }
  },
  methods: {
    // 可添加相关方法
  }
}
</script>

<style scoped>
.profile-container {
  padding: 20px;
}

.page-title {
  margin-bottom: 24px;
  font-size: 24px;
  color: #333;
}

.profile-content {
  display: flex;
  gap: 20px;
}

.profile-left {
  width: 300px;
}

.profile-right {
  flex: 1;
}

.user-card {
  background: white;
  border-radius: 8px;
  padding: 30px 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  text-align: center;
  margin-bottom: 20px;
}

.avatar-container {
  position: relative;
  width: 100px;
  height: 100px;
  margin: 0 auto 20px;
}

.user-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
}

.change-avatar {
  position: absolute;
  right: 0;
  bottom: 0;
  width: 32px;
  height: 32px;
  background: #409EFF;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.user-name {
  margin: 0 0 5px;
  font-size: 18px;
  font-weight: 600;
}

.user-role {
  color: #666;
  margin: 0 0 5px;
}

.user-id {
  color: #999;
  margin: 0 0 15px;
  font-size: 12px;
}

.user-stat {
  display: flex;
  border-top: 1px solid #f0f0f0;
  padding-top: 15px;
}

.stat-item {
  flex: 1;
}

.stat-value {
  font-size: 20px;
  font-weight: 600;
  color: #333;
}

.stat-label {
  font-size: 12px;
  color: #666;
}

.achievement-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.section-title {
  display: flex;
  align-items: center;
  font-size: 16px;
  margin-top: 0;
  margin-bottom: 15px;
  color: #333;
}

.section-title i {
  margin-right: 8px;
  color: #faad14;
}

.badge-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.badge-item {
  text-align: center;
}

.badge-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 8px;
  font-size: 20px;
}

.badge-icon.gold {
  background: linear-gradient(45deg, #FFD700, #FFA500);
  color: white;
}

.badge-icon.silver {
  background: linear-gradient(45deg, #C0C0C0, #A9A9A9);
  color: white;
}

.badge-icon.bronze {
  background: linear-gradient(45deg, #CD7F32, #A0522D);
  color: white;
}

.badge-name {
  font-size: 12px;
}

.badge-item.locked {
  opacity: 0.5;
}

.profile-tabs {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.stat-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.stat-box {
  background: #f9f9f9;
  border-radius: 4px;
  padding: 15px;
}

.stat-box h4 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 16px;
  color: #333;
}

.stat-chart {
  height: 200px;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
}

.security-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid #f0f0f0;
}

.security-item:last-child {
  border-bottom: none;
}

.security-info h4 {
  margin: 0 0 5px;
  font-size: 16px;
}

.security-info p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

/* 响应式布局 */
@media (max-width: 992px) {
  .profile-content {
    flex-direction: column;
  }
  
  .profile-left {
    width: 100%;
  }
  
  .badge-list {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 768px) {
  .stat-grid {
    grid-template-columns: 1fr;
  }
  
  .badge-list {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
