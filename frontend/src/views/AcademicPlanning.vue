<template>
  <div class="academic-planning-container">
    <h1 class="page-title">学业规划</h1>
    
    <div class="planning-content">
      <div class="planning-tabs">
        <el-tabs v-model="activeTab" type="border-card">
          <el-tab-pane name="semester" label="学期规划">
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
          </el-tab-pane>
          
          <el-tab-pane name="degree" label="学位要求">
            <div class="degree-progress">
              <el-progress :percentage="53" :format="format" :stroke-width="18"></el-progress>
              <div class="progress-text">您已完成学位要求的53%，预计毕业时间：2025年6月</div>
            </div>
            
            <div class="requirement-categories">
              <div v-for="(category, index) in degreeRequirements" :key="index" class="requirement-card">
                <div class="card-header">
                  <h3>{{category.name}}</h3>
                  <div class="progress-info">
                    {{category.completed}}/{{category.required}} {{category.unit}}
                  </div>
                </div>
                <el-progress 
                  :percentage="Math.min(100, (category.completed/category.required) * 100)" 
                  :color="getProgressColor(category.completed/category.required)"
                  :show-text="false"
                ></el-progress>
                <div class="requirement-items">
                  <div v-for="(item, i) in category.items" :key="i" class="requirement-item">
                    <div :class="['status-dot', item.status]"></div>
                    <div class="item-detail">
                      <div class="item-name">{{item.name}}</div>
                      <div class="item-progress">{{item.note}}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </el-tab-pane>
          
          <el-tab-pane name="graduation" label="毕业审计">
            <div class="audit-summary">
              <div class="audit-status">
                <i class="el-icon-warning-outline"></i>
                <div class="text">
                  <div class="title">毕业审计结果</div>
                  <div class="description">您还有部分要求未满足，请查看以下详情</div>
                </div>
              </div>
              
              <div class="checklist">
                <div class="checklist-item complete">
                  <i class="el-icon-check"></i>
                  <span>总学分要求 (已修满86学分，还需74学分)</span>
                </div>
                <div class="checklist-item incomplete">
                  <i class="el-icon-close"></i>
                  <span>核心课程要求 (缺少《软件工程》、《计算机网络》)</span>
                </div>
                <div class="checklist-item complete">
                  <i class="el-icon-check"></i>
                  <span>通识教育要求 (已完成所有通识课程)</span>
                </div>
                <div class="checklist-item incomplete">
                  <i class="el-icon-close"></i>
                  <span>专业选修课要求 (需要额外选修12学分专业课)</span>
                </div>
                <div class="checklist-item incomplete">
                  <i class="el-icon-close"></i>
                  <span>毕业设计/论文 (尚未开始)</span>
                </div>
              </div>
            </div>
            
            <div class="recommendation">
              <h3>推荐行动</h3>
              <div class="action-cards">
                <div class="action-card" v-for="(action, index) in recommendedActions" :key="index">
                  <div class="icon" :style="{ backgroundColor: action.color }">
                    <i :class="action.icon"></i>
                  </div>
                  <div class="content">
                    <div class="title">{{action.title}}</div>
                    <div class="description">{{action.description}}</div>
                    <el-button type="text" class="action-btn">{{action.action}}</el-button>
                  </div>
                </div>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
  </div>
</template>

<script>
import { planningApi, courseApi } from '@/utils/api'

export default {
  name: "AcademicPlanning",
  data() {
    return {
      activeTab: 'semester',
      plans: [],
      currentPlanId: null,
      currentPlanDetails: [],
      planLoading: false,
      showCreatePlanDialog: false,
      createPlanForm: { plan_name: '', description: '' },
      createPlanLoading: false,
      showAddCourseDialog: false,
      addCourseForm: { course_id: null, semester: '', priority: 1 },
      addCourseLoading: false,
      allCourses: [],
      timeSlots: [
        { id: 1, slot: '1-2', time: '8:00-9:40' },
        { id: 2, slot: '3-4', time: '10:00-11:40' },
        { id: 3, slot: '5-6', time: '13:30-15:10' },
        { id: 4, slot: '7-8', time: '15:30-17:10' },
        { id: 5, slot: '9-10', time: '18:30-20:10' }
      ],
      weekDays: [
        { id: 1, name: '周一' },
        { id: 2, name: '周二' },
        { id: 3, name: '周三' },
        { id: 4, name: '周四' },
        { id: 5, name: '周五' }
      ],
      scheduleData: [
        { day: 1, time: 1, course: { name: '数据库原理', location: '教学楼A302' } },
        { day: 1, time: 3, course: { name: '人工智能导论', location: '教学楼B201' } },
        { day: 2, time: 2, course: { name: '概率论与数理统计', location: '理科楼C305' } },
        { day: 3, time: 1, course: { name: '软件工程', location: '教学楼A405' } },
        { day: 4, time: 4, course: { name: '中国近代史纲要', location: '人文楼D102' } },
        { day: 5, time: 2, course: { name: '数据库原理', location: '教学楼A302' } }
      ],
      degreeRequirements: [
        { 
          name: '专业必修课', 
          required: 60, 
          completed: 32, 
          unit: '学分',
          items: [
            { name: '计算机导论', status: 'completed', note: '4学分，已完成' },
            { name: '程序设计基础', status: 'completed', note: '4学分，已完成' },
            { name: '数据结构', status: 'completed', note: '4学分，已完成' },
            { name: '数据库原理', status: 'in-progress', note: '4学分，进行中' },
            { name: '软件工程', status: 'in-progress', note: '3学分，进行中' },
            { name: '计算机网络', status: 'planned', note: '下学期计划修读' },
            { name: '操作系统', status: 'not-started', note: '尚未开始' }
          ]
        },
        { 
          name: '专业选修课', 
          required: 24, 
          completed: 9, 
          unit: '学分',
          items: [
            { name: '机器学习', status: 'completed', note: '3学分，已完成' },
            { name: '计算机图形学', status: 'completed', note: '3学分，已完成' },
            { name: '人工智能导论', status: 'in-progress', note: '3学分，进行中' },
            { name: '高级数据库技术', status: 'planned', note: '下学期计划修读' }
          ]
        },
        { 
          name: '通识教育', 
          required: 36, 
          completed: 28, 
          unit: '学分',
          items: [
            { name: '大学英语', status: 'completed', note: '8学分，已完成' },
            { name: '高等数学', status: 'completed', note: '10学分，已完成' },
            { name: '中国近代史纲要', status: 'in-progress', note: '2学分，进行中' },
            { name: '创新创业基础', status: 'planned', note: '下学期计划修读' }
          ]
        },
        { 
          name: '实践环节', 
          required: 40, 
          completed: 17, 
          unit: '学分',
          items: [
            { name: '程序设计实验', status: 'completed', note: '4学分，已完成' },
            { name: '数据结构实验', status: 'completed', note: '3学分，已完成' },
            { name: '专业实习', status: 'planned', note: '计划大四完成' },
            { name: '毕业设计', status: 'not-started', note: '大四进行' }
          ]
        }
      ],
      recommendedActions: [
        {
          title: '选修软件工程实践',
          description: '建议下学期选修，可满足实践环节学分要求',
          action: '查看课程详情',
          icon: 'el-icon-s-cooperation',
          color: '#409EFF'
        },
        {
          title: '准备专业实习',
          description: '建议提前半年准备，联系相关企业',
          action: '浏览实习机会',
          icon: 'el-icon-office-building',
          color: '#67C23A'
        },
        {
          title: '补修专业核心课',
          description: '计算机网络为必修课，需优先安排',
          action: '加入选课计划',
          icon: 'el-icon-reading',
          color: '#E6A23C'
        }
      ]
    }
  },
  mounted() {
    this.loadPlans()
  },
  methods: {
    format(percentage) {
      return `${percentage}%`;
    },
    getProgressColor(ratio) {
      if (ratio >= 1) return '#67C23A';
      if (ratio >= 0.6) return '#409EFF';
      if (ratio >= 0.3) return '#E6A23C';
      return '#F56C6C';
    },
    hasCourse(day, time) {
      return this.scheduleData.some(item => item.day === day && item.time === time);
    },
    getCourseAt(day, time) {
      const found = this.scheduleData.find(item => item.day === day && item.time === time);
      return found ? found.course : null;
    },
    async loadPlans() {
      try {
        const res = await planningApi.getPlans()
        this.plans = res.plans || []
        if (this.plans.length && !this.currentPlanId) {
          this.currentPlanId = this.plans[0].plan_id
          try {
            await this.loadPlanDetails()
          } catch (e) {
            this.$message.error('加载计划详情失败')
          }
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
        this.currentPlanDetails = (res.plan && res.plan.details) || []
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
        this.currentPlanId = res.plan.plan_id
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
  }
}
</script>

<style scoped>
.academic-planning-container {
  padding: 20px;
}

.page-title {
  margin-bottom: 24px;
  font-size: 24px;
  color: #333;
}

.planning-content {
  background: white;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.semester-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.semester-header h3 {
  margin: 0;
}

.plan-selector {
  display: flex;
  align-items: center;
}

.empty-tip {
  padding: 40px 0;
}

.actions {
  display: flex;
  gap: 10px;
}

.credit-summary {
  display: flex;
  margin-bottom: 20px;
  background: #f9f9f9;
  border-radius: 4px;
  padding: 15px;
}

.summary-item {
  flex: 1;
  text-align: center;
  border-right: 1px solid #eee;
}

.summary-item:last-child {
  border-right: none;
}

.summary-item .label {
  color: #666;
  font-size: 14px;
  margin-bottom: 5px;
}

.summary-item .value {
  font-size: 20px;
  font-weight: 600;
  color: #333;
}

.danger-text {
  color: #F56C6C;
}

.schedule-view {
  margin-top: 30px;
}

.schedule-view h3 {
  margin-bottom: 15px;
}

.weekly-schedule {
  display: flex;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  overflow: hidden;
}

.time-column, .day-column {
  display: flex;
  flex-direction: column;
}

.time-column {
  width: 100px;
  background: #f5f7fa;
}

.day-column {
  flex: 1;
  min-width: 120px;
}

.header-cell {
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  border-bottom: 1px solid #ebeef5;
  background: #f5f7fa;
}

.time-cell {
  height: 80px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #ebeef5;
  font-size: 14px;
}

.time-cell:last-child {
  border-bottom: none;
}

.time-detail {
  font-size: 12px;
  color: #666;
}

.schedule-cell {
  height: 80px;
  border-left: 1px solid #ebeef5;
  border-bottom: 1px solid #ebeef5;
  padding: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.schedule-cell:last-child {
  border-bottom: none;
}

.schedule-cell:hover {
  background-color: #f5f7fa;
}

.has-course {
  background-color: #e1f3d8;
}

.course-brief {
  font-size: 12px;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: center;
}

.location {
  font-size: 11px;
  color: #666;
  margin-top: 3px;
}

.degree-progress {
  text-align: center;
  max-width: 600px;
  margin: 0 auto 30px;
}

.progress-text {
  margin-top: 10px;
  color: #666;
}

.requirement-categories {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.requirement-card {
  border: 1px solid #ebeef5;
  border-radius: 4px;
  padding: 15px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.card-header h3 {
  margin: 0;
  font-size: 16px;
}

.progress-info {
  color: #666;
}

.requirement-items {
  margin-top: 15px;
}

.requirement-item {
  display: flex;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px dashed #ebeef5;
}

.requirement-item:last-child {
  border-bottom: none;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-right: 10px;
}

.status-dot.completed {
  background-color: #67C23A;
}

.status-dot.in-progress {
  background-color: #E6A23C;
}

.status-dot.planned {
  background-color: #409EFF;
}

.status-dot.not-started {
  background-color: #909399;
}

.item-detail {
  flex: 1;
}

.item-name {
  font-weight: 500;
}

.item-progress {
  font-size: 12px;
  color: #666;
  margin-top: 2px;
}

.audit-summary {
  margin-bottom: 30px;
}

.audit-status {
  display: flex;
  align-items: center;
  background: #fdf6ec;
  border-radius: 4px;
  padding: 15px;
  margin-bottom: 20px;
}

.audit-status i {
  font-size: 32px;
  color: #E6A23C;
  margin-right: 15px;
}

.audit-status .title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 5px;
}

.audit-status .description {
  color: #666;
}

.checklist {
  padding: 0 20px;
}

.checklist-item {
  display: flex;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px dashed #ebeef5;
}

.checklist-item:last-child {
  border-bottom: none;
}

.checklist-item i {
  margin-right: 10px;
  font-size: 16px;
}

.checklist-item.complete i {
  color: #67C23A;
}

.checklist-item.incomplete i {
  color: #F56C6C;
}

.recommendation {
  margin-top: 20px;
}

.recommendation h3 {
  margin-bottom: 15px;
}

.action-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
}

.action-card {
  display: flex;
  padding: 15px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
}

.action-card .icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-right: 15px;
}

.action-card .content {
  flex: 1;
}

.action-card .title {
  font-weight: 600;
  margin-bottom: 5px;
}

.action-card .description {
  font-size: 13px;
  color: #666;
  margin-bottom: 8px;
}

.action-btn {
  padding: 0;
}

/* 响应式布局 */
@media (max-width: 992px) {
  .credit-summary {
    flex-wrap: wrap;
  }
  
  .summary-item {
    flex: 1 0 50%;
    padding: 10px 0;
    border-right: none;
    border-bottom: 1px solid #eee;
  }
  
  .summary-item:nth-child(3),
  .summary-item:nth-child(4) {
    border-bottom: none;
  }
  
  .weekly-schedule {
    overflow-x: auto;
  }
}

@media (max-width: 768px) {
  .semester-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .actions {
    margin-top: 10px;
  }
  
  .summary-item {
    flex: 1 0 100%;
  }
  
  .summary-item:nth-child(3) {
    border-bottom: 1px solid #eee;
  }
}
</style>
