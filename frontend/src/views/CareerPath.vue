<template>
  <div class="career-container">
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">职业发展规划</h1>
        <span class="page-subtitle">探索适合你的职业方向</span>
      </div>
      <div class="search-wrap">
        <el-input
          v-model="searchQuery"
          placeholder="搜索职业或技能..."
          clearable
          size="large"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>
    </div>

    <!-- 筛选栏 -->
    <div class="filters-panel">
      <div class="filter-row">
        <span class="filter-label">领域</span>
        <div class="filter-tags">
          <span class="filter-tag" :class="{ active: selectedField === 'all' }" @click="selectedField = 'all'">全部</span>
          <span class="filter-tag" :class="{ active: selectedField === 'development' }" @click="selectedField = 'development'">软件开发</span>
          <span class="filter-tag" :class="{ active: selectedField === 'ai' }" @click="selectedField = 'ai'">人工智能</span>
          <span class="filter-tag" :class="{ active: selectedField === 'data' }" @click="selectedField = 'data'">数据科学</span>
          <span class="filter-tag" :class="{ active: selectedField === 'security' }" @click="selectedField = 'security'">网络安全</span>
        </div>
      </div>
      <div class="filter-divider"></div>
      <div class="filter-row filter-row-selects">
        <div class="select-group">
          <span class="filter-label">薪资范围</span>
          <el-select v-model="salaryRange" size="small" placeholder="不限" style="width: 130px">
            <el-option v-for="item in salaryOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </div>
        <div class="select-group">
          <span class="filter-label">排序方式</span>
          <el-select v-model="sortBy" size="small" placeholder="热门程度" style="width: 130px">
            <el-option label="热门程度" value="popularity" />
            <el-option label="薪资水平" value="salary" />
            <el-option label="职业前景" value="prospect" />
          </el-select>
        </div>
      </div>
    </div>

    <!-- 职业卡片列表 -->
    <div class="career-grid" v-if="!selectedPath">
      <div
        v-for="(path, index) in filteredPaths"
        :key="index"
        class="career-card"
        @click="selectCareerPath(path)"
      >
        <div class="card-top" :style="{ background: path.color }">
          <el-icon class="card-top-icon"><component :is="path.icon" /></el-icon>
          <div class="card-match-badge">匹配 {{ path.match }}%</div>
        </div>
        <div class="card-body">
          <h3 class="career-title">{{ path.title }}</h3>
          <p class="career-desc">{{ path.description }}</p>
          <div class="career-stats">
            <div class="stat-item">
              <span class="stat-label">平均薪资</span>
              <span class="stat-value">{{ path.salary }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">需求趋势</span>
              <span class="stat-value trend-value" :style="{ color: getTrendColor(path.trend) }">
                <el-icon><component :is="getTrendIcon(path.trend)" /></el-icon>
                {{ path.trend > 0 ? '+' + path.trend + '%' : path.trend + '%' }}
              </span>
            </div>
            <div class="stat-item">
              <span class="stat-label">入行年限</span>
              <span class="stat-value">{{ path.experience }} 年</span>
            </div>
          </div>
        </div>
        <div class="card-footer">
          <el-button type="primary" link @click.stop="selectCareerPath(path)">查看详情</el-button>
          <el-button type="primary" size="small" @click.stop="createPlan(path)">制定规划</el-button>
        </div>
      </div>
    </div>

    <!-- 职业详情 -->
    <div class="career-detail" v-if="selectedPath">
      <div class="detail-hero" :style="{ background: selectedPath.color }">
        <el-icon class="hero-icon"><component :is="selectedPath.icon" /></el-icon>
        <div class="hero-info">
          <h2 class="hero-title">{{ selectedPath.title }}</h2>
          <div class="hero-badges">
            <span class="match-badge" :class="getMatchClass(selectedPath.match)">
              匹配度 {{ selectedPath.match }}%
            </span>
            <span class="field-badge">{{ fieldLabel[selectedPath.field] }}</span>
          </div>
        </div>
        <el-button class="back-btn" @click="selectedPath = null" size="small">
          <el-icon><ArrowLeft /></el-icon> 返回列表
        </el-button>
      </div>

      <div class="detail-body">
        <!-- 概览 -->
        <div class="detail-section">
          <p class="detail-desc">{{ selectedPath.fullDescription || selectedPath.description }}</p>
          <div class="overview-stats">
            <div class="overview-stat">
              <div class="ov-label">平均薪资</div>
              <div class="ov-value">{{ selectedPath.salary }}</div>
            </div>
            <div class="overview-stat">
              <div class="ov-label">市场需求</div>
              <div class="ov-value" :style="{ color: getTrendColor(selectedPath.trend) }">
                {{ selectedPath.trend > 0 ? '上升 +' + selectedPath.trend + '%' : '下降 ' + selectedPath.trend + '%' }}
              </div>
            </div>
            <div class="overview-stat">
              <div class="ov-label">入行年限</div>
              <div class="ov-value">{{ selectedPath.experience }} 年</div>
            </div>
          </div>
        </div>

        <!-- 技能要求 -->
        <div class="detail-section">
          <h3 class="section-title">所需技能</h3>
          <div class="skill-groups">
            <div class="skill-group">
              <h4 class="skill-group-title">核心技能</h4>
              <div
                v-for="(skill, idx) in selectedPath.coreSkills"
                :key="'core-' + idx"
                class="skill-item"
              >
                <div class="skill-row">
                  <span class="skill-name">{{ skill.name }}</span>
                  <span class="skill-pcts">
                    <span class="current-pct">当前 {{ skill.currentLevel }}%</span>
                    <span class="required-pct">需要 {{ skill.requiredLevel }}%</span>
                  </span>
                </div>
                <div class="skill-track">
                  <div class="skill-required" :style="{ width: skill.requiredLevel + '%' }"></div>
                  <div class="skill-current" :style="{ width: skill.currentLevel + '%' }"></div>
                </div>
              </div>
            </div>
            <div class="skill-group">
              <h4 class="skill-group-title">辅助技能</h4>
              <div
                v-for="(skill, idx) in selectedPath.supportSkills"
                :key="'support-' + idx"
                class="skill-item"
              >
                <div class="skill-row">
                  <span class="skill-name">{{ skill.name }}</span>
                  <span class="skill-pcts">
                    <span class="current-pct">当前 {{ skill.currentLevel }}%</span>
                    <span class="required-pct">需要 {{ skill.requiredLevel }}%</span>
                  </span>
                </div>
                <div class="skill-track">
                  <div class="skill-required" :style="{ width: skill.requiredLevel + '%' }"></div>
                  <div class="skill-current" :style="{ width: skill.currentLevel + '%' }"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 学习路线图 -->
        <div class="detail-section" v-if="selectedPath.roadmap && selectedPath.roadmap.length">
          <h3 class="section-title">学习路线图</h3>
          <div class="roadmap">
            <div
              v-for="(stage, idx) in selectedPath.roadmap"
              :key="idx"
              class="roadmap-item"
            >
              <div class="roadmap-indicator">
                <div class="roadmap-dot" :class="{ completed: stage.completed }"></div>
                <div class="roadmap-line" v-if="idx < selectedPath.roadmap.length - 1"></div>
              </div>
              <div class="roadmap-content">
                <div class="roadmap-header">
                  <span class="roadmap-title">{{ stage.title }}</span>
                  <span class="roadmap-duration">{{ stage.duration }}</span>
                </div>
                <p class="roadmap-desc">{{ stage.description }}</p>
                <div class="roadmap-resources" v-if="stage.resources && stage.resources.length">
                  <div
                    v-for="(res, ri) in stage.resources"
                    :key="ri"
                    class="resource-tag"
                  >
                    <el-icon><component :is="getResourceIcon(res.type)" /></el-icon>
                    {{ res.title }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="detail-actions">
          <el-button type="primary" size="large" @click="createPlan(selectedPath)">制定个人发展规划</el-button>
          <el-button size="large" @click="showRelatedCourses(selectedPath)">查看相关课程</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  Search, ArrowLeft, ArrowUp, ArrowDown, Minus,
  Monitor, DataLine, TrendCharts, Cpu, Lock,
  Reading, Notebook, OfficeBuilding, Document
} from '@element-plus/icons-vue'

export default {
  name: "CareerPath",
  components: {
    Search, ArrowLeft, ArrowUp, ArrowDown, Minus,
    Monitor, DataLine, TrendCharts, Cpu, Lock,
    Reading, Notebook, OfficeBuilding, Document
  },
  data() {
    return {
      searchQuery: '',
      selectedField: 'all',
      salaryRange: '',
      sortBy: 'popularity',
      selectedPath: null,
      fieldLabel: {
        development: '软件开发',
        ai: '人工智能',
        data: '数据科学',
        security: '网络安全'
      },
      salaryOptions: [
        { value: '', label: '不限' },
        { value: '10k-15k', label: '10k-15k' },
        { value: '15k-20k', label: '15k-20k' },
        { value: '20k-30k', label: '20k-30k' },
        { value: '30k+', label: '30k 以上' }
      ],
      careerPaths: [
        {
          id: 1,
          title: '前端开发工程师',
          description: '专注于网站和应用的用户界面和交互体验的开发与实现。',
          fullDescription: '前端开发工程师负责构建网站和应用程序的用户界面，确保用户体验流畅和响应迅速。他们使用 HTML、CSS 和 JavaScript 等技术，结合现代前端框架如 React、Vue 或 Angular 来开发交互式网页应用。前端开发者需要关注网站性能优化、浏览器兼容性和响应式设计，确保应用在各种设备上都能良好运行。',
          color: 'linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%)',
          icon: 'Monitor',
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
              description: '学习 HTML、CSS 和 JavaScript 基础，理解 Web 工作原理',
              completed: true,
              resources: [
                { type: 'course', title: 'Web开发基础课程' },
                { type: 'book', title: 'JavaScript高级程序设计' }
              ]
            },
            {
              title: '学习框架',
              duration: '3-4个月',
              description: '学习 React 或 Vue 等主流前端框架，掌握组件化开发',
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
          color: 'linear-gradient(135deg, #064e3b 0%, #10b981 100%)',
          icon: 'DataLine',
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
          description: '设计和实现机器学习模型和算法，将 AI 技术应用到实际业务中。',
          color: 'linear-gradient(135deg, #78350f 0%, #f59e0b 100%)',
          icon: 'TrendCharts',
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
          color: 'linear-gradient(135deg, #4c1d95 0%, #a855f7 100%)',
          icon: 'Cpu',
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
          color: 'linear-gradient(135deg, #1f2937 0%, #6b7280 100%)',
          icon: 'Lock',
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
      let result = this.careerPaths
      if (this.selectedField !== 'all') {
        result = result.filter(p => p.field === this.selectedField)
      }
      if (this.salaryRange) {
        const minKey = this.salaryRange.split('-')[0]
        result = result.filter(p => p.salary.includes(minKey))
      }
      if (this.searchQuery) {
        const q = this.searchQuery.toLowerCase()
        result = result.filter(p =>
          p.title.toLowerCase().includes(q) ||
          p.description.toLowerCase().includes(q)
        )
      }
      const sorted = [...result]
      if (this.sortBy === 'salary') {
        sorted.sort((a, b) => parseInt(b.salary) - parseInt(a.salary))
      } else if (this.sortBy === 'prospect') {
        sorted.sort((a, b) => b.trend - a.trend)
      } else {
        sorted.sort((a, b) => b.match - a.match)
      }
      return sorted
    }
  },
  methods: {
    selectCareerPath(path) {
      this.selectedPath = path
      this.$nextTick(() => window.scrollTo({ top: 0, behavior: 'smooth' }))
    },
    createPlan(path) {
      this.$message({ message: `即将为您制定"${path.title}"的职业发展规划`, type: 'success' })
    },
    showRelatedCourses(path) {
      this.$message({ message: `查看与"${path.title}"相关的课程`, type: 'info' })
    },
    getTrendIcon(trend) {
      if (trend > 0) return 'ArrowUp'
      if (trend < 0) return 'ArrowDown'
      return 'Minus'
    },
    getTrendColor(trend) {
      if (trend > 15) return '#10b981'
      if (trend > 0) return '#f59e0b'
      return '#ef4444'
    },
    getMatchClass(match) {
      if (match >= 80) return 'badge-high'
      if (match >= 60) return 'badge-mid'
      return 'badge-low'
    },
    getResourceIcon(type) {
      const map = {
        course: 'Reading',
        book: 'Notebook',
        project: 'Document',
        internship: 'OfficeBuilding'
      }
      return map[type] || 'Document'
    }
  }
}
</script>

<style scoped>
.career-container {
  padding: 28px 24px;
  min-height: 100%;
}

/* ── Header ── */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.page-title {
  font-size: 22px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.page-subtitle {
  font-size: 13px;
  color: #94a3b8;
}

.search-wrap {
  width: 300px;
}

/* ── Filters ── */
.filters-panel {
  background: #fff;
  border-radius: 10px;
  padding: 16px 20px;
  margin-bottom: 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

.filter-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.filter-row-selects {
  gap: 24px;
}

.select-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-label {
  font-size: 13px;
  color: #64748b;
  white-space: nowrap;
  min-width: 44px;
}

.filter-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.filter-tag {
  padding: 4px 14px;
  border-radius: 20px;
  font-size: 13px;
  color: #64748b;
  background: #f1f5f9;
  cursor: pointer;
  transition: all 0.2s;
  user-select: none;
}

.filter-tag:hover {
  background: #e2e8f0;
  color: #334155;
}

.filter-tag.active {
  background: #0ea5e9;
  color: #fff;
}

.filter-divider {
  height: 1px;
  background: #f1f5f9;
  margin: 12px 0;
}

/* ── Career Grid ── */
.career-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.career-card {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 12px rgba(0,0,0,0.04);
  cursor: pointer;
  transition: transform 0.22s ease, box-shadow 0.22s ease;
  display: flex;
  flex-direction: column;
}

.career-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 28px rgba(0,0,0,0.11);
}

.card-top {
  height: 110px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.card-top-icon {
  font-size: 44px;
  color: rgba(255,255,255,0.9);
}

.card-match-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(0,0,0,0.25);
  backdrop-filter: blur(4px);
  color: #fff;
  font-size: 11px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 12px;
}

.card-body {
  padding: 16px;
  flex: 1;
}

.career-title {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 8px;
}

.career-desc {
  font-size: 13px;
  color: #64748b;
  line-height: 1.6;
  margin: 0 0 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.career-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  border-top: 1px solid #f1f5f9;
  padding-top: 12px;
}

.stat-item {
  text-align: center;
}

.stat-label {
  display: block;
  font-size: 11px;
  color: #94a3b8;
  margin-bottom: 4px;
}

.stat-value {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 3px;
  font-size: 13px;
  font-weight: 600;
  color: #334155;
}

.trend-value {
  font-size: 12px;
}

.card-footer {
  padding: 10px 16px;
  border-top: 1px solid #f1f5f9;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* ── Detail ── */
.career-detail {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.06);
}

.detail-hero {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 28px 28px;
  position: relative;
}

.hero-icon {
  font-size: 52px;
  color: rgba(255,255,255,0.9);
  flex-shrink: 0;
}

.hero-info {
  flex: 1;
}

.hero-title {
  font-size: 22px;
  font-weight: 700;
  color: #fff;
  margin: 0 0 10px;
}

.hero-badges {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.match-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  color: #fff;
}

.badge-high { background: rgba(16,185,129,0.85); }
.badge-mid  { background: rgba(245,158,11,0.85); }
.badge-low  { background: rgba(239,68,68,0.85); }

.field-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  background: rgba(255,255,255,0.2);
  color: #fff;
}

.back-btn {
  background: rgba(255,255,255,0.15);
  border: 1px solid rgba(255,255,255,0.3);
  color: #fff;
  flex-shrink: 0;
}

.back-btn:hover {
  background: rgba(255,255,255,0.25);
  color: #fff;
}

.detail-body {
  padding: 28px;
}

.detail-section {
  margin-bottom: 32px;
}

.detail-desc {
  font-size: 14px;
  color: #475569;
  line-height: 1.8;
  margin: 0 0 20px;
}

.overview-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.overview-stat {
  background: #f8fafc;
  border-radius: 10px;
  padding: 16px;
  text-align: center;
  border: 1px solid #e2e8f0;
}

.ov-label {
  font-size: 12px;
  color: #94a3b8;
  margin-bottom: 8px;
}

.ov-value {
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
}

.section-title {
  font-size: 17px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 16px;
  padding-bottom: 10px;
  border-bottom: 2px solid #f1f5f9;
}

.skill-groups {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.skill-group-title {
  font-size: 14px;
  font-weight: 600;
  color: #64748b;
  margin: 0 0 14px;
}

.skill-item {
  margin-bottom: 14px;
}

.skill-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.skill-name {
  font-size: 13px;
  font-weight: 500;
  color: #334155;
}

.skill-pcts {
  display: flex;
  gap: 10px;
  font-size: 11px;
}

.current-pct { color: #0ea5e9; }
.required-pct { color: #94a3b8; }

.skill-track {
  height: 6px;
  background: #e2e8f0;
  border-radius: 3px;
  position: relative;
  overflow: hidden;
}

.skill-required {
  position: absolute;
  height: 100%;
  background: #e2e8f0;
  border-radius: 3px;
}

.skill-current {
  position: absolute;
  height: 100%;
  background: linear-gradient(90deg, #38bdf8, #0ea5e9);
  border-radius: 3px;
  z-index: 1;
}

/* ── Roadmap ── */
.roadmap {
  padding: 4px 0;
}

.roadmap-item {
  display: flex;
  gap: 16px;
  margin-bottom: 28px;
}

.roadmap-item:last-child {
  margin-bottom: 0;
}

.roadmap-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
}

.roadmap-dot {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #cbd5e1;
  border: 2px solid #fff;
  box-shadow: 0 0 0 2px #cbd5e1;
  z-index: 1;
  flex-shrink: 0;
}

.roadmap-dot.completed {
  background: #10b981;
  box-shadow: 0 0 0 2px #10b981;
}

.roadmap-line {
  flex: 1;
  width: 2px;
  background: #e2e8f0;
  margin: 4px 0;
  min-height: 24px;
}

.roadmap-content {
  flex: 1;
  padding-bottom: 4px;
}

.roadmap-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.roadmap-title {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
}

.roadmap-duration {
  font-size: 12px;
  color: #94a3b8;
  background: #f1f5f9;
  padding: 2px 10px;
  border-radius: 10px;
}

.roadmap-desc {
  font-size: 13px;
  color: #64748b;
  line-height: 1.6;
  margin: 0 0 10px;
}

.roadmap-resources {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.resource-tag {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: #475569;
  background: #f1f5f9;
  padding: 4px 10px;
  border-radius: 6px;
}

.resource-tag .el-icon {
  font-size: 13px;
  color: #0ea5e9;
}

/* ── Actions ── */
.detail-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  padding-top: 8px;
}

@media (max-width: 992px) {
  .skill-groups {
    grid-template-columns: 1fr;
  }
  .overview-stats {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  .search-wrap { width: 100%; }
  .career-grid { grid-template-columns: 1fr; }
  .detail-hero { flex-wrap: wrap; }
  .back-btn { width: 100%; }
}
</style>
