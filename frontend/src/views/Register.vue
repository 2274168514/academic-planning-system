<template>
  <div class="auth-page">
    <!-- 左侧图片区 -->
    <div class="auth-left">
      <img
        src="https://images.unsplash.com/photo-1481627834876-b7833e8f5570?auto=format&fit=crop&w=1200&q=80"
        class="auth-bg-img"
        alt=""
      />
      <div class="auth-left-overlay"></div>
      <div class="auth-left-content">
        <div class="auth-logo" @click="$router.push('/')">
          <span class="logo-mark">智</span>
          <span class="logo-name">学规划</span>
        </div>
        <div class="auth-left-text">
          <h2>开启你的<br/>智能学业之旅</h2>
          <p>注册即可免费使用 AI 学业规划、<br/>知识图谱探索与个性化课程推荐</p>
        </div>
      </div>
    </div>

    <!-- 右侧表单区 -->
    <div class="auth-right">
      <div class="auth-form-wrap">
        <div class="auth-back" @click="$router.push('/')">
          <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 10H5M10 4l-6 6 6 6"/></svg>
          返回首页
        </div>

        <div class="auth-form-header">
          <h1>创建账号</h1>
          <p>免费注册，立即使用全部功能</p>
        </div>

        <div class="auth-form">
          <div class="form-field">
            <label>用户名</label>
            <input v-model="username" type="text" placeholder="请设置用户名" />
          </div>
          <div class="form-field">
            <label>邮箱</label>
            <input v-model="email" type="email" placeholder="请输入邮箱地址" />
          </div>
          <div class="form-field">
            <label>密码</label>
            <input v-model="password" type="password" placeholder="请设置密码（至少6位）" />
          </div>
          <div class="form-field">
            <label>确认密码</label>
            <input v-model="confirmPassword" type="password" placeholder="请再次输入密码" @keyup.enter="register" />
          </div>
          <button class="btn-submit" @click="register" :disabled="loading">
            <span v-if="!loading">注 册</span>
            <span v-else>注册中...</span>
          </button>
          <p class="auth-switch">
            已有账号？
            <router-link to="/login">立即登录</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { userApi } from '../utils/api'
import { ElMessage } from 'element-plus'

export default {
  name: 'Register',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      loading: false
    }
  },
  methods: {
    async register() {
      if (!this.username || !this.email || !this.password) {
        ElMessage.warning('请填写完整信息')
        return
      }
      if (this.password !== this.confirmPassword) {
        ElMessage.warning('两次输入的密码不一致')
        return
      }
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailRegex.test(this.email)) {
        ElMessage.warning('请输入有效的邮箱地址')
        return
      }
      this.loading = true
      try {
        await userApi.register({ username: this.username, email: this.email, password: this.password })
        ElMessage.success('注册成功，请登录')
        this.$router.push('/login')
      } catch (error) {
        ElMessage.error(error.response?.data?.error || error.response?.data?.message || '注册失败，请稍后重试')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.auth-page {
  display: flex;
  height: 100vh;
  font-family: 'DM Sans', sans-serif;
}

.auth-left {
  flex: 1;
  position: relative;
  overflow: hidden;
}
.auth-bg-img {
  position: absolute; inset: 0;
  width: 100%; height: 100%;
  object-fit: cover;
  filter: brightness(0.45) saturate(1.3);
}
.auth-left-overlay {
  position: absolute; inset: 0;
  background: linear-gradient(160deg, rgba(10,12,26,0.9) 0%, rgba(10,12,26,0.6) 100%);
}
.auth-left-content {
  position: relative; z-index: 1;
  padding: 40px 48px;
  display: flex; flex-direction: column;
  justify-content: space-between; height: 100%;
}
.auth-logo {
  display: flex; align-items: center; gap: 10px;
  cursor: pointer; width: fit-content;
}
.logo-mark {
  width: 38px; height: 38px;
  background: #c9a84c; color: #0a0c1a;
  font-family: 'Playfair Display', serif;
  font-weight: 900; font-size: 20px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 8px;
}
.logo-name {
  font-family: 'Playfair Display', serif;
  font-size: 18px; font-weight: 700; color: #ffffff;
}
.auth-left-text { padding-bottom: 60px; }
.auth-left-text h2 {
  font-family: 'Playfair Display', serif;
  font-size: 36px; font-weight: 700;
  color: #ffffff; line-height: 1.3; margin-bottom: 16px;
}
.auth-left-text p {
  font-size: 15px; line-height: 1.75;
  color: rgba(255,255,255,0.65);
}

.auth-right {
  width: 500px;
  background: #faf8f4;
  display: flex; align-items: center; justify-content: center;
  padding: 40px;
  overflow-y: auto;
}
.auth-form-wrap { width: 100%; max-width: 380px; }
.auth-back {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 13px; color: #9a97b0;
  cursor: pointer; margin-bottom: 36px;
  transition: color 0.2s;
}
.auth-back:hover { color: #c9a84c; }
.auth-back svg { width: 16px; height: 16px; }

.auth-form-header { margin-bottom: 28px; }
.auth-form-header h1 {
  font-family: 'Playfair Display', serif;
  font-size: 30px; font-weight: 700;
  color: #1a1a2e; margin-bottom: 6px;
}
.auth-form-header p { font-size: 14px; color: #6b6b8a; }

.auth-form { display: flex; flex-direction: column; gap: 16px; }
.form-field { display: flex; flex-direction: column; gap: 7px; }
.form-field label { font-size: 13px; font-weight: 500; color: #4a4a6a; }
.form-field input {
  padding: 11px 14px;
  border: 1.5px solid #e0ddd5;
  border-radius: 8px;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px; color: #1a1a2e;
  background: #ffffff; outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.form-field input:focus {
  border-color: #c9a84c;
  box-shadow: 0 0 0 3px rgba(201,168,76,0.12);
}
.form-field input::placeholder { color: #b0adc5; }

.btn-submit {
  width: 100%; padding: 13px;
  background: #c9a84c; color: #0a0c1a;
  border: none; border-radius: 8px;
  font-family: 'DM Sans', sans-serif;
  font-size: 15px; font-weight: 500;
  cursor: pointer; margin-top: 4px;
  transition: background 0.2s, transform 0.15s, box-shadow 0.2s;
}
.btn-submit:hover:not(:disabled) {
  background: #e0bc66;
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(201,168,76,0.3);
}
.btn-submit:disabled { opacity: 0.65; cursor: not-allowed; }

.auth-switch {
  text-align: center; font-size: 13px; color: #6b6b8a;
}
.auth-switch a { color: #c9a84c; text-decoration: none; font-weight: 500; }
.auth-switch a:hover { text-decoration: underline; }

@media (max-width: 768px) {
  .auth-left { display: none; }
  .auth-right { width: 100%; padding: 32px 24px; }
}
</style>
