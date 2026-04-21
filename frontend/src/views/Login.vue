<template>
  <div class="login-container">
    <div class="login-box">
      <h2>学术规划系统</h2>
      <div class="login-form">
        <div class="form-item">
          <label>用户名</label>
          <input v-model="username" type="text" placeholder="请输入用户名" />
        </div>
        <div class="form-item">
          <label>密码</label>
          <input v-model="password" type="password" placeholder="请输入密码" />
        </div>
        <div class="form-actions">
          <button @click="login" class="btn-login" :disabled="loading">登 录</button>
          <router-link to="/register" class="link-register">没有账号？立即注册</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { userApi } from '../utils/api'
import { ElMessage } from 'element-plus'

export default {
  name: "Login",
  data() {
    return {
      username: '',
      password: '',
      loading: false
    }
  },
  methods: {
    async login() {
      // 表单验证
      if (!this.username || !this.password) {
        ElMessage.warning("用户名和密码不能为空");
        return;
      }
      
      this.loading = true;
      try {
        // 调用登录API
        const response = await userApi.login({
          username: this.username,
          password: this.password
        });
        
        // 保存登录状态
        this.$store.dispatch('login', {
          token: response.token,
          user: response.user
        });
        
        // 提示成功
        ElMessage.success("登录成功");
        
        // 获取重定向地址，如果没有则默认到首页
        const redirect = this.$route.query.redirect || '/';
        this.$router.push(redirect);
      } catch (error) {
        // 登录失败
        ElMessage.error(error.response?.data?.message || "登录失败，请检查用户名和密码");
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f2f5;
}

.login-box {
  width: 360px;
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

.login-form {
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

.btn-login {
  width: 100%;
  padding: 12px 0;
  background-color: #0066cc;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-login:hover {
  background-color: #0052a3;
}

.link-register {
  display: block;
  text-align: center;
  margin-top: 15px;
  color: #0066cc;
  text-decoration: none;
}
</style>
