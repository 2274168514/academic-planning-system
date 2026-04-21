<template>
  <div class="career-path-container">
    <h1 class="page-title">职业发展规划</h1>
    
    <div class="career-explore-section">
      <div class="section-header">
        <h2>探索职业方向</h2>
        <div class="search-bar">
          <el-input
            placeholder="搜索职业或技能..."
            v-model="searchQuery"
            prefix-icon="el-icon-search"
            clearable
          >
          </el-input>
        </div>
      </div>
      
      <div class="career-filters">
        <div class="filter-group">
          <span class="filter-label">领域：</span>
          <el-radio-group v-model="selectedField" size="small">
            <el-radio-button label="all">全部</el-radio-button>
            <el-radio-button label="development">软件开发</el-radio-button>
            <el-radio-button label="ai">人工智能</el-radio-button>
            <el-radio-button label="data">数据科学</el-radio-button>
            <el-radio-button label="security">网络安全</el-radio-button>
          </el-radio-group>
        </div>
        
        <div class="filter-group">
          <span class="filter-label">薪资范围：</span>
          <el-select v-model="salaryRange" size="small" placeholder="选择薪资范围">
            <el-option
              v-for="item in salaryOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </div>
        
        <div class="filter-group">
          <span class="filter-label">排序方式：</span>
          <el-select v-model="sortBy" size="small" placeholder="排序方式">
            <el-option label="热门程度" value="popularity"></el-option>
            <el-option label="薪资水平" value="salary"></el-option>
            <el-option label="职业前景" value="prospect"></el-option>
          </el-select>
        </div>
      </div>
      
      <div class="career-paths">
        <div v-for="(path, index) in filteredPaths" :key="index" class="career-card" @click="selectCareerPath(path)">
          <div class="career-header">
            <div class="career-icon" :style="{ backgroundColor: path.color }">
              <i :class="path.icon"></i>
            </div>
            <div class="career-title">{{ path.title }}</div>
          </div>
          <div class="career-content">
            <div class="career-desc">{{ path.description }}</div>
            <div class="career-stats">
              <div class="stat-item">
                <div class="stat-label">平均薪资</div>
                <div class="stat-value">{{ path.salary }}</div>
              </div>
              <div class="stat-item">
                <div class="stat-label">需求趋势</div>
                <div class="stat-value">
                  <i :class="getTrendIcon(path.trend)" :style="{ color: getTrendColor(path.trend) }"></i>
                  {{ path.trend > 0 ? '+' + path.trend + '%' : path.trend + '%' }}
                </div>
              </div>
              <div class="stat-item">
                <div class="stat-label">匹配度</div>
                <div class="stat-value">{{ path.match }}%</div>
              </div>
            </div>
          </div>
          <div class="career-footer">
            <el-button type="text">查看详情</el-button>
            <el-button type="primary" size="small" @click.stop="createPlan(path)">制定规划</el-button>
          </div>
        </div>
      </div>
    </div>
    
    <div class="career-detail-section" v-if="selectedPath">
      <div class="section-header">
        <div class="header-title">
          <h2>{{ selectedPath.title }}</h2>
          <div class="match-badge" :class="getMatchClass(selectedPath.match)">
            匹配度 {{ selectedPath.match }}%
          </div>
        </div>
        <el-button @click="selectedPath = null" icon="el-icon-back" size="small">返回列表</el-button>
      </div>
      
      <div class="detail-content">
        <div class="detail-overview">
          <p class="detail-description">{{ selectedPath.fullDescription || selectedPath.description }}</p>
          
          <div class="detail-stats">
            <div class="stat-box">
              <div class="stat-title">平均薪资</div>
              <div class="stat-value lg">{{ selectedPath.salary }}</div>
            </div>
            <div class="stat-box">
              <div class="stat-title">市场需求</div>
              <div class="stat-value lg" :style="{ color: getTrendColor(selectedPath.trend) }">
                {{ selectedPath.trend > 0 ? '上升 ' + selectedPath.trend + '%' : '下降 ' + Math.abs(selectedPath.trend) + '%' }}
              </div>
            </div>
            <div class="stat-box">
              <div class="stat-title">入行年限</div>
              <div class="stat-value lg">{{ selectedPath.experience }}年</div>
            </div>
          </div>
        </div>
        
        <div class="skill-requirements">
          <h3>所需技能</h3>
          <div class="skill-groups">
            <div class="skill-group">
              <h4>核心技能</h4>
              <div class="skill-list">
                <div v-for="(skill, idx) in selectedPath.coreSkills" :key="'core-'+idx" class="skill-item">
                  <div class="skill-name">{{ skill.name }}</div>
                  <div class="skill-level-bar">
                    <div class="skill-level-indicator">
                      <div class="required-level" :style="{ width: skill.requiredLevel + '%' }"></div>
                      <div class="current-level" :style="{ width: skill.currentLevel + '%' }"></div>
                    </div>
                    <div class="skill-level-text">
                      <span>当前: {{ skill.currentLevel }}%</span>
                      <span>要求: {{ skill.requiredLevel }}%</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="skill-group">
              <h4>辅助技能</h4>
              <div class="skill-list">
                <div v-for="(skill, idx) in selectedPath.supportSkills" :key="'support-'+idx" class="skill-item">
                  <div class="skill-name">{{ skill.name }}</div>
                  <div class="skill-level-bar">
                    <div class="skill-level-indicator">
                      <div class="required-level" :style="{ width: skill.requiredLevel + '%' }"></div>
                      <div class="current-level" :style="{ width: skill.currentLevel + '%' }"></div>
                    </div>
                    <div class="skill-level-text">
                      <span>当前: {{ skill.currentLevel }}%</span>
                      <span>要求: {{ skill.requiredLevel }}%</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="learning-roadmap">
          <h3>学习路线图</h3>
          <div class="roadmap-timeline">
            <div v-for="(stage, idx) in selectedPath.roadmap" :key="idx" class="roadmap-stage">
              <div class="stage-indicator">
                <div class="stage-dot" :class="{ 'completed': stage.completed }"></div>
                <div class="stage-line" v-if="idx < selectedPath.roadmap.length - 1"></div>
              </div>
              <div class="stage-content">
                <div class="stage-header">
                  <div class="stage-title">{{ stage.title }}</div>
                  <div class="stage-duration">{{ stage.duration }}</div>
                </div>
                <div class="stage-description">{{ stage.description }}</div>
                <div class="stage-resources" v-if="stage.resources && stage.resources.length">
                  <div v-for="(resource, resIdx) in stage.resources" :key="resIdx" class="stage-resource">
                    <i :class="getResourceTypeIcon(resource.type)"></i> {{ resource.title }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="action-buttons">
          <el-button type="primary" @click="createPlan(selectedPath)">制定个人发展规划</el-button>
          <el-button @click="showRelatedCourses(selectedPath)">查看相关课程</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CareerPath",
  data() {
    return {
      searchQuery: '',
      selectedField: 'all',
      salaryRange: '',
      sortBy: 'popularity',
      selectedPath: null,
      
      salaryOptions: [
        { value: '', label: '不限' },
        { value: '10k-15k', label: '10k-15k' },
        { value: '15k-20k', label: '15k-20k' },
        { value: '20k-30k', label: '20k-30k' },
        { value: '30k+', label: '30k以上' }
      ],
      
      careerPaths: [
        {
          id: 1,
          title: '前端开发工程师',
          description: '专注于网站和应用的用户界面和交互体验的开发与实现。',
          fullDescription: '前端开发工程师负责构建网站和应用程序的用户界面，确保用户体验流畅和响应迅速。他们使用HTML、CSS和JavaScript等技术，结合现代前端框架如React、Vue或Angular来开发交互式网页应用。前端开发者需要关注网站性能优化、浏览器兼容性和响应式设计，确保应用在各种设备上都能良好运行。',
          color: '#409EFF',
          icon: 'el-icon-s-platform',
          field: 'development',
          salary: '15k-25k',
          trend: 15,
          match: 85,
          experience: 1,
          coreSkills: [
            { name: 'HTML/CSS', requiredLevel: 90, currentLevel: 80 },
            { name: 'JavaScript', requiredLevel: 85, currentLevel: 75 },
            { name: 'React/Vue', requiredLevel: 80, currentLevel: 60 },
            { name: 'Web性能优化', requiredLevel: 70, currentLevel: 45 }
          ],
          supportSkills: [
            { name: 'UI/UX设计基础', requiredLevel: 60, currentLevel: 50 },
            { name: 'Node.js', requiredLevel: 50, currentLevel: 40 },
            { name: '浏览器开发工具', requiredLevel: 75, currentLevel: 65 },
            { name: '响应式设计', requiredLevel: 85, currentLevel: 70 }
          ],
          roadmap: [
            {
              title: '掌握基础',
              duration: '2-3个月',
              description: '学习HTML、CSS和JavaScript基础，理解Web工作原理',
              completed: true,
              resources: [
                { type: 'course', title: 'Web开发基础课程' },
                { type: 'book', title: 'JavaScript高级程序设计' }
              ]
            },
            {
              title: '学习框架',
              duration: '3-4个月',
              description: '学习React或Vue等主流前端框架，掌握组件化开发',
              completed: false,
              resources: [
                { type: 'course', title: 'React入门到精通' },
                { type: 'project', title: '构建个人项目管理应用' }
              ]
            },
            {
              title: '进阶技能',
              duration: '2-3个月',
              description: '学习状态管理、路由、性能优化等进阶技能',
              completed: false,
              resources: [
                { type: 'course', title: '前端性能优化实战' },
                { type: 'project', title: '开发一个完整的电商前端' }
              ]
            },
            {
              title: '实战项目',
              duration: '3-6个月',
              description: '参与实际项目开发，积累项目经验和团队协作能力',
              completed: false,
              resources: [
                { type: 'internship', title: '前端开发实习' },
                { type: 'project', title: '开源项目贡献' }
              ]
            }
          ]
        },
        {
          id: 2,
          title: '数据科学家',
          description: '通过数据分析和机器学习技术解决复杂问题，提供数据驱动的决策支持。',
          color: '#67C23A',
          icon: 'el-icon-s-data',
          field: 'data',
          salary: '20k-35k',
          trend: 25,
          match: 70,
          experience: 2,
          coreSkills: [
            { name: 'Python', requiredLevel: 85, currentLevel: 70 },
            { name: '统计学', requiredLevel: 80, currentLevel: 65 },
            { name: '机器学习', requiredLevel: 85, currentLevel: 55 },
            { name: '数据可视化', requiredLevel: 75, currentLevel: 60 }
          ],
          supportSkills: [
            { name: 'SQL', requiredLevel: 70, currentLevel: 60 },
            { name: '大数据处理', requiredLevel: 65, currentLevel: 40 },
            { name: '业务分析能力', requiredLevel: 75, currentLevel: 65 },
            { name: '数据挖掘', requiredLevel: 70, currentLevel: 50 }
          ]
        },
        {
          id: 3,
          title: '机器学习工程师',
          description: '设计和实现机器学习模型和算法，将AI技术应用到实际业务中。',
          color: '#E6A23C',
          icon: 'el-icon-s-opportunity',
          field: 'ai',
          salary: '25k-40k',
          trend: 30,
          match: 65,
          experience: 2,
          coreSkills: [
            { name: 'Python', requiredLevel: 90, currentLevel: 70 },
            { name: '机器学习算法', requiredLevel: 85, currentLevel: 55 },
            { name: '深度学习', requiredLevel: 80, currentLevel: 40 },
            { name: '数据处理', requiredLevel: 75, currentLevel: 60 }
          ],
          supportSkills: [
            { name: '数学基础', requiredLevel: 80, currentLevel: 70 },
            { name: '算法优化', requiredLevel: 70, currentLevel: 50 },
            { name: '计算机系统', requiredLevel: 65, currentLevel: 55 },
            { name: '软件工程', requiredLevel: 60, currentLevel: 65 }
          ]
        },
        {
          id: 4,
          title: '后端开发工程师',
          description: '负责服务器端应用程序的开发，确保系统的性能、安全和可扩展性。',
          color: '#F56C6C',
          icon: 'el-icon-s-cooperation',
          field: 'development',
          salary: '18k-30k',
          trend: 10,
          match: 75,
          experience: 1,
          coreSkills: [
            { name: 'Java/Python/Go', requiredLevel: 85, currentLevel: 75 },
            { name: '数据库设计', requiredLevel: 80, currentLevel: 60 },
            { name: 'API开发', requiredLevel: 75, currentLevel: 65 },
            { name: '系统架构', requiredLevel: 70, currentLevel: 50 }
          ],
          supportSkills: [
            { name: '服务器管理', requiredLevel: 60, currentLevel: 45 },
            { name: '性能优化', requiredLevel: 65, currentLevel: 50 },
            { name: '安全知识', requiredLevel: 70, currentLevel: 55 },
            { name: '微服务', requiredLevel: 65, currentLevel: 40 }
          ]
        },
        {
          id: 5,
          title: '网络安全工程师',
          description: '保护组织的计算机系统和网络免受攻击，确保数据安全和隐私。',
          color: '#909399',
          icon: 'el-icon-lock',
          field: 'security',
          salary: '20k-35k',
          trend: 20,
          match: 60,
          experience: 3,
          coreSkills: [
            { name: '网络协议', requiredLevel: 85, currentLevel: 60 },
            { name: '安全评估', requiredLevel: 80, currentLevel: 50 },
            { name: '漏洞分析', requiredLevel: 75, currentLevel: 45 },
            { name: '安全工具使用', requiredLevel: 80, currentLevel: 55 }
          ],
          supportSkills: [
            { name: '编程能力', requiredLevel: 70, currentLevel: 65 },
            { name: '操作系统知识', requiredLevel: 75, currentLevel: 60 },
            { name: '风险管理', requiredLevel: 65, currentLevel: 40 },
            { name: '密码学', requiredLevel: 70, currentLevel: 35 }
          ]
        }
      ]
    }
  },
  computed: {
    filteredPaths() {
      let result = this.careerPaths;
      
      // 按照领域筛选
      if (this.selectedField !== 'all') {
        result = result.filter(path => path.field === this.selectedField);
      }
      
      // 按照薪资范围筛选
      if (this.salaryRange) {
        // 简化处理，实际应根据薪资范围具体逻辑筛选
        result = result.filter(path => path.salary.includes(this.salaryRange.split('-')[0]));
      }
      
      // 搜索关键词
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(path => 
          path.title.toLowerCase().includes(query) || 
          path.description.toLowerCase().includes(query)
        );
      }
      
      // 根据排序方式排序
      switch(this.sortBy) {
        case 'popularity':
          result.sort((a, b) => b.match - a.match);
          break;
        case 'salary':
          // 简化处理，实际应解析薪资字符串进行比较
          result.sort((a, b) => {
            const aMin = parseInt(a.salary.split('-')[0]);
            const bMin = parseInt(b.salary.split('-')[0]);
            return bMin - aMin;
          });
          break;
        case 'prospect':
          result.sort((a, b) => b.trend - a.trend);
          break;
      }
      
      return result;
    }
  },
  methods: {
    selectCareerPath(path) {
      this.selectedPath = path;
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    },
    
    createPlan(path) {
      // 实现制定规划的逻辑
      this.$message({
        message: `即将为您制定"${path.title}"的职业发展规划`,
        type: 'success'
      });
    },
    
    showRelatedCourses(path) {
      // 实现显示相关课程的逻辑
      this.$message({
        message: `查看与"${path.title}"相关的课程`,
        type: 'info'
      });
    },
    
    getTrendIcon(trend) {
      if (trend > 0) return 'el-icon-top';
      if (trend < 0) return 'el-icon-bottom';
      return 'el-icon-right';
    },
    
    getTrendColor(trend) {
      if (trend > 15) return '#67C23A';
      if (trend > 0) return '#E6A23C';
      return '#F56C6C';
    },
    
    getMatchClass(match) {
      if (match >= 80) return 'high-match';
      if (match >= 60) return 'medium-match';
      return 'low-match';
    },
    
    getResourceTypeIcon(type) {
      const icons = {
        'course': 'el-icon-reading',
        'book': 'el-icon-notebook-2',
        'project': 'el-icon-s-cooperation',
        'internship': 'el-icon-office-building'
      };
      return icons[type] || 'el-icon-document';
    }
  }
}
</script>

<style scoped>
.career-path-container {
  padding: 20px;
}

.page-title {
  margin-bottom: 24px;
  font-size: 24px;
  color: #333;
}

.career-explore-section, .career-detail-section {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  padding: 20px;
  margin-bottom: 30px;
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
}

.search-bar {
  width: 300px;
}

.career-filters {
  margin-bottom: 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.filter-group {
  display: flex;
  align-items: center;
}

.filter-label {
  margin-right: 10px;
  color: #606266;
}

.career-paths {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.career-card {
  border: 1px solid #ebeef5;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;
}

.career-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.career-header {
  display: flex;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
}

.career-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  color: white;
  font-size: 18px;
}

.career-title {
  font-size: 16px;
  font-weight: 600;
}

.career-content {
  padding: 15px;
}

.career-desc {
  color: #606266;
  margin-bottom: 15px;
  min-height: 60px;
}

.career-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.stat-item {
  text-align: center;
}

.stat-label {
  font-size: 12px;
  color: #909399;
  margin-bottom: 5px;
}

.stat-value {
  font-size: 14px;
  font-weight: 600;
}

.career-footer {
  padding: 10px 15px;
  border-top: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 详情部分 */
.header-title {
  display: flex;
  align-items: center;
}

.match-badge {
  margin-left: 15px;
  padding: 4px 10px;
  border-radius: 15px;
  font-size: 12px;
  color: white;
}

.high-match {
  background-color: #67C23A;
}

.medium-match {
  background-color: #E6A23C;
}

.low-match {
  background-color: #F56C6C;
}

.detail-content {
  padding: 10px;
}

.detail-overview {
  margin-bottom: 30px;
}

.detail-description {
  color: #606266;
  line-height: 1.6;
  margin-bottom: 20px;
}

.detail-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.stat-box {
  background: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
  text-align: center;
}

.stat-title {
  color: #909399;
  margin-bottom: 10px;
  font-size: 14px;
}

.stat-value.lg {
  font-size: 18px;
  font-weight: 600;
}

.skill-requirements {
  margin-bottom: 30px;
}

.skill-requirements h3, .learning-roadmap h3 {
  font-size: 18px;
  margin-bottom: 15px;
  color: #333;
}

.skill-groups {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.skill-group h4 {
  font-size: 16px;
  margin-bottom: 10px;
}

.skill-item {
  margin-bottom: 15px;
}

.skill-name {
  font-weight: 500;
  margin-bottom: 5px;
}

.skill-level-bar {
  margin-bottom: 10px;
}

.skill-level-indicator {
  height: 8px;
  background-color: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
  position: relative;
  margin-bottom: 5px;
}

.required-level {
  position: absolute;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}

.current-level {
  position: absolute;
  height: 100%;
  background-color: #409EFF;
  border-radius: 4px;
  z-index: 1;
}

.skill-level-text {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #909399;
}

.roadmap-timeline {
  padding: 10px 0;
}

.roadmap-stage {
  display: flex;
  margin-bottom: 30px;
}

.roadmap-stage:last-child {
  margin-bottom: 0;
}

.stage-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-right: 15px;
}

.stage-dot {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background-color: #dcdfe6;
  z-index: 1;
}

.stage-dot.completed {
  background-color: #67C23A;
}

.stage-line {
  height: 100%;
  width: 2px;
  background-color: #dcdfe6;
  margin: 5px 0;
}

.stage-content {
  flex: 1;
}

.stage-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.stage-title {
  font-weight: 600;
  font-size: 16px;
}

.stage-duration {
  color: #909399;
  font-size: 14px;
}

.stage-description {
  color: #606266;
  margin-bottom: 10px;
}

.stage-resources {
  margin-top: 10px;
}

.stage-resource {
  background-color: #f5f7fa;
  padding: 5px 10px;
  border-radius: 4px;
  margin-right: 10px;
  margin-bottom: 10px;
  display: inline-block;
  font-size: 13px;
  color: #606266;
}

.stage-resource i {
  margin-right: 5px;
  color: #409EFF;
}

.action-buttons {
  margin-top: 30px;
  display: flex;
  justify-content: center;
  gap: 20px;
}

/* 响应式布局 */
@media (max-width: 992px) {
  .skill-groups {
    grid-template-columns: 1fr;
  }
  
  .detail-stats {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .search-bar {
    width: 100%;
    margin-top: 10px;
  }
  
  .career-paths {
    grid-template-columns: 1fr;
  }
  
  .career-stats {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .header-title {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .match-badge {
    margin-left: 0;
    margin-top: 10px;
  }
}
</style>
