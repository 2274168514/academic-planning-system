<template>
  <div class="learning-progress-container">
    <h1 class="page-title">学习进度</h1>
    
    <div class="progress-overview">
      <div class="overview-cards">
        <div class="card">
          <div class="card-header">
            <div class="title">总体完成度</div>
            <el-select v-model="selectedSemester" size="small" placeholder="选择学期">
              <el-option
                v-for="item in semesters"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </div>
          <div class="progress-circle">
            <el-progress type="circle" :percentage="75" :width="140"></el-progress>
            <div class="progress-detail">
              <div class="main">75%</div>
              <div class="sub-text">已完成/总计</div>
            </div>
          </div>
          <div class="card-footer">
            <div class="stat-item">
              <div class="value">152/204</div>
              <div class="label">学时</div>
            </div>
            <div class="stat-item">
              <div class="value">6/8</div>
              <div class="label">课程</div>
            </div>
            <div class="stat-item">
              <div class="value">42</div>
              <div class="label">技能点</div>
            </div>
          </div>
        </div>
        
        <div class="card time-card">
          <div class="card-header">
            <div class="title">学习时长</div>
            <el-select v-model="selectedTimeRange" size="small" placeholder="时间范围">
              <el-option
                v-for="item in timeRanges"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </div>
          <div class="time-chart" ref="timeChart">
            <!-- 这里将渲染学习时间图表 -->
            <div class="chart-placeholder">时间分布图表</div>
          </div>
          <div class="card-footer time-stats">
            <div class="stat-item">
              <div class="value">26.5</div>
              <div class="label">本周学时</div>
            </div>
            <div class="stat-item">
              <div class="value">+15%</div>
              <div class="label">环比增长</div>
            </div>
          </div>
        </div>
        
        <div class="card skill-card">
          <div class="card-header">
            <div class="title">技能雷达</div>
            <el-select v-model="selectedSkillCategory" size="small" placeholder="技能类别">
              <el-option
                v-for="item in skillCategories"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </div>
          <div class="skill-radar" ref="skillRadar">
            <!-- 这里将渲染技能雷达图 -->
            <div class="chart-placeholder">技能雷达图</div>
          </div>
          <div class="card-footer">
            <div class="skill-legend">
              <div class="legend-item">
                <div class="color-box current"></div>
                <div class="legend-text">当前水平</div>
              </div>
              <div class="legend-item">
                <div class="color-box target"></div>
                <div class="legend-text">目标水平</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="course-progress-section">
      <div class="section-header">
        <h2>课程学习进度</h2>
        <div class="header-right">
          <el-select v-model="courseSort" size="small" placeholder="排序方式">
            <el-option label="按进度降序" value="progress-desc"></el-option>
            <el-option label="按进度升序" value="progress-asc"></el-option>
            <el-option label="按名称排序" value="name"></el-option>
          </el-select>
        </div>
      </div>
      
      <div class="course-progress-list">
        <div v-for="(course, index) in sortedCourses" :key="index" class="course-progress-item">
          <div class="course-info">
            <div class="course-title">{{ course.name }}</div>
            <div class="course-meta">
              <span class="meta-item">
                <i class="el-icon-user"></i> {{ course.instructor }}
              </span>
              <span class="meta-item">
                <i class="el-icon-time"></i> {{ course.duration }}
              </span>
            </div>
          </div>
          <div class="progress-stats">
            <div class="progress-bar-wrapper">
              <div class="progress-labels">
                <span>{{ course.progress }}%</span>
                <span>{{ course.completedUnits }}/{{ course.totalUnits }} 单元</span>
              </div>
              <el-progress 
                :percentage="course.progress" 
                :color="getProgressColor(course.progress)"
              ></el-progress>
            </div>
            <div class="course-actions">
              <el-button size="small" type="primary" plain>继续学习</el-button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="learning-achievement-section">
      <div class="section-header">
        <h2>学习成就</h2>
        <div class="header-right">
          <el-radio-group v-model="achievementFilter" size="small">
            <el-radio-button label="all">全部</el-radio-button>
            <el-radio-button label="unlocked">已获得</el-radio-button>
            <el-radio-button label="locked">待解锁</el-radio-button>
          </el-radio-group>
        </div>
      </div>
      
      <div class="achievement-grid">
        <div v-for="(achievement, index) in filteredAchievements" :key="index" 
          :class="['achievement-card', {'locked': !achievement.unlocked}]">
          <div class="achievement-icon">
            <i :class="achievement.icon"></i>
          </div>
          <div class="achievement-content">
            <div class="achievement-title">{{ achievement.title }}</div>
            <div class="achievement-desc">{{ achievement.description }}</div>
            <div v-if="!achievement.unlocked" class="achievement-progress">
              <div class="progress-text">{{ achievement.progress }}/{{ achievement.target }}</div>
              <el-progress 
                :percentage="(achievement.progress/achievement.target) * 100" 
                :show-text="false"
              ></el-progress>
            </div>
            <div v-else class="achievement-date">
              获得于 {{ achievement.dateUnlocked }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "LearningProgress",
  data() {
    return {
      selectedSemester: 'current',
      selectedTimeRange: 'week',
      selectedSkillCategory: 'all',
      courseSort: 'progress-desc',
      achievementFilter: 'all',
      
      semesters: [
        { value: 'current', label: '当前学期' },
        { value: 'last', label: '上学期' },
        { value: 'all', label: '所有学期' }
      ],
      
      timeRanges: [
        { value: 'week', label: '本周' },
        { value: 'month', label: '本月' },
        { value: 'semester', label: '学期' }
      ],
      
      skillCategories: [
        { value: 'all', label: '所有技能' },
        { value: 'programming', label: '编程能力' },
        { value: 'theory', label: '理论知识' },
        { value: 'design', label: '设计能力' }
      ],
      
      courses: [
        {
          name: '数据结构与算法',
          instructor: '张教授',
          duration: '48课时',
          progress: 85,
          completedUnits: 17,
          totalUnits: 20
        },
        {
          name: '计算机网络原理',
          instructor: '李教授',
          duration: '36课时',
          progress: 62,
          completedUnits: 10,
          totalUnits: 16
        },
        {
          name: '操作系统',
          instructor: '王教授',
          duration: '40课时',
          progress: 45,
          completedUnits: 9,
          totalUnits: 20
        },
        {
          name: '软件工程',
          instructor: '刘教授',
          duration: '32课时',
          progress: 90,
          completedUnits: 18,
          totalUnits: 20
        },
        {
          name: '计算机图形学',
          instructor: '赵教授',
          duration: '36课时',
          progress: 25,
          completedUnits: 4,
          totalUnits: 16
        }
      ],
      
      achievements: [
        {
          title: '勤奋学习者',
          description: '连续30天每天学习超过2小时',
          icon: 'el-icon-timer',
          unlocked: true,
          dateUnlocked: '2023-04-15',
          progress: 30,
          target: 30
        },
        {
          title: '编程高手',
          description: '完成100个编程练习',
          icon: 'el-icon-s-opportunity',
          unlocked: true,
          dateUnlocked: '2023-03-22',
          progress: 100,
          target: 100
        },
        {
          title: '知识探索者',
          description: '在3个不同学科领域学习课程',
          icon: 'el-icon-discover',
          unlocked: true,
          dateUnlocked: '2023-02-18',
          progress: 3,
          target: 3
        },
        {
          title: '完美主义者',
          description: '5门课程获得优秀成绩',
          icon: 'el-icon-trophy',
          unlocked: false,
          progress: 3,
          target: 5
        },
        {
          title: '团队合作者',
          description: '参与10个小组项目',
          icon: 'el-icon-s-custom',
          unlocked: false,
          progress: 6,
          target: 10
        },
        {
          title: '精通者',
          description: '在一门课程的所有测验中获得满分',
          icon: 'el-icon-star-on',
          unlocked: false,
          progress: 8,
          target: 10
        }
      ]
    }
  },
  computed: {
    sortedCourses() {
      // 按选定的排序方式返回排序后的课程
      return [...this.courses].sort((a, b) => {
        if (this.courseSort === 'progress-desc') {
          return b.progress - a.progress;
        } else if (this.courseSort === 'progress-asc') {
          return a.progress - b.progress;
        } else if (this.courseSort === 'name') {
          return a.name.localeCompare(b.name);
        }
        return 0;
      });
    },
    filteredAchievements() {
      // 按照选择的过滤条件过滤成就
      if (this.achievementFilter === 'all') {
        return this.achievements;
      } else if (this.achievementFilter === 'unlocked') {
        return this.achievements.filter(a => a.unlocked);
      } else {
        return this.achievements.filter(a => !a.unlocked);
      }
    }
  },
  mounted() {
    this.initCharts();
  },
  methods: {
    initCharts() {
      console.log('初始化图表');
      // 在这里使用echarts或其他图表库初始化时间图表和技能雷达图
    },
    getProgressColor(percentage) {
      if (percentage < 30) return '#F56C6C';
      if (percentage < 70) return '#E6A23C';
      return '#67C23A';
    }
  }
}
</script>

<style scoped>
.learning-progress-container {
  padding: 20px;
}

.page-title {
  margin-bottom: 24px;
  font-size: 24px;
  color: #333;
}

.progress-overview {
  margin-bottom: 30px;
}

.overview-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-header .title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.progress-circle {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  margin-bottom: 15px;
}

.progress-detail {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.progress-detail .main {
  font-size: 24px;
  font-weight: 600;
  color: #333;
}

.progress-detail .sub-text {
  font-size: 12px;
  color: #666;
  margin-top: 4px;
}

.card-footer {
  display: flex;
  justify-content: space-around;
}

.time-stats {
  margin-top: 20px;
}

.stat-item {
  text-align: center;
}

.stat-item .value {
  font-size: 20px;
  font-weight: 600;
  color: #333;
}

.stat-item .label {
  font-size: 13px;
  color: #666;
  margin-top: 5px;
}

.time-chart, .skill-radar {
  height: 220px;
  width: 100%;
}

.chart-placeholder {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  background: #f9f9f9;
  border-radius: 4px;
}

.skill-legend {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.legend-item {
  display: flex;
  align-items: center;
}

.color-box {
  width: 12px;
  height: 12px;
  margin-right: 6px;
  border-radius: 2px;
}

.color-box.current {
  background-color: #409EFF;
}

.color-box.target {
  background-color: rgba(64, 158, 255, 0.3);
}

.legend-text {
  font-size: 12px;
  color: #666;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h2 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.course-progress-section, .learning-achievement-section {
  margin-top: 30px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  padding: 20px;
}

.course-progress-item {
  display: flex;
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
}

.course-progress-item:last-child {
  border-bottom: none;
}

.course-info {
  flex: 1;
}

.course-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 8px;
}

.course-meta {
  color: #666;
  font-size: 13px;
}

.meta-item {
  margin-right: 15px;
}

.meta-item i {
  margin-right: 4px;
}

.progress-stats {
  width: 50%;
  display: flex;
  align-items: center;
}

.progress-bar-wrapper {
  flex: 1;
  margin-right: 15px;
}

.progress-labels {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
  font-size: 13px;
  color: #666;
}

.achievement-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
}

.achievement-card {
  display: flex;
  background: white;
  padding: 15px;
  border-radius: 4px;
  border: 1px solid #ebeef5;
}

.achievement-card.locked {
  opacity: 0.7;
}

.achievement-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: #409EFF;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin-right: 15px;
}

.locked .achievement-icon {
  background-color: #909399;
}

.achievement-content {
  flex: 1;
}

.achievement-title {
  font-weight: 600;
  margin-bottom: 5px;
}

.achievement-desc {
  font-size: 13px;
  color: #666;
  margin-bottom: 8px;
}

.achievement-progress, .achievement-date {
  font-size: 12px;
  color: #999;
}

.progress-text {
  margin-bottom: 4px;
}

/* 响应式布局 */
@media (max-width: 1200px) {
  .overview-cards {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .skill-card {
    grid-column: span 2;
  }
}

@media (max-width: 768px) {
  .overview-cards {
    grid-template-columns: 1fr;
  }
  
  .skill-card {
    grid-column: span 1;
  }
  
  .course-progress-item {
    flex-direction: column;
  }
  
  .progress-stats {
    width: 100%;
    margin-top: 15px;
  }
  
  .achievement-grid {
    grid-template-columns: 1fr;
  }
}
</style>
