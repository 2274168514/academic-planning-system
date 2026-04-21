<template>
  <div class="courses-container">
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">课程中心</h1>
        <span class="course-count">共 {{ courses.length }} 门课程</span>
      </div>
      <div class="search-wrap">
        <el-input
          v-model="searchQuery"
          placeholder="搜索课程名称或关键词"
          @input="searchCourses"
          clearable
          size="large"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>
    </div>

    <div class="filters-panel">
      <div class="filter-row">
        <span class="filter-label">学科领域</span>
        <div class="filter-tags">
          <span
            v-for="cat in categoryOptions"
            :key="cat.value"
            class="filter-tag"
            :class="{ active: selectedCategory === cat.value }"
            @click="filterByCategory(cat.value)"
          >{{ cat.label }}</span>
        </div>
      </div>
      <div class="filter-divider"></div>
      <div class="filter-row">
        <span class="filter-label">难度等级</span>
        <div class="filter-tags">
          <span class="filter-tag" :class="{ active: selectedDifficulty === 'all' }" @click="filterByDifficulty('all')">全部</span>
          <span class="filter-tag diff-beginner" :class="{ active: selectedDifficulty === 'beginner' }" @click="filterByDifficulty('beginner')">入门</span>
          <span class="filter-tag diff-intermediate" :class="{ active: selectedDifficulty === 'intermediate' }" @click="filterByDifficulty('intermediate')">中级</span>
          <span class="filter-tag diff-advanced" :class="{ active: selectedDifficulty === 'advanced' }" @click="filterByDifficulty('advanced')">高级</span>
        </div>
      </div>
    </div>

    <div class="result-bar">
      <span class="result-count">找到 {{ allFiltered.length }} 门课程</span>
    </div>

    <div class="course-list">
      <div v-if="allFiltered.length === 0" class="empty-state">
        <el-icon class="empty-icon"><Document /></el-icon>
        <p class="empty-text">没有找到符合条件的课程</p>
        <el-button type="primary" link @click="resetFilters">清除筛选条件</el-button>
      </div>

      <div v-else class="course-grid">
        <div
          v-for="course in filteredCourses"
          :key="course.id"
          class="course-card"
          @click="viewCourseDetail(course.id)"
        >
          <div class="course-banner" :style="{ background: categoryConfig[course.category].gradient }">
            <el-icon class="banner-icon"><component :is="categoryConfig[course.category].icon" /></el-icon>
            <span class="diff-badge" :class="'diff-' + course.difficulty">{{ difficultyText[course.difficulty] }}</span>
          </div>
          <div class="course-body">
            <div class="category-label">{{ categoryLabel[course.category] }}</div>
            <h3 class="course-title">{{ course.title }}</h3>
            <p class="course-desc">{{ course.description }}</p>
            <div class="course-meta">
              <span class="meta-item">
                <el-icon><User /></el-icon>
                <span>{{ course.instructor }}</span>
              </span>
              <span class="meta-item">
                <el-icon><Tickets /></el-icon>
                <span>{{ course.credits }} 学分</span>
              </span>
            </div>
            <div v-if="course.enrolled" class="progress-wrap">
              <div class="progress-header">
                <span class="progress-label">学习进度</span>
                <span class="progress-pct">{{ course.progress }}%</span>
              </div>
              <div class="progress-track">
                <div class="progress-fill" :style="{ width: course.progress + '%' }"></div>
              </div>
            </div>
            <div class="course-footer">
              <el-tag v-if="course.enrolled" type="success" size="small" effect="plain">已选课</el-tag>
              <el-tag v-else size="small" effect="plain">未选课</el-tag>
              <el-button
                v-if="!course.enrolled"
                type="primary"
                size="small"
                @click.stop
              >选课</el-button>
              <el-button
                v-else
                type="primary"
                plain
                size="small"
                @click.stop
              >继续学习</el-button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="pagination" v-if="totalPages > 1">
      <el-button :disabled="currentPage === 1" @click="prevPage" circle size="small">
        <el-icon><ArrowLeft /></el-icon>
      </el-button>
      <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
      <el-button :disabled="currentPage === totalPages" @click="nextPage" circle size="small">
        <el-icon><ArrowRight /></el-icon>
      </el-button>
    </div>
  </div>
</template>

<script>
import {
  Search, User, Tickets, Document, ArrowLeft, ArrowRight,
  Monitor, DataAnalysis, Setting, Reading
} from '@element-plus/icons-vue'

export default {
  name: "Courses",
  components: { Search, User, Tickets, Document, ArrowLeft, ArrowRight, Monitor, DataAnalysis, Setting, Reading },
  data() {
    return {
      searchQuery: '',
      selectedCategory: 'all',
      selectedDifficulty: 'all',
      currentPage: 1,
      coursesPerPage: 9,
      difficultyText: {
        beginner: '入门',
        intermediate: '中级',
        advanced: '高级'
      },
      categoryLabel: {
        'computer-science': '计算机科学',
        'mathematics': '数学',
        'engineering': '工程学',
        'humanities': '人文社科'
      },
      categoryOptions: [
        { value: 'all', label: '全部' },
        { value: 'computer-science', label: '计算机科学' },
        { value: 'mathematics', label: '数学' },
        { value: 'engineering', label: '工程学' },
        { value: 'humanities', label: '人文社科' }
      ],
      categoryConfig: {
        'computer-science': {
          gradient: 'linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%)',
          icon: 'Monitor'
        },
        'mathematics': {
          gradient: 'linear-gradient(135deg, #78350f 0%, #f59e0b 100%)',
          icon: 'DataAnalysis'
        },
        'engineering': {
          gradient: 'linear-gradient(135deg, #3b0764 0%, #a855f7 100%)',
          icon: 'Setting'
        },
        'humanities': {
          gradient: 'linear-gradient(135deg, #064e3b 0%, #10b981 100%)',
          icon: 'Reading'
        }
      },
      courses: [
        {
          id: 1,
          title: '数据结构与算法',
          description: '掌握计算机科学中最基础的数据结构和算法设计原理',
          instructor: '张教授',
          credits: 4,
          category: 'computer-science',
          difficulty: 'intermediate',
          enrolled: true,
          progress: 65
        },
        {
          id: 2,
          title: '高等数学',
          description: '学习微积分、线性代数等高等数学基础知识',
          instructor: '李教授',
          credits: 5,
          category: 'mathematics',
          difficulty: 'beginner',
          enrolled: true,
          progress: 85
        },
        {
          id: 3,
          title: '计算机网络',
          description: '深入了解网络协议、架构及网络应用开发',
          instructor: '王教授',
          credits: 3,
          category: 'computer-science',
          difficulty: 'intermediate',
          enrolled: false,
          progress: 0
        },
        {
          id: 4,
          title: '操作系统原理',
          description: '探索现代操作系统的设计与实现',
          instructor: '刘教授',
          credits: 4,
          category: 'computer-science',
          difficulty: 'advanced',
          enrolled: false,
          progress: 0
        },
        {
          id: 5,
          title: '工程伦理学',
          description: '讨论工程实践中的伦理道德问题与职业责任',
          instructor: '赵教授',
          credits: 2,
          category: 'humanities',
          difficulty: 'beginner',
          enrolled: true,
          progress: 30
        },
        {
          id: 6,
          title: '机械设计基础',
          description: '学习机械零部件设计及力学分析方法',
          instructor: '钱教授',
          credits: 3,
          category: 'engineering',
          difficulty: 'intermediate',
          enrolled: false,
          progress: 0
        }
      ]
    }
  },
  computed: {
    allFiltered() {
      let result = this.courses
      if (this.searchQuery) {
        const q = this.searchQuery.toLowerCase()
        result = result.filter(c =>
          c.title.toLowerCase().includes(q) ||
          c.description.toLowerCase().includes(q)
        )
      }
      if (this.selectedCategory !== 'all') {
        result = result.filter(c => c.category === this.selectedCategory)
      }
      if (this.selectedDifficulty !== 'all') {
        result = result.filter(c => c.difficulty === this.selectedDifficulty)
      }
      return result
    },
    filteredCourses() {
      const start = (this.currentPage - 1) * this.coursesPerPage
      return this.allFiltered.slice(start, start + this.coursesPerPage)
    },
    totalPages() {
      return Math.max(1, Math.ceil(this.allFiltered.length / this.coursesPerPage))
    }
  },
  methods: {
    searchCourses() {
      this.currentPage = 1
    },
    filterByCategory(category) {
      this.selectedCategory = category
      this.currentPage = 1
    },
    filterByDifficulty(difficulty) {
      this.selectedDifficulty = difficulty
      this.currentPage = 1
    },
    resetFilters() {
      this.searchQuery = ''
      this.selectedCategory = 'all'
      this.selectedDifficulty = 'all'
      this.currentPage = 1
    },
    viewCourseDetail(courseId) {
      this.$router.push(`/courses/${courseId}`)
    },
    prevPage() {
      if (this.currentPage > 1) this.currentPage--
    },
    nextPage() {
      if (this.currentPage < this.totalPages) this.currentPage++
    }
  }
}
</script>

<style scoped>
.courses-container {
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
  align-items: baseline;
  gap: 12px;
}

.page-title {
  font-size: 22px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.course-count {
  font-size: 13px;
  color: #94a3b8;
}

.search-wrap {
  width: 320px;
}

/* ── Filters ── */
.filters-panel {
  background: #fff;
  border-radius: 10px;
  padding: 16px 20px;
  margin-bottom: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

.filter-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.filter-label {
  font-size: 13px;
  color: #64748b;
  white-space: nowrap;
  min-width: 60px;
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

.diff-beginner.active { background: #10b981; }
.diff-intermediate.active { background: #f59e0b; }
.diff-advanced.active { background: #ef4444; }

.filter-divider {
  height: 1px;
  background: #f1f5f9;
  margin: 12px 0;
}

/* ── Result bar ── */
.result-bar {
  margin-bottom: 16px;
}

.result-count {
  font-size: 13px;
  color: #94a3b8;
}

/* ── Grid ── */
.course-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.course-card {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 12px rgba(0,0,0,0.04);
  cursor: pointer;
  transition: transform 0.22s ease, box-shadow 0.22s ease;
}

.course-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.10);
}

/* ── Banner ── */
.course-banner {
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.banner-icon {
  font-size: 48px;
  color: rgba(255,255,255,0.85);
}

.diff-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  color: #fff;
  background: rgba(0,0,0,0.25);
  backdrop-filter: blur(4px);
}

.diff-badge.diff-beginner  { background: rgba(16,185,129,0.75); }
.diff-badge.diff-intermediate { background: rgba(245,158,11,0.75); }
.diff-badge.diff-advanced  { background: rgba(239,68,68,0.75); }

/* ── Body ── */
.course-body {
  padding: 16px;
}

.category-label {
  font-size: 11px;
  font-weight: 600;
  color: #0ea5e9;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 6px;
}

.course-title {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 8px;
  line-height: 1.4;
}

.course-desc {
  font-size: 13px;
  color: #64748b;
  line-height: 1.6;
  margin: 0 0 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.course-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #94a3b8;
}

.meta-item .el-icon {
  font-size: 13px;
}

/* ── Progress ── */
.progress-wrap {
  margin-bottom: 12px;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
}

.progress-label {
  font-size: 12px;
  color: #94a3b8;
}

.progress-pct {
  font-size: 12px;
  font-weight: 600;
  color: #0ea5e9;
}

.progress-track {
  height: 5px;
  background: #e2e8f0;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #38bdf8, #0ea5e9);
  border-radius: 3px;
  transition: width 0.4s ease;
}

/* ── Footer ── */
.course-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 4px;
}

/* ── Empty state ── */
.empty-state {
  text-align: center;
  padding: 60px 0;
  color: #94a3b8;
}

.empty-icon {
  font-size: 52px;
  display: block;
  margin: 0 auto 12px;
}

.empty-text {
  font-size: 14px;
  margin: 0 0 12px;
}

/* ── Pagination ── */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin-top: 32px;
}

.page-info {
  font-size: 13px;
  color: #64748b;
  min-width: 60px;
  text-align: center;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  .search-wrap {
    width: 100%;
  }
  .course-grid {
    grid-template-columns: 1fr;
  }
}
</style>
