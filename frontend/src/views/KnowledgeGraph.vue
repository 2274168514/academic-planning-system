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
