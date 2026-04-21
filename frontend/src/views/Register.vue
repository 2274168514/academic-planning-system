<template>
  <div class="register-container">
    <div class="register-box">
      <h2>用户注册</h2>
      <div class="register-form">
        <div class="form-item">
          <label>用户名</label>
          <input v-model="username" type="text" placeholder="请设置用户名" />
        </div>
        <div class="form-item">
          <label>邮箱</label>
          <input v-model="email" type="email" placeholder="请输入邮箱" />
        </div>
        <div class="form-item">
          <label>密码</label>
          <input v-model="password" type="password" placeholder="请设置密码" />
        </div>
        <div class="form-item">
          <label>确认密码</label>
          <input v-model="confirmPassword" type="password" placeholder="请再次输入密码" />
        </div>
        <div class="form-actions">
          <button @click="register" class="btn-register" :disabled="loading">注 册</button>
          <router-link to="/login" class="link-login">已有账号？返回登录</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { userApi } from '../utils/api'
import { ElMessage } from 'element-plus'

export default {
  name: "Register",
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
      // 表单验证
      if (!this.username || !this.email || !this.password) {
        ElMessage.warning("请填写完整信息");
        return;
      }
      
      if (this.password !== this.confirmPassword) {
        ElMessage.warning("两次输入的密码不一致");
        return;
      }
      
      // 简单验证邮箱格式
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(this.email)) {
        ElMessage.warning("请输入有效的邮箱地址");
        return;
      }
      
      this.loading = true;
      try {
        // 调用注册API
        await userApi.register({
          username: this.username,
          email: this.email,
          password: this.password
        });
        
        // 注册成功
        ElMessage.success("注册成功，请登录");
        this.$router.push('/login');
      } catch (error) {
        // 注册失败
        ElMessage.error(error.response?.data?.message || "注册失败，请稍后重试");
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f2f5;
}

.register-box {
  width: 400px;
  padding: 30px;
  background: white;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 24px;
  color: #0066cc;
}

.register-form {
  margin-top: 20px;
}

.form-item {
  margin-bottom: 20px;
}

.form-item label {
  display: block;
  margin-bottom: 5px;
}

.form-item input {
  width: 100%;
  padding: 10px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  box-sizing: border-box;
}

.form-actions {
  margin-top: 30px;
}

.btn-register {
  width: 100%;
  padding: 12px 0;
  background-color: #0066cc;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-register:hover {
  background-color: #0052a3;
}

.link-login {
  display: block;
  text-align: center;
  margin-top: 15px;
  color: #0066cc;
  text-decoration: none;
}
</style>
