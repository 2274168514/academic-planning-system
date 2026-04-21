import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

// 路由页面
const Login = () => import('../views/Login.vue')
const Register = () => import('../views/Register.vue')
const Layout = () => import('../views/layout/Layout.vue')
const Dashboard = () => import('../views/Dashboard.vue')
const Courses = () => import('../views/Courses.vue')
const CourseDetail = () => import('../views/CourseDetail.vue')
const KnowledgeGraph = () => import('../views/KnowledgeGraph.vue')
const CareerPath = () => import('../views/CareerPath.vue')
const AcademicPlanning = () => import('../views/AcademicPlanning.vue')
const AiAssistant = () => import('../views/AiAssistant.vue')
const LearningProgress = () => import('../views/LearningProgress.vue')
const UserProfile = () => import('../views/UserProfile.vue')

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: Layout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: Dashboard,
        meta: { title: '首页' }
      },
      {
        path: 'courses',
        name: 'Courses',
        component: Courses,
        meta: { title: '课程' }
      },
      {
        path: 'courses/:id',
        name: 'CourseDetail',
        component: CourseDetail,
        props: true,
        meta: { title: '课程详情' }
      },
      {
        path: 'knowledge-graph',
        name: 'KnowledgeGraph',
        component: KnowledgeGraph,
        meta: { title: '知识图谱' }
      },
      {
        path: 'career-path',
        name: 'CareerPath',
        component: CareerPath,
        meta: { title: '职业路径' }
      },
      {
        path: 'academic-planning',
        name: 'AcademicPlanning',
        component: AcademicPlanning,
        meta: { title: '学业规划' }
      },
      {
        path: 'ai-assistant',
        name: 'AiAssistant',
        component: AiAssistant,
        meta: { title: 'AI助手' }
      },
      {
        path: 'learning-progress',
        name: 'LearningProgress',
        component: LearningProgress,
        meta: { title: '学习进度' }
      },
      {
        path: 'profile',
        name: 'UserProfile',
        component: UserProfile,
        meta: { title: '个人中心' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 检查路由是否需要认证
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 检查是否已登录
    if (!store.getters.isLoggedIn) {
      // 未登录，重定向到登录页
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } else {
      // 已登录，继续
      next()
    }
  } else {
    // 不需要认证的路由，直接继续
    next()
  }
})

export default router 
 