# Feature Completion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 完善学习进度图表、学业规划 CRUD、知识图谱可视化三个页面的功能。

**Architecture:** 学业规划页接真实后端 API（Flask `/api/study_plans`），学习进度和知识图谱使用 mock 数据渲染 ECharts 和 Vis.js 图表。先修正 api.js 的端点，再逐个实现三个页面。

**Tech Stack:** Vue 3 Composition API（Options API 风格）、Element Plus、ECharts 5、Vis.js vis-network 9

---

## 文件变更总览

| 文件 | 操作 | 职责 |
|------|------|------|
| `frontend/src/utils/api.js` | 修改 | 修正 planningApi 端点，使其与后端匹配 |
| `frontend/src/views/LearningProgress.vue` | 修改 | 实现 ECharts 时间柱状图和技能雷达图 |
| `frontend/src/views/AcademicPlanning.vue` | 修改 | 实现真实 CRUD：新建/删除计划，添加/移除课程 |
| `frontend/src/views/KnowledgeGraph.vue` | 重写 | 从零实现 Vis.js 知识图谱，mock 12 门课程数据 |

---

## Task 1: 修正 planningApi 端点

**Files:**
- Modify: `frontend/src/utils/api.js:69-73`

- [ ] **Step 1: 替换 planningApi 为正确端点**

将 `api.js` 中 `planningApi` 对象替换为：

```javascript
// 学业规划相关API
const planningApi = {
  getPlans: () => api.get('/study_plans'),
  createPlan: (data) => api.post('/study_plans', data),
  getPlan: (id) => api.get(`/study_plans/${id}`),
  deletePlan: (id) => api.delete(`/study_plans/${id}`),
  addDetail: (planId, data) => api.post(`/study_plans/${planId}/details`, data),
  removeDetail: (planId, detailId) => api.delete(`/study_plans/${planId}/details/${detailId}`)
}
```

- [ ] **Step 2: 验证文件保存正确**

打开 `frontend/src/utils/api.js`，确认 planningApi 的 6 个方法都存在，没有旧的 `getSemesterPlan`、`addCourseToSemester`、`removeCourse`。

- [ ] **Step 3: Commit**

```bash
cd E:\A课程\大创\DC
git add frontend/src/utils/api.js
git commit -m "fix: 修正 planningApi 端点与后端对齐"
```

---

## Task 2: 学习进度 ECharts 图表

**Files:**
- Modify: `frontend/src/views/LearningProgress.vue`

- [ ] **Step 1: 在 script 顶部引入 echarts**

在 `<script>` 标签内，`export default` 之前加入：

```javascript
import * as echarts from 'echarts'
```

- [ ] **Step 2: 在 data() 中添加图表实例变量**

在 `data()` 返回对象中，已有的字段之后追加：

```javascript
timeChartInstance: null,
skillRadarInstance: null,
weeklyStudyData: {
  week: [2.5, 3.0, 1.5, 4.0, 2.0, 3.5, 2.5],
  month: [18, 22, 15, 28, 20, 25, 19, 24, 16, 28, 21, 26, 18, 22, 17, 29, 23, 27, 20, 25, 18, 24, 16, 28, 21, 26, 19, 22, 17, 25],
  semester: [85, 92, 78, 96, 88, 94, 82, 90, 76, 95, 86, 91, 79, 97, 87]
},
```

- [ ] **Step 3: 替换 initCharts 方法**

将现有的 `initCharts()` 方法完全替换为：

```javascript
initCharts() {
  this.$nextTick(() => {
    this.initTimeChart()
    this.initSkillRadar()
  })
},

initTimeChart() {
  const el = this.$refs.timeChart
  if (!el) return
  if (this.timeChartInstance) this.timeChartInstance.dispose()
  this.timeChartInstance = echarts.init(el)
  this.renderTimeChart()
},

renderTimeChart() {
  const rangeMap = {
    week: { data: this.weeklyStudyData.week, labels: ['周一','周二','周三','周四','周五','周六','周日'] },
    month: { data: this.weeklyStudyData.month, labels: Array.from({length: 30}, (_, i) => `${i+1}日`) },
    semester: { data: this.weeklyStudyData.semester, labels: Array.from({length: 15}, (_, i) => `第${i+1}周`) }
  }
  const { data, labels } = rangeMap[this.selectedTimeRange] || rangeMap.week
  this.timeChartInstance.setOption({
    tooltip: { trigger: 'axis', formatter: '{b}: {c} 小时' },
    grid: { left: '10%', right: '5%', top: '10%', bottom: '15%' },
    xAxis: {
      type: 'category',
      data: labels,
      axisLabel: { fontSize: 11, color: '#666' }
    },
    yAxis: {
      type: 'value',
      name: '小时',
      nameTextStyle: { color: '#999', fontSize: 11 },
      axisLabel: { color: '#666' }
    },
    series: [{
      type: 'bar',
      data: data,
      barMaxWidth: 32,
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#409EFF' },
          { offset: 1, color: '#a0cfff' }
        ]),
        borderRadius: [4, 4, 0, 0]
      }
    }]
  })
},

initSkillRadar() {
  const el = this.$refs.skillRadar
  if (!el) return
  if (this.skillRadarInstance) this.skillRadarInstance.dispose()
  this.skillRadarInstance = echarts.init(el)
  this.skillRadarInstance.setOption({
    tooltip: {},
    legend: {
      data: ['当前水平', '目标水平'],
      bottom: 0,
      textStyle: { fontSize: 12, color: '#666' }
    },
    radar: {
      indicator: [
        { name: '编程能力', max: 100 },
        { name: '算法基础', max: 100 },
        { name: '系统知识', max: 100 },
        { name: '网络协议', max: 100 },
        { name: '数据库', max: 100 },
        { name: '软件工程', max: 100 }
      ],
      radius: '65%',
      splitNumber: 4,
      axisName: { color: '#555', fontSize: 12 },
      splitArea: { areaStyle: { color: ['rgba(64,158,255,0.02)', 'rgba(64,158,255,0.05)'] } }
    },
    series: [{
      type: 'radar',
      data: [
        {
          value: [80, 65, 70, 55, 75, 60],
          name: '当前水平',
          itemStyle: { color: '#409EFF' },
          areaStyle: { color: 'rgba(64,158,255,0.2)' },
          lineStyle: { width: 2 }
        },
        {
          value: [90, 85, 80, 80, 90, 80],
          name: '目标水平',
          itemStyle: { color: '#909399' },
          areaStyle: { color: 'rgba(144,147,153,0.1)' },
          lineStyle: { width: 2, type: 'dashed' }
        }
      ]
    }]
  })
},
```

- [ ] **Step 4: 添加 watch 和生命周期钩子**

在 `computed` 之后、`mounted` 之前添加 `watch`：

```javascript
watch: {
  selectedTimeRange() {
    if (this.timeChartInstance) this.renderTimeChart()
  }
},
```

将 `mounted()` 改为：

```javascript
mounted() {
  this.initCharts()
},
```

在 `methods` 同级添加 `beforeUnmount`：

```javascript
beforeUnmount() {
  if (this.timeChartInstance) this.timeChartInstance.dispose()
  if (this.skillRadarInstance) this.skillRadarInstance.dispose()
},
```

- [ ] **Step 5: 替换模板中的占位符 div**

将模板中的：
```html
<div class="time-chart" ref="timeChart">
  <!-- 这里将渲染学习时间图表 -->
  <div class="chart-placeholder">时间分布图表</div>
</div>
```
替换为：
```html
<div class="time-chart" ref="timeChart"></div>
```

将：
```html
<div class="skill-radar" ref="skillRadar">
  <!-- 这里将渲染技能雷达图 -->
  <div class="chart-placeholder">技能雷达图</div>
</div>
```
替换为：
```html
<div class="skill-radar" ref="skillRadar"></div>
```

- [ ] **Step 6: 在浏览器验证图表渲染**

打开 `http://localhost:8080`，登录后进入「学习进度」页面，确认：
- 时间图表显示蓝色柱状图（7根柱体）
- 技能雷达图显示六边形，有实线和虚线两层
- 切换「本周/本月/学期」下拉时时间图表数据更新

- [ ] **Step 7: Commit**

```bash
cd E:\A课程\大创\DC
git add frontend/src/views/LearningProgress.vue
git commit -m "feat: 实现学习进度 ECharts 时间图表和技能雷达图"
```

---

## Task 3: 学业规划 CRUD 接真实 API

**Files:**
- Modify: `frontend/src/views/AcademicPlanning.vue`

- [ ] **Step 1: 更新 script 引入**

在 `<script>` 标签内 `export default` 之前加入：

```javascript
import { planningApi, courseApi } from '@/utils/api'
```

- [ ] **Step 2: 重写 data() 中与学期规划相关的字段**

保留 `timeSlots`、`weekDays`、`scheduleData`、`degreeRequirements`、`recommendedActions`。

新增/替换以下字段：

```javascript
activeTab: 'semester',
// 计划管理
plans: [],
currentPlanId: null,
currentPlanDetails: [],
planLoading: false,
// 新建计划弹窗
showCreatePlanDialog: false,
createPlanForm: { plan_name: '', description: '' },
createPlanLoading: false,
// 添加课程弹窗
showAddCourseDialog: false,
addCourseForm: { course_id: null, semester: '', priority: 1 },
addCourseLoading: false,
allCourses: [],
```

- [ ] **Step 3: 重写 semester tab 的模板**

将 `<el-tab-pane name="semester" label="学期规划">` 内的全部内容替换为：

```html
<div class="semester-header">
  <div class="plan-selector">
    <el-select
      v-model="currentPlanId"
      placeholder="选择学习计划"
      style="width: 220px"
      @change="loadPlanDetails"
    >
      <el-option
        v-for="plan in plans"
        :key="plan.plan_id"
        :label="plan.plan_name"
        :value="plan.plan_id"
      />
    </el-select>
    <el-button
      v-if="currentPlanId"
      type="danger"
      plain
      size="small"
      style="margin-left: 8px"
      @click="confirmDeletePlan"
    >删除计划</el-button>
  </div>
  <div class="actions">
    <el-button type="primary" size="small" @click="openAddCourseDialog">添加课程</el-button>
    <el-button type="success" size="small" @click="showCreatePlanDialog = true">新建计划</el-button>
  </div>
</div>

<div v-if="!plans.length && !planLoading" class="empty-tip">
  <el-empty description="暂无学习计划，点击「新建计划」创建" />
</div>

<el-table
  v-if="currentPlanId"
  v-loading="planLoading"
  :data="currentPlanDetails"
  style="width: 100%"
  border
>
  <el-table-column prop="course.course_name" label="课程名称" />
  <el-table-column prop="course.course_type" label="类型" width="100" />
  <el-table-column prop="course.credit" label="学分" width="80" align="center" />
  <el-table-column prop="semester" label="学期" width="140" />
  <el-table-column prop="priority" label="优先级" width="90" align="center" />
  <el-table-column prop="status" label="状态" width="110">
    <template #default="scope">
      <el-tag :type="statusTagType(scope.row.status)" size="small">
        {{ statusLabel(scope.row.status) }}
      </el-tag>
    </template>
  </el-table-column>
  <el-table-column label="操作" width="90" align="center">
    <template #default="scope">
      <el-button type="text" size="small" class="danger-text" @click="removeDetail(scope.row)">移除</el-button>
    </template>
  </el-table-column>
</el-table>

<!-- 新建计划弹窗 -->
<el-dialog v-model="showCreatePlanDialog" title="新建学习计划" width="440px" @close="resetCreateForm">
  <el-form :model="createPlanForm" label-width="80px">
    <el-form-item label="计划名称">
      <el-input v-model="createPlanForm.plan_name" placeholder="请输入计划名称" />
    </el-form-item>
    <el-form-item label="描述">
      <el-input v-model="createPlanForm.description" type="textarea" :rows="3" placeholder="选填" />
    </el-form-item>
  </el-form>
  <template #footer>
    <el-button @click="showCreatePlanDialog = false">取消</el-button>
    <el-button type="primary" :loading="createPlanLoading" @click="submitCreatePlan">创建</el-button>
  </template>
</el-dialog>

<!-- 添加课程弹窗 -->
<el-dialog v-model="showAddCourseDialog" title="添加课程到计划" width="440px" @close="resetAddCourseForm">
  <el-form :model="addCourseForm" label-width="80px">
    <el-form-item label="课程">
      <el-select v-model="addCourseForm.course_id" placeholder="选择课程" style="width: 100%">
        <el-option
          v-for="c in allCourses"
          :key="c.course_id"
          :label="`${c.course_name}（${c.credit}学分）`"
          :value="c.course_id"
        />
      </el-select>
    </el-form-item>
    <el-form-item label="学期">
      <el-input v-model="addCourseForm.semester" placeholder="如：大二上学期" />
    </el-form-item>
    <el-form-item label="优先级">
      <el-input-number v-model="addCourseForm.priority" :min="1" :max="5" />
    </el-form-item>
  </el-form>
  <template #footer>
    <el-button @click="showAddCourseDialog = false">取消</el-button>
    <el-button type="primary" :loading="addCourseLoading" @click="submitAddCourse">添加</el-button>
  </template>
</el-dialog>
```

- [ ] **Step 4: 重写 methods**

将 methods 中的 `addCourse`、`switchSemester`、`viewCourseDetails`、`removeCourse`、`showCourseAt` 全部删除，替换为以下完整方法集（保留 `format`、`getProgressColor`、`hasCourse`、`getCourseAt`）：

```javascript
async loadPlans() {
  try {
    const res = await planningApi.getPlans()
    this.plans = res.study_plans || []
    if (this.plans.length && !this.currentPlanId) {
      this.currentPlanId = this.plans[0].plan_id
      await this.loadPlanDetails()
    }
  } catch (e) {
    this.$message.error('加载计划列表失败')
  }
},

async loadPlanDetails() {
  if (!this.currentPlanId) return
  this.planLoading = true
  try {
    const res = await planningApi.getPlan(this.currentPlanId)
    this.currentPlanDetails = res.details || []
  } catch (e) {
    this.$message.error('加载计划详情失败')
  } finally {
    this.planLoading = false
  }
},

async submitCreatePlan() {
  if (!this.createPlanForm.plan_name.trim()) {
    this.$message.warning('请输入计划名称')
    return
  }
  this.createPlanLoading = true
  try {
    const res = await planningApi.createPlan(this.createPlanForm)
    this.$message.success('创建成功')
    this.showCreatePlanDialog = false
    await this.loadPlans()
    this.currentPlanId = res.plan_id
    await this.loadPlanDetails()
  } catch (e) {
    this.$message.error('创建失败')
  } finally {
    this.createPlanLoading = false
  }
},

async confirmDeletePlan() {
  try {
    await this.$confirm('确定删除该计划吗？', '提示', {
      confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning'
    })
    await planningApi.deletePlan(this.currentPlanId)
    this.$message.success('删除成功')
    this.currentPlanId = null
    this.currentPlanDetails = []
    await this.loadPlans()
  } catch (e) {
    if (e !== 'cancel') this.$message.error('删除失败')
  }
},

async openAddCourseDialog() {
  if (!this.currentPlanId) {
    this.$message.warning('请先选择或创建一个计划')
    return
  }
  if (!this.allCourses.length) {
    try {
      const res = await courseApi.getCourses({ per_page: 100 })
      this.allCourses = res.courses || []
    } catch (e) {
      this.$message.error('加载课程列表失败')
      return
    }
  }
  this.showAddCourseDialog = true
},

async submitAddCourse() {
  if (!this.addCourseForm.course_id) {
    this.$message.warning('请选择课程')
    return
  }
  if (!this.addCourseForm.semester.trim()) {
    this.$message.warning('请填写学期')
    return
  }
  this.addCourseLoading = true
  try {
    await planningApi.addDetail(this.currentPlanId, this.addCourseForm)
    this.$message.success('添加成功')
    this.showAddCourseDialog = false
    await this.loadPlanDetails()
  } catch (e) {
    this.$message.error('添加失败')
  } finally {
    this.addCourseLoading = false
  }
},

async removeDetail(row) {
  try {
    await this.$confirm(`确定移除课程「${row.course.course_name}」吗？`, '提示', {
      confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning'
    })
    await planningApi.removeDetail(this.currentPlanId, row.detail_id)
    this.$message.success('已移除')
    await this.loadPlanDetails()
  } catch (e) {
    if (e !== 'cancel') this.$message.error('移除失败')
  }
},

resetCreateForm() {
  this.createPlanForm = { plan_name: '', description: '' }
},

resetAddCourseForm() {
  this.addCourseForm = { course_id: null, semester: '', priority: 1 }
},

statusTagType(status) {
  const map = { pending: 'info', in_progress: 'warning', completed: 'success' }
  return map[status] || 'info'
},

statusLabel(status) {
  const map = { pending: '待开始', in_progress: '进行中', completed: '已完成' }
  return map[status] || status
},
```

- [ ] **Step 5: 更新 mounted 调用 loadPlans**

将 `mounted()` 改为：

```javascript
mounted() {
  this.loadPlans()
},
```

- [ ] **Step 6: 确认后端 study_plans 接口响应格式**

在终端运行（后端需已启动，已登录拿到 token）：

```bash
curl -H "Authorization: Bearer <your_token>" http://localhost:5000/api/study_plans
```

确认响应包含 `study_plans` 数组，每个元素有 `plan_id`、`plan_name`。
GET `/api/study_plans/:id` 响应包含 `details` 数组，每个 detail 有 `detail_id`、`course`（含 `course_name`、`credit`、`course_type`）、`semester`、`priority`、`status`。

- [ ] **Step 7: 在浏览器验证学业规划页**

进入「学业规划」页面，确认：
- 已有计划加载到下拉框
- 切换计划时表格刷新
- 「新建计划」弹窗可提交，提交后列表更新
- 「添加课程」弹窗可选课程并提交
- 「移除」按钮删除一行后表格刷新
- 「删除计划」二次确认后计划消失

- [ ] **Step 8: Commit**

```bash
cd E:\A课程\大创\DC
git add frontend/src/views/AcademicPlanning.vue
git commit -m "feat: 学业规划 CRUD 接真实后端 API"
```

---

## Task 4: 知识图谱 Vis.js 实现

**Files:**
- Rewrite: `frontend/src/views/KnowledgeGraph.vue`

- [ ] **Step 1: 完整替换 KnowledgeGraph.vue**

用以下完整内容覆盖该文件：

```vue
<template>
  <div class="kg-container">
    <div class="kg-toolbar">
      <el-input
        v-model="searchText"
        placeholder="搜索课程..."
        clearable
        style="width: 240px"
        @input="onSearch"
        @clear="onSearch"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
      <div class="filter-btns">
        <el-button
          :type="filter === 'all' ? 'primary' : 'default'"
          size="small"
          @click="setFilter('all')"
        >全部</el-button>
        <el-button
          :type="filter === '必修' ? 'primary' : 'default'"
          size="small"
          @click="setFilter('必修')"
        >必修</el-button>
        <el-button
          :type="filter === '选修' ? 'primary' : 'default'"
          size="small"
          @click="setFilter('选修')"
        >选修</el-button>
      </div>
    </div>

    <div class="kg-body">
      <div class="kg-graph" ref="graphContainer"></div>
      <div v-if="selectedCourse" class="kg-detail">
        <div class="detail-header">
          <h3>{{ selectedCourse.label }}</h3>
          <el-tag :type="selectedCourse.course_type === '必修' ? 'primary' : 'success'" size="small">
            {{ selectedCourse.course_type }}
          </el-tag>
        </div>
        <div class="detail-item">
          <span class="detail-key">课程编号</span>
          <span class="detail-val">{{ selectedCourse.id }}</span>
        </div>
        <div class="detail-item">
          <span class="detail-key">学分</span>
          <span class="detail-val">{{ selectedCourse.credit }} 学分</span>
        </div>
        <div class="detail-item">
          <span class="detail-key">院系</span>
          <span class="detail-val">{{ selectedCourse.department }}</span>
        </div>
        <div class="detail-item description">
          <span class="detail-key">简介</span>
          <span class="detail-val">{{ selectedCourse.description }}</span>
        </div>
        <div v-if="selectedCourse.prerequisite" class="detail-item">
          <span class="detail-key">先修课程</span>
          <span class="detail-val">{{ getPrerequisiteNames(selectedCourse.prerequisite) }}</span>
        </div>
      </div>
      <div v-else class="kg-detail kg-detail--empty">
        <div class="empty-hint">点击节点查看课程详情</div>
      </div>
    </div>
  </div>
</template>

<script>
import { Network } from 'vis-network/standalone'
import { Search } from '@element-plus/icons-vue'

const COURSES = [
  { id: 'CS101', label: '计算机导论', credit: 3, course_type: '必修', department: '计算机科学与技术', prerequisite: '', description: '计算机科学的基础课程，介绍计算机的基本概念、原理和应用。' },
  { id: 'CS102', label: '程序设计基础', credit: 4, course_type: '必修', department: '计算机科学与技术', prerequisite: '', description: '介绍基本的程序设计概念和方法，使用C/C++语言。' },
  { id: 'CS201', label: '数据结构', credit: 4, course_type: '必修', department: '计算机科学与技术', prerequisite: 'CS102', description: '介绍基本的数据结构和算法，包括数组、链表、栈、队列、树、图等。' },
  { id: 'CS301', label: '算法设计与分析', credit: 3, course_type: '必修', department: '计算机科学与技术', prerequisite: 'CS201', description: '介绍常见的算法设计技术和分析方法，包括分治、动态规划、贪心等。' },
  { id: 'CS302', label: '操作系统', credit: 4, course_type: '必修', department: '计算机科学与技术', prerequisite: 'CS201', description: '介绍操作系统的基本概念、原理和实现方法。' },
  { id: 'CS303', label: '计算机网络', credit: 3, course_type: '必修', department: '计算机科学与技术', prerequisite: 'CS101', description: '介绍计算机网络的基本概念、原理和协议。' },
  { id: 'CS304', label: '数据库系统', credit: 4, course_type: '必修', department: '计算机科学与技术', prerequisite: 'CS201', description: '介绍数据库系统的基本概念、原理和实现方法。' },
  { id: 'CS401', label: '软件工程', credit: 3, course_type: '必修', department: '计算机科学与技术', prerequisite: 'CS304', description: '介绍软件开发的原则、方法和工具。' },
  { id: 'CS402', label: '人工智能', credit: 3, course_type: '选修', department: '计算机科学与技术', prerequisite: 'CS301', description: '介绍人工智能的基本概念、原理和应用。' },
  { id: 'CS403', label: '机器学习', credit: 3, course_type: '选修', department: '计算机科学与技术', prerequisite: 'CS402', description: '介绍机器学习的基本概念、原理和算法。' },
  { id: 'CS404', label: '深度学习', credit: 3, course_type: '选修', department: '计算机科学与技术', prerequisite: 'CS403', description: '介绍深度学习的基本概念、原理和模型。' },
  { id: 'CS405', label: '计算机图形学', credit: 3, course_type: '选修', department: '计算机科学与技术', prerequisite: 'CS201', description: '介绍计算机图形学的基本概念、原理和算法。' }
]

const EDGES = [
  { from: 'CS102', to: 'CS201' },
  { from: 'CS201', to: 'CS301' },
  { from: 'CS201', to: 'CS302' },
  { from: 'CS101', to: 'CS303' },
  { from: 'CS201', to: 'CS304' },
  { from: 'CS304', to: 'CS401' },
  { from: 'CS301', to: 'CS402' },
  { from: 'CS402', to: 'CS403' },
  { from: 'CS403', to: 'CS404' },
  { from: 'CS201', to: 'CS405' }
]

export default {
  name: 'KnowledgeGraph',
  components: { Search },
  data() {
    return {
      network: null,
      selectedCourse: null,
      searchText: '',
      filter: 'all'
    }
  },
  mounted() {
    this.$nextTick(() => this.initGraph())
  },
  beforeUnmount() {
    if (this.network) this.network.destroy()
  },
  methods: {
    getVisibleCourses() {
      if (this.filter === 'all') return COURSES
      return COURSES.filter(c => c.course_type === this.filter)
    },

    buildDataset(courses) {
      const ids = new Set(courses.map(c => c.id))
      const nodes = courses.map(c => ({
        id: c.id,
        label: c.label,
        color: {
          background: c.course_type === '必修' ? '#409EFF' : '#67C23A',
          border: c.course_type === '必修' ? '#2d7dd2' : '#4a9e57',
          highlight: { background: '#E6A23C', border: '#c07a1a' }
        },
        font: { color: '#fff', size: 13 },
        size: c.credit * 8,
        shape: 'circle',
        title: c.label,
        ...c
      }))
      const edges = EDGES
        .filter(e => ids.has(e.from) && ids.has(e.to))
        .map((e, i) => ({
          id: i,
          from: e.from,
          to: e.to,
          arrows: 'to',
          color: { color: '#aaa', highlight: '#E6A23C' },
          smooth: { type: 'curvedCW', roundness: 0.1 }
        }))
      return { nodes, edges }
    },

    initGraph() {
      const container = this.$refs.graphContainer
      if (!container) return
      const { nodes, edges } = this.buildDataset(this.getVisibleCourses())
      const options = {
        layout: {
          hierarchical: {
            direction: 'UD',
            sortMethod: 'directed',
            nodeSpacing: 120,
            levelSeparation: 100
          }
        },
        physics: { enabled: false },
        interaction: { hover: true, tooltipDelay: 200 },
        nodes: { borderWidth: 2 },
        edges: { width: 1.5 }
      }
      if (this.network) this.network.destroy()
      this.network = new Network(container, { nodes, edges }, options)
      this.network.on('click', params => {
        if (params.nodes.length) {
          const id = params.nodes[0]
          this.selectedCourse = COURSES.find(c => c.id === id) || null
        } else {
          this.selectedCourse = null
        }
      })
    },

    onSearch() {
      if (!this.network) return
      const q = this.searchText.trim().toLowerCase()
      const visible = this.getVisibleCourses()
      const updates = visible.map(c => {
        const match = !q || c.label.toLowerCase().includes(q) || c.id.toLowerCase().includes(q)
        return {
          id: c.id,
          color: match
            ? { background: c.course_type === '必修' ? '#409EFF' : '#67C23A', border: c.course_type === '必修' ? '#2d7dd2' : '#4a9e57' }
            : { background: '#ddd', border: '#bbb' },
          font: { color: match ? '#fff' : '#aaa' }
        }
      })
      this.network.body.data.nodes.update(updates)
    },

    setFilter(val) {
      this.filter = val
      this.selectedCourse = null
      this.searchText = ''
      this.initGraph()
    },

    getPrerequisiteNames(prerequisite) {
      if (!prerequisite) return '无'
      return prerequisite.split(',').map(code => {
        const c = COURSES.find(x => x.id === code.trim())
        return c ? c.label : code.trim()
      }).join('、')
    }
  }
}
</script>

<style scoped>
.kg-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 120px);
  padding: 20px;
}

.kg-toolbar {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.filter-btns {
  display: flex;
  gap: 8px;
}

.kg-body {
  display: flex;
  flex: 1;
  gap: 16px;
  min-height: 0;
}

.kg-graph {
  flex: 7;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  overflow: hidden;
}

.kg-detail {
  flex: 3;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  padding: 20px;
  overflow-y: auto;
}

.kg-detail--empty {
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-hint {
  color: #999;
  font-size: 14px;
}

.detail-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.detail-header h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.detail-item {
  display: flex;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px dashed #f0f0f0;
  font-size: 14px;
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-item.description {
  flex-direction: column;
  gap: 6px;
}

.detail-key {
  color: #999;
  min-width: 64px;
}

.detail-val {
  color: #333;
  flex: 1;
  line-height: 1.6;
}
</style>
```

- [ ] **Step 2: 在浏览器验证知识图谱页面**

进入「知识图谱」页面，确认：
- 图谱显示 12 个节点，蓝色必修、绿色选修
- 节点间有带箭头的连线表示先修关系
- 层次布局（基础课在上，高级课在下）
- 点击节点右侧显示课程详情面板
- 搜索框输入「数据」时，相关节点高亮，其余变灰
- 点击「必修」筛选按钮，只显示必修课节点和它们之间的连线

- [ ] **Step 3: Commit**

```bash
cd E:\A课程\大创\DC
git add frontend/src/views/KnowledgeGraph.vue
git commit -m "feat: 实现知识图谱 Vis.js 可视化，12门课程 mock 数据"
```

---

## Task 5: 推送到 GitHub

- [ ] **Step 1: 推送所有提交**

```bash
cd E:\A课程\大创\DC
git push origin master
```

- [ ] **Step 2: 确认 GitHub 上代码已更新**

访问 https://github.com/2274168514/academic-planning-system 确认最新提交显示。
