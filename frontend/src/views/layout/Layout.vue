<template>
  <div class="layout-container">
    <div class="sidebar">
      <div class="logo">
        <el-icon class="logo-icon"><Collection /></el-icon>
        <span class="logo-text">学业规划</span>
      </div>
      <nav class="menu">
        <router-link to="/" class="menu-item" exact-active-class="active">
          <el-icon><House /></el-icon>
          <span>首页</span>
        </router-link>
        <router-link to="/courses" class="menu-item" active-class="active">
          <el-icon><Reading /></el-icon>
          <span>课程中心</span>
        </router-link>
        <router-link to="/knowledge-graph" class="menu-item" active-class="active">
          <el-icon><Share /></el-icon>
          <span>知识图谱</span>
        </router-link>
        <router-link to="/career-path" class="menu-item" active-class="active">
          <el-icon><Compass /></el-icon>
          <span>职业路径</span>
        </router-link>
        <router-link to="/academic-planning" class="menu-item" active-class="active">
          <el-icon><Calendar /></el-icon>
          <span>学业规划</span>
        </router-link>
        <router-link to="/ai-assistant" class="menu-item" active-class="active">
          <el-icon><ChatDotRound /></el-icon>
          <span>AI 助手</span>
        </router-link>
        <router-link to="/learning-progress" class="menu-item" active-class="active">
          <el-icon><TrendCharts /></el-icon>
          <span>学习进度</span>
        </router-link>
        <router-link to="/profile" class="menu-item" active-class="active">
          <el-icon><UserFilled /></el-icon>
          <span>个人中心</span>
        </router-link>
      </nav>
    </div>

    <div class="main-content">
      <header class="header">
        <div class="header-left">
          <span class="page-title">{{ getCurrentRouteName() }}</span>
        </div>
        <div class="header-right">
          <el-icon class="header-icon"><Bell /></el-icon>
          <div class="user-avatar">{{ avatarLetter }}</div>
          <el-dropdown @command="handleCommand">
            <div class="user-name-wrap">
              <span class="username">{{ username }}</span>
              <el-icon class="arrow-icon"><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人信息</el-dropdown-item>
                <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </header>

      <div class="content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import {
  House, Collection, Reading, Share, Compass,
  Calendar, ChatDotRound, TrendCharts, UserFilled,
  Bell, ArrowDown
} from '@element-plus/icons-vue'

export default {
  name: 'Layout',
  components: {
    House, Collection, Reading, Share, Compass,
    Calendar, ChatDotRound, TrendCharts, UserFilled,
    Bell, ArrowDown
  },
  data() {
    return {
      username: '学习者'
    }
  },
  computed: {
    ...mapGetters(['userInfo']),
    avatarLetter() {
      return this.username ? this.username[0].toUpperCase() : 'U'
    }
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
* { box-sizing: border-box; }

.layout-container {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

/* ── 侧边栏 ── */
.sidebar {
  width: 220px;
  background: #0f172a;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.logo {
  height: 64px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 20px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}

.logo-icon {
  font-size: 22px;
  color: #38bdf8;
}

.logo-text {
  font-size: 17px;
  font-weight: 700;
  color: #f1f5f9;
  letter-spacing: 0.5px;
}

.menu {
  flex: 1;
  padding: 12px 10px;
  display: flex;
  flex-direction: column;
  gap: 2px;
  overflow-y: auto;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 8px;
  color: rgba(255,255,255,0.5);
  text-decoration: none;
  font-size: 14px;
  transition: all 0.2s;
  border-left: 3px solid transparent;
}

.menu-item .el-icon {
  font-size: 17px;
  flex-shrink: 0;
}

.menu-item:hover {
  color: rgba(255,255,255,0.85);
  background: rgba(255,255,255,0.06);
}

.menu-item.active {
  color: #38bdf8;
  background: rgba(56,189,248,0.1);
  border-left-color: #38bdf8;
}

/* ── 主内容 ── */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #f1f5f9;
  overflow: hidden;
  min-width: 0;
}

/* ── 顶栏 ── */
.header {
  height: 64px;
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 28px;
  box-shadow: 0 1px 0 #e2e8f0;
  flex-shrink: 0;
}

.page-title {
  font-size: 16px;
  font-weight: 600;
  color: #0f172a;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-icon {
  font-size: 20px;
  color: #64748b;
  cursor: pointer;
  transition: color 0.2s;
}

.header-icon:hover {
  color: #0f172a;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #0ea5e9;
  color: white;
  font-size: 13px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-name-wrap {
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
}

.username {
  font-size: 14px;
  color: #374151;
  font-weight: 500;
}

.arrow-icon {
  font-size: 12px;
  color: #9ca3af;
}

/* ── 内容区 ── */
.content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

/* 响应式 */
@media (max-width: 768px) {
  .sidebar { width: 64px; }
  .menu-item span, .logo-text { display: none; }
  .logo { justify-content: center; padding: 0; }
  .menu-item { justify-content: center; border-left: none; border-radius: 8px; }
  .menu-item.active { border-left: none; }
}
</style>
