<template>
  <div class="courses-container">
    <div class="page-header">
      <h1 class="page-title">课程中心</h1>
      <div class="search-bar">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="搜索课程名称或关键词" 
          @input="searchCourses"
        />
        <button class="btn-search">
          <i class="el-icon-search"></i>
        </button>
      </div>
    </div>
    
    <div class="filters">
      <div class="filter-group">
        <span class="filter-label">学科领域：</span>
        <span 
          class="filter-item" 
          :class="{ active: selectedCategory === 'all' }" 
          @click="filterByCategory('all')"
        >全部</span>
        <span 
          class="filter-item" 
          :class="{ active: selectedCategory === 'computer-science' }" 
          @click="filterByCategory('computer-science')"
        >计算机科学</span>
        <span 
          class="filter-item" 
          :class="{ active: selectedCategory === 'mathematics' }" 
          @click="filterByCategory('mathematics')"
        >数学</span>
        <span 
          class="filter-item" 
          :class="{ active: selectedCategory === 'engineering' }" 
          @click="filterByCategory('engineering')"
        >工程学</span>
        <span 
          class="filter-item" 
          :class="{ active: selectedCategory === 'humanities' }" 
          @click="filterByCategory('humanities')"
        >人文社科</span>
      </div>
      
      <div class="filter-group">
        <span class="filter-label">难度等级：</span>
        <span 
          class="filter-item" 
          :class="{ active: selectedDifficulty === 'all' }" 
          @click="filterByDifficulty('all')"
        >全部</span>
        <span 
          class="filter-item" 
          :class="{ active: selectedDifficulty === 'beginner' }" 
          @click="filterByDifficulty('beginner')"
        >入门</span>
        <span 
          class="filter-item" 
          :class="{ active: selectedDifficulty === 'intermediate' }" 
          @click="filterByDifficulty('intermediate')"
        >中级</span>
        <span 
          class="filter-item" 
          :class="{ active: selectedDifficulty === 'advanced' }" 
          @click="filterByDifficulty('advanced')"
        >高级</span>
      </div>
    </div>
    
    <div class="course-list">
      <div v-if="filteredCourses.length === 0" class="no-courses">
        <i class="el-icon-document"></i>
        <p>没有找到符合条件的课程</p>
      </div>
      
      <div v-else class="course-grid">
        <div v-for="course in filteredCourses" :key="course.id" class="course-card" @click="viewCourseDetail(course.id)">
          <div class="course-image" :style="{ 'background-image': `url(${course.image})` }">
            <div class="course-difficulty" :class="course.difficulty">
              {{ difficultyText[course.difficulty] }}
            </div>
          </div>
          <div class="course-info">
            <h3 class="course-title">{{ course.title }}</h3>
            <p class="course-desc">{{ course.description }}</p>
            <div class="course-meta">
              <span class="course-instructor">
                <i class="el-icon-user"></i> {{ course.instructor }}
              </span>
              <span class="course-credits">
                <i class="el-icon-data-analysis"></i> {{ course.credits }}学分
              </span>
            </div>
            <div class="course-progress" v-if="course.enrolled">
              <div class="progress-bar">
                <div class="progress-inner" :style="{ width: course.progress + '%' }"></div>
              </div>
              <span class="progress-text">{{ course.progress }}% 完成</span>
            </div>
            <div class="course-actions">
              <button class="btn-enroll" v-if="!course.enrolled">选课</button>
              <button class="btn-continue" v-else>继续学习</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="pagination">
      <button class="btn-page" :disabled="currentPage === 1" @click="prevPage">
        <i class="el-icon-arrow-left"></i>
      </button>
      <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
      <button class="btn-page" :disabled="currentPage === totalPages" @click="nextPage">
        <i class="el-icon-arrow-right"></i>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "Courses",
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
      // 模拟课程数据
      courses: [
        {
          id: 1,
          title: '数据结构与算法',
          description: '掌握计算机科学中最基础的数据结构和算法设计原理',
          instructor: '张教授',
          credits: 4,
          category: 'computer-science',
          difficulty: 'intermediate',
          image: 'https://via.placeholder.com/300x180?text=数据结构与算法',
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
          image: 'https://via.placeholder.com/300x180?text=高等数学',
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
          image: 'https://via.placeholder.com/300x180?text=计算机网络',
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
          image: 'https://via.placeholder.com/300x180?text=操作系统原理',
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
          image: 'https://via.placeholder.com/300x180?text=工程伦理学',
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
          image: 'https://via.placeholder.com/300x180?text=机械设计基础',
          enrolled: false,
          progress: 0
        }
      ]
    }
  },
  computed: {
    filteredCourses() {
      let result = this.courses;
      
      // 根据搜索关键词筛选
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(course => 
          course.title.toLowerCase().includes(query) || 
          course.description.toLowerCase().includes(query)
        );
      }
      
      // 根据分类筛选
      if (this.selectedCategory !== 'all') {
        result = result.filter(course => course.category === this.selectedCategory);
      }
      
      // 根据难度筛选
      if (this.selectedDifficulty !== 'all') {
        result = result.filter(course => course.difficulty === this.selectedDifficulty);
      }
      
      // 分页
      const startIndex = (this.currentPage - 1) * this.coursesPerPage;
      return result.slice(startIndex, startIndex + this.coursesPerPage);
    },
    totalPages() {
      // 计算总页数
      return Math.ceil(this.courses.length / this.coursesPerPage);
    }
  },
  methods: {
    searchCourses() {
      // 搜索时重置页码
      this.currentPage = 1;
    },
    filterByCategory(category) {
      this.selectedCategory = category;
      this.currentPage = 1;
    },
    filterByDifficulty(difficulty) {
      this.selectedDifficulty = difficulty;
      this.currentPage = 1;
    },
    viewCourseDetail(courseId) {
      // 跳转到课程详情页
      this.$router.push(`/courses/${courseId}`);
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    }
  }
}
</script>

<style scoped>
.courses-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-title {
  font-size: 24px;
  margin: 0;
}

.search-bar {
  display: flex;
  width: 360px;
}

.search-bar input {
  flex: 1;
  padding: 10px 15px;
  border: 1px solid #dcdfe6;
  border-radius: 4px 0 0 4px;
  font-size: 14px;
}

.btn-search {
  background-color: #0066cc;
  color: white;
  border: none;
  border-radius: 0 4px 4px 0;
  padding: 0 15px;
  cursor: pointer;
}

.filters {
  background: white;
  border-radius: 4px;
  padding: 15px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.filter-group {
  margin-bottom: 10px;
}

.filter-group:last-child {
  margin-bottom: 0;
}

.filter-label {
  color: #606266;
  margin-right: 10px;
}

.filter-item {
  display: inline-block;
  padding: 6px 12px;
  margin-right: 8px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.filter-item:hover {
  background-color: #f5f7fa;
}

.filter-item.active {
  background-color: #e6f2ff;
  color: #0066cc;
}

.course-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.course-card {
  background: white;
  border-radius: 4px;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  transition: all 0.3s;
  cursor: pointer;
}

.course-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px 0 rgba(0, 0, 0, 0.1);
}

.course-image {
  height: 180px;
  background-size: cover;
  background-position: center;
  position: relative;
}

.course-difficulty {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 4px 8px;
  border-radius: 2px;
  font-size: 12px;
  color: white;
}

.course-difficulty.beginner {
  background-color: #67c23a;
}

.course-difficulty.intermediate {
  background-color: #e6a23c;
}

.course-difficulty.advanced {
  background-color: #f56c6c;
}

.course-info {
  padding: 15px;
}

.course-title {
  margin: 0 0 10px;
  font-size: 18px;
}

.course-desc {
  color: #666;
  margin: 0 0 15px;
  font-size: 14px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.5;
  height: 3em;
}

.course-meta {
  display: flex;
  justify-content: space-between;
  color: #909399;
  font-size: 13px;
  margin-bottom: 15px;
}

.course-progress {
  margin-bottom: 15px;
}

.progress-bar {
  height: 6px;
  background-color: #ebeef5;
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 5px;
}

.progress-inner {
  height: 100%;
  background-color: #0066cc;
  border-radius: 3px;
}

.progress-text {
  color: #606266;
  font-size: 12px;
}

.course-actions {
  text-align: center;
}

.btn-enroll, .btn-continue {
  width: 100%;
  padding: 8px 0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-enroll {
  background-color: #0066cc;
  color: white;
}

.btn-continue {
  background-color: #e6f2ff;
  color: #0066cc;
}

.no-courses {
  text-align: center;
  padding: 50px 0;
  color: #909399;
}

.no-courses i {
  font-size: 48px;
  margin-bottom: 10px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 30px;
}

.btn-page {
  border: 1px solid #dcdfe6;
  background-color: white;
  padding: 6px 12px;
  margin: 0 5px;
  border-radius: 4px;
  cursor: pointer;
}

.btn-page:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.page-info {
  color: #606266;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .search-bar {
    width: 100%;
    margin-top: 15px;
  }
  
  .course-grid {
    grid-template-columns: 1fr;
  }
}
</style>
