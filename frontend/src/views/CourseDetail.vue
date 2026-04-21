<template>
  <div class="course-detail-container">
    <div class="page-header">
      <div class="header-nav">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item :to="{ path: '/courses' }">课程中心</el-breadcrumb-item>
          <el-breadcrumb-item>{{ course.title }}</el-breadcrumb-item>
        </el-breadcrumb>
        <el-button icon="el-icon-back" size="small" @click="$router.push('/courses')">返回课程列表</el-button>
      </div>
      <h1 class="course-title">{{ course.title }}</h1>
      <div class="course-info">
        <div class="info-tag" v-if="course.category">
          <i class="el-icon-collection-tag"></i> {{ course.category }}
        </div>
        <div class="info-tag">
          <i class="el-icon-user"></i> {{ course.instructor }}
        </div>
        <div class="info-tag">
          <i class="el-icon-date"></i> {{ course.startDate }}
        </div>
        <div class="info-tag">
          <i class="el-icon-medal"></i> {{ course.level }}
        </div>
        <div class="info-tag">
          <i class="el-icon-reading"></i> {{ course.credits }}学分
        </div>
      </div>
    </div>
    
    <div class="course-content">
      <div class="main-content">
        <div class="course-intro">
          <div class="intro-header">
            <h2>课程介绍</h2>
            <div class="enrollment-status" v-if="course.enrolled">
              <el-progress
                :percentage="course.progress || 0"
                :stroke-width="12"
                :color="getProgressColor"
              ></el-progress>
              <span class="progress-text">{{ course.progress || 0 }}% 完成</span>
              <el-button type="primary" size="small" class="continue-btn" @click="continueLearning">继续学习</el-button>
            </div>
            <el-button v-else type="primary" @click="enrollCourse">选课</el-button>
          </div>
          
          <div class="intro-image" v-if="course.coverImage">
            <img :src="course.coverImage" :alt="course.title">
          </div>
          
          <div class="intro-text">
            {{ course.description }}
          </div>
          
          <div class="course-goals" v-if="course.learningGoals && course.learningGoals.length">
            <h3>学习目标</h3>
            <ul class="goal-list">
              <li v-for="(goal, index) in course.learningGoals" :key="index">
                <i class="el-icon-check"></i>
                <span>{{ goal }}</span>
              </li>
            </ul>
          </div>
        </div>
        
        <div class="course-outline">
          <h2>课程大纲</h2>
          <el-collapse v-model="activeChapters" accordion>
            <el-collapse-item v-for="(chapter, index) in course.chapters" :key="index" :title="chapter.title" :name="index">
              <div class="chapter-info">
                <div class="chapter-desc">{{ chapter.description }}</div>
                <div class="chapter-duration">
                  <i class="el-icon-timer"></i> {{ chapter.duration }}
                </div>
              </div>
              
              <div class="chapter-lessons">
                <div v-for="(lesson, lidx) in chapter.lessons" :key="lidx" class="lesson-item">
                  <div class="lesson-info">
                    <div class="lesson-icon">
                      <i :class="getLessonIcon(lesson.type)"></i>
                    </div>
                    <div class="lesson-detail">
                      <div class="lesson-name">{{ lesson.title }}</div>
                      <div class="lesson-duration">{{ lesson.duration }}</div>
                    </div>
                  </div>
                  <div class="lesson-actions">
                    <el-button 
                      size="mini" 
                      type="primary" 
                      plain 
                      :disabled="!course.enrolled"
                      @click="viewLesson(chapter, lesson)"
                    >
                      {{ lesson.completed ? '复习' : '学习' }}
                    </el-button>
                  </div>
                </div>
              </div>
            </el-collapse-item>
          </el-collapse>
        </div>
        
        <div class="instructor-info">
          <h2>授课教师</h2>
          <div class="instructor-card">
            <div class="instructor-avatar">
              <img :src="course.instructorAvatar || 'https://via.placeholder.com/100'" :alt="course.instructor">
            </div>
            <div class="instructor-detail">
              <div class="instructor-name">{{ course.instructor }}</div>
              <div class="instructor-title">{{ course.instructorTitle || '教授' }}</div>
              <div class="instructor-bio">{{ course.instructorBio || '专业领域教育工作者，在该领域有丰富的教学和实践经验。' }}</div>
            </div>
          </div>
        </div>
        
        <div class="course-reviews" v-if="course.reviews && course.reviews.length">
          <h2>学生评价</h2>
          <div class="review-summary">
            <div class="rating-box">
              <div class="rating-score">{{ course.averageRating || 4.8 }}</div>
              <div class="rating-stars">
                <i v-for="n in 5" :key="n" :class="n <= Math.round(course.averageRating || 4.8) ? 'el-icon-star-on' : 'el-icon-star-off'"></i>
              </div>
              <div class="rating-count">{{ course.reviews.length }}人评价</div>
            </div>
            <div class="rating-distribution">
              <div v-for="n in 5" :key="n" class="rating-bar">
                <div class="rating-label">{{ 6 - n }}星</div>
                <div class="rating-progress">
                  <div class="progress-bar" :style="{ width: getRatingPercentage(6 - n) + '%' }"></div>
                </div>
                <div class="rating-percent">{{ getRatingPercentage(6 - n) }}%</div>
              </div>
            </div>
          </div>
          
          <div class="review-list">
            <div v-for="(review, index) in course.reviews" :key="index" class="review-item">
              <div class="review-header">
                <div class="reviewer-avatar">
                  <img :src="review.avatar || 'https://via.placeholder.com/40'" :alt="review.name">
                </div>
                <div class="reviewer-info">
                  <div class="reviewer-name">{{ review.name }}</div>
                  <div class="review-date">{{ review.date }}</div>
                </div>
                <div class="review-rating">
                  <i v-for="n in 5" :key="n" :class="n <= review.rating ? 'el-icon-star-on' : 'el-icon-star-off'"></i>
                </div>
              </div>
              <div class="review-content">
                {{ review.content }}
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="side-content">
        <div class="course-action-card">
          <div class="action-header">
            <div class="course-price" v-if="course.price">{{ course.price }}</div>
            <div class="course-free" v-else>免费</div>
          </div>
          <div class="action-content">
            <div class="action-item">
              <i class="el-icon-time"></i>
              <span>总课时：{{ course.totalDuration || '48学时' }}</span>
            </div>
            <div class="action-item">
              <i class="el-icon-document"></i>
              <span>章节数：{{ course.chapters ? course.chapters.length : 8 }}</span>
            </div>
            <div class="action-item">
              <i class="el-icon-trophy"></i>
              <span>证书：{{ course.certificate ? '完成后颁发' : '无' }}</span>
            </div>
            <div class="action-item">
              <i class="el-icon-user"></i>
              <span>已有{{ course.studentCount || 256 }}人学习</span>
            </div>
          </div>
          <div class="action-buttons">
            <el-button v-if="!course.enrolled" type="primary" class="full-width-btn" @click="enrollCourse">选修课程</el-button>
            <el-button v-else type="success" class="full-width-btn" @click="continueLearning">继续学习</el-button>
            <el-button type="info" plain class="full-width-btn">添加到学习计划</el-button>
          </div>
        </div>
        
        <div class="prerequisites-card" v-if="course.prerequisites && course.prerequisites.length">
          <h3>先修要求</h3>
          <ul class="prerequisites-list">
            <li v-for="(prereq, index) in course.prerequisites" :key="index">
              <i class="el-icon-info"></i>
              <span>{{ prereq }}</span>
            </li>
          </ul>
        </div>
        
        <div class="related-courses-card" v-if="relatedCourses && relatedCourses.length">
          <h3>相关课程</h3>
          <div class="related-list">
            <div v-for="(relCourse, index) in relatedCourses" :key="index" class="related-course-item" @click="viewCourse(relCourse.id)">
              <div class="related-course-image">
                <img :src="relCourse.image" :alt="relCourse.title">
              </div>
              <div class="related-course-info">
                <div class="related-course-title">{{ relCourse.title }}</div>
                <div class="related-course-instructor">{{ relCourse.instructor }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CourseDetail',
  data() {
    return {
      courseId: null,
      activeChapters: [0], // 默认打开第一章
      course: {
        id: 1,
        title: '数据结构与算法',
        instructor: '张教授',
        instructorTitle: '计算机科学教授',
        instructorAvatar: 'https://via.placeholder.com/100',
        instructorBio: '计算机科学博士，拥有10年以上教学经验，主要研究领域包括算法设计、数据结构优化及其在大数据处理中的应用。',
        category: '计算机科学',
        level: '中级',
        credits: 4,
        startDate: '2023-09-01',
        endDate: '2024-01-15',
        enrolled: true,
        progress: 65,
        totalDuration: '48学时',
        studentCount: 328,
        certificate: true,
        coverImage: 'https://via.placeholder.com/800x400?text=数据结构与算法',
        description: '本课程系统介绍了计算机科学中最基础且最重要的数据结构和算法。通过学习各种数据结构（如数组、链表、栈、队列、树、图等）及其操作算法，学生将能够分析问题并选择最合适的数据结构来解决特定的问题。课程还涵盖了算法复杂度分析、排序和搜索算法、动态规划和贪心算法等内容，旨在培养学生的算法思维和问题解决能力。',
        averageRating: 4.7,
        learningGoals: [
          '理解和掌握基本数据结构的原理和实现',
          '分析算法的时间和空间复杂度',
          '能够根据问题特点选择合适的数据结构和算法',
          '掌握常见排序和搜索算法的设计与分析',
          '能够应用算法思想解决实际编程问题'
        ],
        prerequisites: [
          '编程基础（C/C++/Java等任一语言）',
          '离散数学基础知识',
          '基本的问题分析能力'
        ],
        chapters: [
          {
            title: '第一章：绪论',
            description: '介绍数据结构与算法的基本概念和重要性',
            duration: '4学时',
            lessons: [
              { title: '数据结构与算法导论', type: 'video', duration: '45分钟', completed: true },
              { title: '算法复杂度分析', type: 'video', duration: '50分钟', completed: true },
              { title: '基本数据结构概述', type: 'video', duration: '40分钟', completed: true },
              { title: '第一章测验', type: 'quiz', duration: '30分钟', completed: true }
            ]
          },
          {
            title: '第二章：线性表',
            description: '学习顺序表、链表等线性数据结构及其操作算法',
            duration: '8学时',
            lessons: [
              { title: '顺序表的实现与操作', type: 'video', duration: '55分钟', completed: true },
              { title: '单链表详解', type: 'video', duration: '60分钟', completed: true },
              { title: '双向链表与循环链表', type: 'video', duration: '45分钟', completed: true },
              { title: '线性表编程实验', type: 'lab', duration: '90分钟', completed: false },
              { title: '线性表应用案例分析', type: 'document', duration: '30分钟', completed: false },
              { title: '第二章测验', type: 'quiz', duration: '40分钟', completed: false }
            ]
          },
          {
            title: '第三章：栈与队列',
            description: '掌握栈和队列的概念、实现及应用',
            duration: '6学时',
            lessons: [
              { title: '栈的概念与实现', type: 'video', duration: '50分钟', completed: false },
              { title: '栈的应用：表达式求值', type: 'video', duration: '45分钟', completed: false },
              { title: '队列的概念与实现', type: 'video', duration: '50分钟', completed: false },
              { title: '栈与队列编程实验', type: 'lab', duration: '90分钟', completed: false },
              { title: '第三章测验', type: 'quiz', duration: '30分钟', completed: false }
            ]
          },
          {
            title: '第四章：树与二叉树',
            description: '学习树形结构及其操作算法',
            duration: '10学时',
            lessons: [
              { title: '树的基本概念', type: 'video', duration: '40分钟', completed: false },
              { title: '二叉树的性质与存储结构', type: 'video', duration: '55分钟', completed: false },
              { title: '二叉树的遍历算法', type: 'video', duration: '60分钟', completed: false },
              { title: '二叉搜索树', type: 'video', duration: '50分钟', completed: false },
              { title: '平衡二叉树', type: 'video', duration: '60分钟', completed: false },
              { title: '树与二叉树编程实验', type: 'lab', duration: '120分钟', completed: false },
              { title: '第四章测验', type: 'quiz', duration: '45分钟', completed: false }
            ]
          }
        ],
        reviews: [
          {
            name: '李明',
            avatar: 'https://via.placeholder.com/40?text=LM',
            date: '2023-11-10',
            rating: 5,
            content: '课程内容非常充实，老师讲解清晰，特别是对算法复杂度分析的部分讲解得很透彻，对我帮助很大。'
          },
          {
            name: '王静',
            avatar: 'https://via.placeholder.com/40?text=WJ',
            date: '2023-11-05',
            rating: 4,
            content: '老师的教学方法很好，课程难度适中，编程实验设计得很有挑战性，能学到很多实用技能。'
          },
          {
            name: '张伟',
            avatar: 'https://via.placeholder.com/40?text=ZW',
            date: '2023-10-28',
            rating: 5,
            content: '这门课程是我学过的最系统的数据结构课程，每个知识点都有配套的编程练习，很实用。'
          }
        ]
      },
      relatedCourses: [
        {
          id: 2,
          title: '算法设计与分析',
          instructor: '李教授',
          image: 'https://via.placeholder.com/100x70?text=算法设计'
        },
        {
          id: 3,
          title: '高级数据结构',
          instructor: '王教授',
          image: 'https://via.placeholder.com/100x70?text=高级数据'
        },
        {
          id: 4,
          title: '计算机算法实战',
          instructor: '刘教授',
          image: 'https://via.placeholder.com/100x70?text=算法实战'
        }
      ]
    }
  },
  created() {
    // 从路由参数获取课程ID
    this.courseId = this.$route.params.id;
    // 实际应用中应根据ID从API获取课程数据
    this.fetchCourseData();
  },
  methods: {
    fetchCourseData() {
      // 模拟API请求
      console.log('获取课程ID: ', this.courseId);
      // 实际应用中应该发起API请求获取课程数据
      // this.course = await apiService.getCourseById(this.courseId);
    },
    enrollCourse() {
      this.$confirm('确定要选修该课程吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'info'
      }).then(() => {
        // 实际应用中应调用API完成选课
        this.course.enrolled = true;
        this.course.progress = 0;
        this.$message({
          type: 'success',
          message: '选课成功!'
        });
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消选课'
        });          
      });
    },
    continueLearning() {
      // 获取当前学习进度，跳转到对应章节
      let nextChapter = 0;
      let nextLesson = 0;
      
      // 找到第一个未完成的课时
      outerLoop:
      for (let i = 0; i < this.course.chapters.length; i++) {
        const chapter = this.course.chapters[i];
        for (let j = 0; j < chapter.lessons.length; j++) {
          if (!chapter.lessons[j].completed) {
            nextChapter = i;
            nextLesson = j;
            break outerLoop;
          }
        }
      }
      
      // 实际应用中应跳转到学习界面
      this.$message({
        message: `继续学习: 第${nextChapter + 1}章 ${this.course.chapters[nextChapter].lessons[nextLesson].title}`,
        type: 'success'
      });
    },
    viewLesson(chapter, lesson) {
      // 实际应用中应跳转到课程学习界面
      this.$message({
        message: `开始学习: ${chapter.title} - ${lesson.title}`,
        type: 'info'
      });
    },
    viewCourse(courseId) {
      // 实际应用中应跳转到对应课程详情页
      this.$router.push(`/courses/${courseId}`);
    },
    getLessonIcon(type) {
      const icons = {
        'video': 'el-icon-video-camera',
        'document': 'el-icon-document',
        'quiz': 'el-icon-question',
        'lab': 'el-icon-cpu'
      };
      return icons[type] || 'el-icon-document';
    },
    getRatingPercentage(stars) {
      // 计算指定星级评价的百分比
      if (!this.course.reviews || this.course.reviews.length === 0) return 0;
      
      const count = this.course.reviews.filter(review => review.rating === stars).length;
      return Math.round((count / this.course.reviews.length) * 100);
    },
    getProgressColor(percentage) {
      if (percentage < 30) return '#909399';
      if (percentage < 70) return '#E6A23C';
      return '#67C23A';
    }
  }
}
</script>

<style scoped>
.course-detail-container {
  padding: 20px;
}

.page-header {
  margin-bottom: 30px;
}

.header-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.course-title {
  font-size: 28px;
  margin: 0 0 15px;
  color: #333;
}

.course-info {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.info-tag {
  display: flex;
  align-items: center;
  background: #f5f7fa;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 14px;
  color: #606266;
}

.info-tag i {
  margin-right: 6px;
  color: #409EFF;
}

.course-content {
  display: flex;
  gap: 30px;
}

.main-content {
  flex: 1;
}

.side-content {
  width: 300px;
}

.course-intro {
  background: white;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 30px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.intro-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.intro-header h2 {
  margin: 0;
  font-size: 20px;
}

.enrollment-status {
  display: flex;
  align-items: center;
  gap: 10px;
}

.progress-text {
  color: #606266;
  white-space: nowrap;
}

.intro-image {
  margin-bottom: 20px;
  border-radius: 8px;
  overflow: hidden;
}

.intro-image img {
  width: 100%;
  display: block;
}

.intro-text {
  color: #606266;
  line-height: 1.6;
  margin-bottom: 20px;
}

.course-goals h3 {
  font-size: 18px;
  margin-bottom: 15px;
}

.goal-list {
  padding: 0;
  list-style: none;
}

.goal-list li {
  display: flex;
  margin-bottom: 10px;
  color: #606266;
}

.goal-list li i {
  color: #67C23A;
  margin-right: 10px;
}

.course-outline {
  background: white;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 30px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.course-outline h2 {
  margin: 0 0 20px;
  font-size: 20px;
}

.chapter-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}

.chapter-desc {
  color: #606266;
}

.chapter-duration {
  color: #909399;
  white-space: nowrap;
}

.chapter-lessons {
  margin-left: 10px;
}

.lesson-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px dashed #ebeef5;
}

.lesson-item:last-child {
  border-bottom: none;
}

.lesson-info {
  display: flex;
  align-items: center;
}

.lesson-icon {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: #f0f2f5;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
  color: #409EFF;
}

.lesson-detail {
  flex: 1;
}

.lesson-name {
  font-weight: 500;
  margin-bottom: 4px;
}

.lesson-duration {
  font-size: 12px;
  color: #909399;
}

.instructor-info {
  background: white;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 30px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.instructor-info h2 {
  margin: 0 0 20px;
  font-size: 20px;
}

.instructor-card {
  display: flex;
  align-items: center;
}

.instructor-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 20px;
}

.instructor-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.instructor-detail {
  flex: 1;
}

.instructor-name {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 5px;
}

.instructor-title {
  color: #606266;
  margin-bottom: 10px;
}

.instructor-bio {
  color: #606266;
  line-height: 1.6;
}

.course-reviews {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.course-reviews h2 {
  margin: 0 0 20px;
  font-size: 20px;
}

.review-summary {
  display: flex;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
}

.rating-box {
  text-align: center;
  padding-right: 30px;
  border-right: 1px solid #ebeef5;
  margin-right: 30px;
}

.rating-score {
  font-size: 36px;
  font-weight: 700;
  color: #303133;
  margin-bottom: 5px;
}

.rating-stars {
  color: #E6A23C;
  font-size: 20px;
  margin-bottom: 5px;
}

.rating-count {
  color: #909399;
}

.rating-distribution {
  flex: 1;
}

.rating-bar {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.rating-label {
  width: 40px;
  text-align: right;
  margin-right: 10px;
  color: #606266;
}

.rating-progress {
  flex: 1;
  height: 8px;
  background: #f0f2f5;
  border-radius: 4px;
  overflow: hidden;
  margin-right: 10px;
}

.progress-bar {
  height: 100%;
  background: #E6A23C;
  border-radius: 4px;
}

.rating-percent {
  width: 40px;
  color: #909399;
}

.review-item {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.review-item:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.review-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.reviewer-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 10px;
}

.reviewer-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.reviewer-info {
  flex: 1;
}

.reviewer-name {
  font-weight: 500;
  margin-bottom: 2px;
}

.review-date {
  font-size: 12px;
  color: #909399;
}

.review-rating {
  color: #E6A23C;
}

.review-content {
  color: #606266;
  line-height: 1.6;
}

.course-action-card {
  background: white;
  border-radius: 8px;
  margin-bottom: 20px;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.action-header {
  padding: 20px;
  text-align: center;
  background: #f5f7fa;
}

.course-price {
  font-size: 28px;
  font-weight: 700;
  color: #F56C6C;
}

.course-free {
  font-size: 28px;
  font-weight: 700;
  color: #67C23A;
}

.action-content {
  padding: 15px 20px;
}

.action-item {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  color: #606266;
}

.action-item i {
  margin-right: 10px;
  color: #909399;
}

.action-buttons {
  padding: 0 20px 20px;
}

.full-width-btn {
  width: 100%;
  margin-bottom: 10px;
}

.full-width-btn:last-child {
  margin-bottom: 0;
}

.prerequisites-card, .related-courses-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.prerequisites-card h3, .related-courses-card h3 {
  margin: 0 0 15px;
  font-size: 16px;
}

.prerequisites-list {
  padding: 0;
  list-style: none;
}

.prerequisites-list li {
  display: flex;
  margin-bottom: 10px;
  color: #606266;
}

.prerequisites-list li i {
  color: #409EFF;
  margin-right: 10px;
}

.related-course-item {
  display: flex;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background-color 0.3s;
}

.related-course-item:hover {
  background-color: #f5f7fa;
}

.related-course-item:last-child {
  border-bottom: none;
}

.related-course-image {
  width: 100px;
  height: 70px;
  border-radius: 4px;
  overflow: hidden;
  margin-right: 10px;
}

.related-course-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.related-course-title {
  font-weight: 500;
  margin-bottom: 5px;
}

.related-course-instructor {
  font-size: 12px;
  color: #909399;
}

/* 响应式布局 */
@media (max-width: 992px) {
  .course-content {
    flex-direction: column;
  }
  
  .side-content {
    width: 100%;
    order: -1;
    margin-bottom: 30px;
  }
  
  .review-summary {
    flex-direction: column;
  }
  
  .rating-box {
    margin-bottom: 20px;
    padding-bottom: 20px;
    padding-right: 0;
    margin-right: 0;
    border-right: none;
    border-bottom: 1px solid #ebeef5;
  }
}

@media (max-width: 768px) {
  .intro-header, .chapter-info {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .enrollment-status, .chapter-duration {
    margin-top: 10px;
  }
  
  .lesson-item {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .lesson-actions {
    margin-top: 10px;
    align-self: flex-end;
  }
  
  .instructor-card {
    flex-direction: column;
    text-align: center;
  }
  
  .instructor-avatar {
    margin-right: 0;
    margin-bottom: 15px;
  }
}
</style>
