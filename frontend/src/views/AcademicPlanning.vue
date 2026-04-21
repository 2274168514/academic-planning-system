<template>
  <div class="academic-planning-container">
    <h1 class="page-title">学业规划</h1>
    
    <div class="planning-content">
      <div class="planning-tabs">
        <el-tabs v-model="activeTab" type="border-card">
          <el-tab-pane name="semester" label="学期规划">
            <div class="semester-header">
              <h3>2023-2024学年 第二学期</h3>
              <div class="actions">
                <el-button type="primary" size="small" @click="addCourse">添加课程</el-button>
                <el-button size="small" @click="switchSemester">切换学期</el-button>
              </div>
            </div>
            
            <div class="credit-summary">
              <div class="summary-item">
                <div class="label">已选学分</div>
                <div class="value">16</div>
              </div>
              <div class="summary-item">
                <div class="label">建议学分</div>
                <div class="value">18-22</div>
              </div>
              <div class="summary-item">
                <div class="label">已修学分</div>
                <div class="value">86</div>
              </div>
              <div class="summary-item">
                <div class="label">总学分要求</div>
                <div class="value">160</div>
              </div>
            </div>
            
            <el-table :data="semesterCourses" style="width: 100%" border>
              <el-table-column prop="code" label="课程编号" width="120"></el-table-column>
              <el-table-column prop="name" label="课程名称"></el-table-column>
              <el-table-column prop="type" label="课程类型" width="120"></el-table-column>
              <el-table-column prop="credits" label="学分" width="80" align="center"></el-table-column>
              <el-table-column prop="hours" label="学时" width="80" align="center"></el-table-column>
              <el-table-column prop="instructor" label="任课教师"></el-table-column>
              <el-table-column label="操作" width="150" align="center">
                <template #default="scope">
                  <el-button type="text" size="small" @click="viewCourseDetails(scope.row)">详情</el-button>
                  <el-button type="text" size="small" class="danger-text" @click="removeCourse(scope.row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
            
            <div class="schedule-view">
              <h3>课程表视图</h3>
              <div class="weekly-schedule">
                <div class="time-column">
                  <div class="header-cell"></div>
                  <div class="time-cell" v-for="time in timeSlots" :key="time.id">
                    第{{time.slot}}节<br>
                    <span class="time-detail">{{time.time}}</span>
                  </div>
                </div>
                <div v-for="day in weekDays" :key="day.id" class="day-column">
                  <div class="header-cell">{{day.name}}</div>
                  <div class="schedule-cell" v-for="time in timeSlots" :key="`${day.id}-${time.id}`"
                    :class="{ 'has-course': hasCourse(day.id, time.id) }"
                    @click="showCourseAt(day.id, time.id)">
                    <div v-if="hasCourse(day.id, time.id)" class="course-brief">
                      {{getCourseAt(day.id, time.id).name}}<br>
                      <span class="location">{{getCourseAt(day.id, time.id).location}}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
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
export default {
  name: "AcademicPlanning",
  data() {
    return {
      activeTab: 'semester',
      semesterCourses: [
        { code: 'CS301', name: '数据库原理', type: '专业必修', credits: 4, hours: 64, instructor: '李教授' },
        { code: 'CS302', name: '软件工程', type: '专业必修', credits: 3, hours: 48, instructor: '王教授' },
        { code: 'CS305', name: '人工智能导论', type: '专业选修', credits: 3, hours: 48, instructor: '张教授' },
        { code: 'MATH201', name: '概率论与数理统计', type: '学科基础', credits: 4, hours: 64, instructor: '刘教授' },
        { code: 'GE102', name: '中国近代史纲要', type: '通识教育', credits: 2, hours: 32, instructor: '赵教授' }
      ],
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
    addCourse() {
      // 实现添加课程的逻辑
      this.$message({
        message: '打开课程选择对话框',
        type: 'info'
      });
    },
    switchSemester() {
      // 实现切换学期的逻辑
      this.$message({
        message: '切换到不同学期',
        type: 'info'
      });
    },
    viewCourseDetails(course) {
      // 实现查看课程详情的逻辑
      this.$message({
        message: `查看课程：${course.name}`,
        type: 'info'
      });
    },
    removeCourse(course) {
      // 实现删除课程的逻辑
      this.$confirm(`确定要从学期计划中移除 ${course.name} 吗?`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$message({
          type: 'success',
          message: '删除成功!'
        });
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        });          
      });
    },
    showCourseAt(day, time) {
      if (this.hasCourse(day, time)) {
        const course = this.getCourseAt(day, time);
        this.$message({
          message: `${course.name} - ${course.location}`,
          type: 'info'
        });
      }
    }
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
