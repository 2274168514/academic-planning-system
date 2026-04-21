import axios from 'axios'

const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:5000/api'

const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器添加token
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, error => {
  return Promise.reject(error)
})

// 响应拦截器处理错误
api.interceptors.response.use(response => {
  return response.data
}, error => {
  if (error.response) {
    // 处理服务器返回的错误
    switch (error.response.status) {
      case 401:
        // 未授权，跳转到登录页
        window.location.href = '/login'
        break
      case 403:
        // 权限不足
        console.error('没有权限访问此资源')
        break
      case 500:
        // 服务器错误
        console.error('服务器错误')
        break
      default:
        console.error(error.response.data.message || '请求失败')
    }
  } else {
    // 网络错误
    console.error('网络错误，请检查您的网络连接')
  }
  return Promise.reject(error)
})

// 用户相关API
const userApi = {
  login: (data) => api.post('/auth/login', data),
  register: (data) => api.post('/auth/register', data),
  getProfile: () => api.get('/users/profile'),
  updateProfile: (data) => api.put('/users/profile', data)
}

// 课程相关API
const courseApi = {
  getCourses: (params) => api.get('/courses', { params }),
  getCourseById: (id) => api.get(`/courses/${id}`),
  enrollCourse: (id) => api.post(`/courses/${id}/enroll`)
}

// 学业规划相关API
const planningApi = {
  getSemesterPlan: (semesterId) => api.get(`/planning/semester/${semesterId}`),
  addCourseToSemester: (semesterId, data) => api.post(`/planning/semester/${semesterId}/courses`, data),
  removeCourse: (semesterId, courseId) => api.delete(`/planning/semester/${semesterId}/courses/${courseId}`)
}

// 学习进度相关API
const progressApi = {
  getProgress: () => api.get('/progress'),
  getProgressByCourse: (courseId) => api.get(`/progress/courses/${courseId}`)
}

// 知识图谱相关API
const knowledgeApi = {
  getGraph: (params) => api.get('/knowledge-graph', { params })
}

// AI助手相关API
const aiApi = {
  checkStatus: () => api.get('/ai/status'),
  chat: (data) => api.post('/ai/chat', data),
  generateStudyPlan: (data) => api.post('/ai/study_plan', data),
  recommendCourses: (params) => api.get('/ai/recommend_courses', { params }),
  recommendNextCourses: (params) => api.get('/ai/recommend_next_courses', { params }),
  recommendStudyPlan: (params) => api.get('/ai/recommend_study_plan', { params })
}

export {
  userApi,
  courseApi,
  planningApi,
  progressApi,
  knowledgeApi,
  aiApi
}

export default api 