<template>
  <div class="layout-container">
    <div class="sidebar">
      <div class="logo">
        <h2>学习助手</h2>
      </div>
      <div class="menu">
        <router-link to="/" class="menu-item" exact>
          <i class="el-icon-s-home"></i>
          <span>首页</span>
        </router-link>
        <router-link to="/courses" class="menu-item">
          <i class="el-icon-reading"></i>
          <span>课程</span>
        </router-link>
        <router-link to="/knowledge-graph" class="menu-item">
          <i class="el-icon-share"></i>
          <span>知识图谱</span>
        </router-link>
        <router-link to="/career-path" class="menu-item">
          <i class="el-icon-guide"></i>
          <span>职业路径</span>
        </router-link>
        <router-link to="/academic-planning" class="menu-item">
          <i class="el-icon-s-order"></i>
          <span>学业规划</span>
        </router-link>
        <router-link to="/ai-assistant" class="menu-item">
          <i class="el-icon-s-opportunity"></i>
          <span>AI助手</span>
        </router-link>
        <router-link to="/learning-progress" class="menu-item">
          <i class="el-icon-data-line"></i>
          <span>学习进度</span>
        </router-link>
        <router-link to="/profile" class="menu-item">
          <i class="el-icon-user"></i>
          <span>个人中心</span>
        </router-link>
      </div>
    </div>
    <div class="main-content">
      <div class="header">
        <div class="header-left">
          <i class="el-icon-menu toggle-sidebar"></i>
          <div class="breadcrumb">{{getCurrentRouteName()}}</div>
        </div>
        <div class="header-right">
          <div class="user-info">
            <i class="el-icon-bell notification-icon"></i>
            <span class="username">{{username}}</span>
            <el-dropdown @command="handleCommand">
              <span class="el-dropdown-link">
                <i class="el-icon-arrow-down"></i>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">个人信息</el-dropdown-item>
                  <el-dropdown-item command="settings">设置</el-dropdown-item>
                  <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </div>
      <div class="content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: "Layout",
  data() {
    return {
      username: '学习者'
    }
  },
  computed: {
    ...mapGetters(['userInfo'])
  },
  methods: {
    getCurrentRouteName() {
      return this.$route.meta.title || '首页'
    },
    handleCommand(command) {
      if (command === 'logout') {
        this.$store.dispatch('logout')
        this.$router.push('/login')
      } else if (command === 'profile') {
        this.$router.push('/profile')
      }
    }
  }
}
</script>

<style scoped>
.layout-container {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  width: 240px;
  background-color: #304156;
  color: white;
  height: 100%;
  display: flex;
  flex-direction: column;
  transition: width 0.3s;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.menu {
  flex: 1;
  padding: 15px 0;
  overflow-y: auto;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  transition: all 0.3s;
}

.menu-item i {
  margin-right: 10px;
  font-size: 18px;
}

.menu-item:hover, .menu-item.router-link-active {
  background-color: #263445;
  color: #409EFF;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #f0f2f5;
  overflow: hidden;
}

.header {
  height: 60px;
  background-color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
}

.header-left {
  display: flex;
  align-items: center;
}

.toggle-sidebar {
  font-size: 20px;
  margin-right: 20px;
  cursor: pointer;
}

.breadcrumb {
  font-size: 16px;
  font-weight: 500;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
}

.notification-icon {
  font-size: 18px;
  margin-right: 20px;
  cursor: pointer;
}

.username {
  margin-right: 8px;
}

.el-dropdown-link {
  cursor: pointer;
}

.content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

/* 响应式布局 */
@media (max-width: 768px) {
  .sidebar {
    width: 64px;
  }
  
  .menu-item span {
    display: none;
  }
  
  .logo h2 {
    display: none;
  }
}
</style>
