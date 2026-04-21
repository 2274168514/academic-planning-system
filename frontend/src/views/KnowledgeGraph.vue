<template>
  <div class="kg-wrapper">
    <!-- 工具栏 -->
    <div class="kg-toolbar">
      <div class="toolbar-search">
        <el-input
          v-model="searchText"
          placeholder="搜索课程..."
          clearable
          @input="onSearch"
          @clear="onSearch"
          class="dark-input"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>
      <div class="toolbar-filters">
        <button
          v-for="f in filters"
          :key="f.value"
          class="filter-btn"
          :class="{ active: filter === f.value }"
          @click="setFilter(f.value)"
        >{{ f.label }}</button>
      </div>
      <div class="toolbar-actions">
        <button class="action-btn" title="放大" @click="zoomIn">
          <el-icon><ZoomIn /></el-icon>
        </button>
        <button class="action-btn" title="缩小" @click="zoomOut">
          <el-icon><ZoomOut /></el-icon>
        </button>
        <button class="action-btn" title="重置视图" @click="resetView">
          <el-icon><RefreshRight /></el-icon>
        </button>
        <button class="action-btn" title="全屏" @click="toggleFullscreen">
          <el-icon><FullScreen /></el-icon>
        </button>
      </div>
    </div>

    <!-- 主体区域 -->
    <div class="kg-body" ref="bodyContainer">
      <!-- 图谱区域 -->
      <div class="kg-graph-wrap" ref="graphWrap">
        <div class="kg-graph" ref="graphContainer"></div>

        <!-- loading 遮罩 -->
        <div v-if="loading" class="kg-loading">
          <div class="loading-spinner"></div>
          <span>正在加载知识图谱...</span>
        </div>

        <!-- 图例 -->
        <div class="kg-legend">
          <div class="legend-item">
            <span class="legend-dot" style="background:#0ea5e9;"></span>
            <span>必修课程</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot" style="background:#10b981;"></span>
            <span>选修课程</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot" style="background:#a855f7;"></span>
            <span>知识点</span>
          </div>
          <div class="legend-item">
            <span class="legend-dot" style="background:#f59e0b;"></span>
            <span>技能</span>
          </div>
        </div>
      </div>

      <!-- 详情面板 -->
      <div class="kg-detail">
        <!-- 空状态 -->
        <template v-if="!selectedNode">
          <div class="detail-empty">
            <el-icon class="empty-icon"><Share /></el-icon>
            <p>点击节点查看详情</p>
            <p class="empty-sub">支持点击课程节点展开知识点和技能</p>
          </div>
        </template>

        <!-- Course 节点详情 -->
        <template v-else-if="selectedNode.node_type === 'Course'">
          <div class="detail-type-bar" :style="{ background: selectedNode.course_type === '必修' ? '#0ea5e9' : '#10b981' }"></div>
          <div class="detail-content">
            <div class="detail-header">
              <el-icon class="detail-type-icon"><Notebook /></el-icon>
              <div>
                <div class="detail-title">{{ selectedNode.label }}</div>
                <div class="detail-code">{{ selectedNode.id }}</div>
              </div>
              <el-tag
                size="small"
                :style="{
                  background: selectedNode.course_type === '必修' ? 'rgba(14,165,233,0.2)' : 'rgba(16,185,129,0.2)',
                  color: selectedNode.course_type === '必修' ? '#38bdf8' : '#34d399',
                  border: 'none'
                }"
              >{{ selectedNode.course_type }}</el-tag>
            </div>

            <div class="detail-divider"></div>

            <div class="detail-item">
              <span class="detail-key">学分</span>
              <span class="detail-val">{{ selectedNode.credit }} 学分</span>
            </div>
            <div class="detail-item">
              <span class="detail-key">院系</span>
              <span class="detail-val">{{ selectedNode.department }}</span>
            </div>
            <div class="detail-item" v-if="selectedNode.prerequisite">
              <span class="detail-key">先修课程</span>
              <span class="detail-val prereq">{{ getPrerequisiteNames(selectedNode.prerequisite) }}</span>
            </div>
            <div class="detail-item" v-else>
              <span class="detail-key">先修课程</span>
              <span class="detail-val muted">无</span>
            </div>

            <div class="detail-divider"></div>

            <div class="detail-desc">
              <div class="detail-key">课程简介</div>
              <div class="detail-desc-text">{{ selectedNode.description }}</div>
            </div>

            <div class="detail-divider"></div>

            <div class="detail-expand-state">
              <el-icon v-if="expandedNodes.has(selectedNode.id)" style="color:#10b981;"><CircleCheckFilled /></el-icon>
              <el-icon v-else style="color:#64748b;"><CirclePlusFilled /></el-icon>
              <span>{{ expandedNodes.has(selectedNode.id) ? '已展开知识点（点击节点可收起）' : '点击节点可展开知识点和技能' }}</span>
            </div>
          </div>
        </template>

        <!-- KnowledgePoint 节点详情 -->
        <template v-else-if="selectedNode.node_type === 'KnowledgePoint'">
          <div class="detail-type-bar" style="background:#a855f7;"></div>
          <div class="detail-content">
            <div class="detail-header">
              <el-icon class="detail-type-icon" style="color:#a855f7;"><Document /></el-icon>
              <div>
                <div class="detail-title">{{ selectedNode.label }}</div>
                <div class="detail-code">知识点</div>
              </div>
            </div>
            <div class="detail-divider"></div>
            <div class="detail-item" v-if="selectedNode.difficulty">
              <span class="detail-key">难度</span>
              <span class="detail-val">
                <span
                  class="difficulty-tag"
                  :style="difficultyStyle(selectedNode.difficulty)"
                >{{ selectedNode.difficulty }}</span>
              </span>
            </div>
            <div class="detail-desc" v-if="selectedNode.content">
              <div class="detail-key">内容</div>
              <div class="detail-desc-text">{{ selectedNode.content }}</div>
            </div>
          </div>
        </template>

        <!-- Skill 节点详情 -->
        <template v-else-if="selectedNode.node_type === 'Skill'">
          <div class="detail-type-bar" style="background:#f59e0b;"></div>
          <div class="detail-content">
            <div class="detail-header">
              <el-icon class="detail-type-icon" style="color:#f59e0b;"><Trophy /></el-icon>
              <div>
                <div class="detail-title">{{ selectedNode.label }}</div>
                <div class="detail-code">技能</div>
              </div>
            </div>
            <div class="detail-divider"></div>
            <div class="detail-desc" v-if="selectedNode.description">
              <div class="detail-key">描述</div>
              <div class="detail-desc-text">{{ selectedNode.description }}</div>
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import { Network, DataSet } from 'vis-network/standalone'
import {
  Search, ZoomIn, ZoomOut, RefreshRight, FullScreen,
  Share, Notebook, Document, Trophy, CircleCheckFilled, CirclePlusFilled
} from '@element-plus/icons-vue'

const BASE_URL = 'http://localhost:5000'

// MOCK 降级数据
const MOCK_NODES = [
  { id: 'CS101', label: '计算机导论', credit: 3, course_type: '必修', department: '计算机科学与技术', description: '计算机科学的基础课程', prerequisite: '', node_type: 'Course' },
  { id: 'CS102', label: '程序设计基础', credit: 4, course_type: '必修', department: '计算机科学与技术', description: '介绍基本的程序设计概念和方法，使用C/C++语言。', prerequisite: '', node_type: 'Course' },
  { id: 'CS201', label: '数据结构', credit: 4, course_type: '必修', department: '计算机科学与技术', description: '介绍基本的数据结构和算法，包括数组、链表、栈、队列、树、图等。', prerequisite: 'CS102', node_type: 'Course' },
  { id: 'CS301', label: '算法设计与分析', credit: 3, course_type: '必修', department: '计算机科学与技术', description: '介绍常见的算法设计技术和分析方法。', prerequisite: 'CS201', node_type: 'Course' },
  { id: 'CS302', label: '操作系统', credit: 4, course_type: '必修', department: '计算机科学与技术', description: '介绍操作系统的基本概念、原理和实现方法。', prerequisite: 'CS201', node_type: 'Course' },
  { id: 'CS303', label: '计算机网络', credit: 3, course_type: '必修', department: '计算机科学与技术', description: '介绍计算机网络的基本概念、原理和协议。', prerequisite: 'CS101', node_type: 'Course' },
  { id: 'CS304', label: '数据库系统', credit: 4, course_type: '必修', department: '计算机科学与技术', description: '介绍数据库系统的基本概念、原理和实现方法。', prerequisite: 'CS201', node_type: 'Course' },
  { id: 'CS401', label: '软件工程', credit: 3, course_type: '必修', department: '计算机科学与技术', description: '介绍软件开发的原则、方法和工具。', prerequisite: 'CS304', node_type: 'Course' },
  { id: 'CS402', label: '人工智能', credit: 3, course_type: '选修', department: '计算机科学与技术', description: '介绍人工智能的基本概念、原理和应用。', prerequisite: 'CS301', node_type: 'Course' },
  { id: 'CS403', label: '机器学习', credit: 3, course_type: '选修', department: '计算机科学与技术', description: '介绍机器学习的基本概念、原理和算法。', prerequisite: 'CS402', node_type: 'Course' },
  { id: 'CS404', label: '深度学习', credit: 3, course_type: '选修', department: '计算机科学与技术', description: '介绍深度学习的基本概念、原理和模型。', prerequisite: 'CS403', node_type: 'Course' },
  { id: 'CS405', label: '计算机图形学', credit: 3, course_type: '选修', department: '计算机科学与技术', description: '介绍计算机图形学的基本概念、原理和算法。', prerequisite: 'CS201', node_type: 'Course' },
]
const MOCK_EDGES = [
  { from: 'CS102', to: 'CS201', relation: 'PREREQUISITE_OF' },
  { from: 'CS201', to: 'CS301', relation: 'PREREQUISITE_OF' },
  { from: 'CS201', to: 'CS302', relation: 'PREREQUISITE_OF' },
  { from: 'CS101', to: 'CS303', relation: 'PREREQUISITE_OF' },
  { from: 'CS201', to: 'CS304', relation: 'PREREQUISITE_OF' },
  { from: 'CS304', to: 'CS401', relation: 'PREREQUISITE_OF' },
  { from: 'CS301', to: 'CS402', relation: 'PREREQUISITE_OF' },
  { from: 'CS402', to: 'CS403', relation: 'PREREQUISITE_OF' },
  { from: 'CS403', to: 'CS404', relation: 'PREREQUISITE_OF' },
  { from: 'CS201', to: 'CS405', relation: 'PREREQUISITE_OF' },
]

// 节点颜色配置
const NODE_COLORS = {
  course_required: { bg: '#0ea5e9', border: '#0284c7' },
  course_elective: { bg: '#10b981', border: '#059669' },
  knowledge_point: { bg: '#a855f7', border: '#9333ea' },
  skill: { bg: '#f59e0b', border: '#d97706' },
  selected: { bg: '#f97316', border: '#ea580c' },
  dimmed: { bg: '#374151', border: '#4b5563' },
}

const RELATION_LABEL = {
  PREREQUISITE_OF: '先修',
  CONTAINS: '包含',
  BUILDS: '构建',
}

export default {
  name: 'KnowledgeGraph',
  components: {
    Search, ZoomIn, ZoomOut, RefreshRight, FullScreen,
    Share, Notebook, Document, Trophy, CircleCheckFilled, CirclePlusFilled
  },
  data() {
    return {
      network: null,
      nodesDataSet: null,
      edgesDataSet: null,

      // 所有原始数据（API/MOCK）
      allNodes: [],
      allEdges: [],

      // 已展开的课程 code 集合
      expandedNodes: new Set(),
      // 记录每个课程展开后的子节点 id
      childrenMap: {},

      selectedNode: null,
      searchText: '',
      filter: 'all',
      loading: false,
      isFullscreen: false,

      filters: [
        { value: 'all', label: '全部' },
        { value: '必修', label: '必修' },
        { value: '选修', label: '选修' },
      ]
    }
  },
  mounted() {
    this.$nextTick(() => this.loadAndInit())
  },
  beforeUnmount() {
    this.destroyNetwork()
    document.removeEventListener('fullscreenchange', this.onFullscreenChange)
  },
  methods: {
    // ========== 数据加载 ==========
    async loadAndInit() {
      this.loading = true
      try {
        const token = localStorage.getItem('token')
        const res = await fetch(`${BASE_URL}/api/knowledge_graph/all_courses`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        if (!res.ok) throw new Error('API failed')
        const data = await res.json()
        this.allNodes = data.nodes || []
        this.allEdges = data.edges || []
      } catch (e) {
        console.warn('知识图谱 API 失败，降级到 MOCK 数据', e)
        this.allNodes = MOCK_NODES.map(n => ({ ...n }))
        this.allEdges = MOCK_EDGES.map(e => ({ ...e }))
      } finally {
        this.loading = false
      }
      this.initGraph()
    },

    // ========== 图谱初始化 ==========
    getVisibleCourseNodes() {
      const courses = this.allNodes.filter(n => n.node_type === 'Course')
      if (this.filter === 'all') return courses
      return courses.filter(n => n.course_type === this.filter)
    },

    buildNodeItem(n) {
      if (n.node_type === 'Course') {
        const colors = n.course_type === '必修' ? NODE_COLORS.course_required : NODE_COLORS.course_elective
        const size = Math.max(20, (n.credit || 3) * 7)
        return {
          id: n.id,
          label: n.label,
          shape: 'dot',
          size,
          color: {
            background: colors.bg,
            border: colors.border,
            highlight: { background: NODE_COLORS.selected.bg, border: NODE_COLORS.selected.border },
            hover: { background: colors.bg, border: '#fff' }
          },
          font: { color: '#ffffff', size: 12, bold: true },
          shadow: { enabled: true, color: 'rgba(0,0,0,0.5)', size: 8, x: 2, y: 2 },
          title: `${n.label}  (${n.credit} 学分)`,
          _data: n
        }
      } else if (n.node_type === 'KnowledgePoint') {
        return {
          id: n.id,
          label: n.label,
          shape: 'dot',
          size: 14,
          color: {
            background: NODE_COLORS.knowledge_point.bg,
            border: NODE_COLORS.knowledge_point.border,
            highlight: { background: NODE_COLORS.selected.bg, border: NODE_COLORS.selected.border }
          },
          font: { color: '#ffffff', size: 11 },
          shadow: { enabled: true, color: 'rgba(0,0,0,0.4)', size: 6, x: 1, y: 1 },
          title: n.label,
          _data: n
        }
      } else {
        // Skill
        return {
          id: n.id,
          label: n.label,
          shape: 'dot',
          size: 12,
          color: {
            background: NODE_COLORS.skill.bg,
            border: NODE_COLORS.skill.border,
            highlight: { background: NODE_COLORS.selected.bg, border: NODE_COLORS.selected.border }
          },
          font: { color: '#ffffff', size: 11 },
          shadow: { enabled: true, color: 'rgba(0,0,0,0.4)', size: 6, x: 1, y: 1 },
          title: n.label,
          _data: n
        }
      }
    },

    buildEdgeItem(e, idx) {
      return {
        id: e.id !== undefined ? e.id : `e_${idx}`,
        from: e.from,
        to: e.to,
        label: RELATION_LABEL[e.relation] || '',
        arrows: { to: { enabled: true, scaleFactor: 0.8 } },
        color: { color: '#94a3b8', highlight: '#f59e0b', hover: '#cbd5e1' },
        font: { color: '#64748b', size: 10, strokeWidth: 0, align: 'middle' },
        smooth: { type: 'curvedCW', roundness: 0.15 },
        width: 1.2
      }
    },

    initGraph() {
      const container = this.$refs.graphContainer
      if (!container) return

      this.destroyNetwork()
      this.expandedNodes = new Set()
      this.childrenMap = {}

      const visibleCourses = this.getVisibleCourseNodes()
      const visibleIds = new Set(visibleCourses.map(n => n.id))

      const nodes = visibleCourses.map(n => this.buildNodeItem(n))
      const edges = this.allEdges
        .filter(e => visibleIds.has(e.from) && visibleIds.has(e.to))
        .map((e, i) => this.buildEdgeItem(e, i))

      this.nodesDataSet = new DataSet(nodes)
      this.edgesDataSet = new DataSet(edges)

      const options = {
        physics: {
          enabled: true,
          barnesHut: {
            gravitationalConstant: -4000,
            centralGravity: 0.3,
            springLength: 160,
            springConstant: 0.04,
            damping: 0.09,
            avoidOverlap: 0.1
          },
          stabilization: { iterations: 150, fit: true }
        },
        interaction: {
          hover: true,
          tooltipDelay: 200,
          hideEdgesOnDrag: false,
          multiselect: false
        },
        nodes: { borderWidth: 2 },
        edges: { width: 1.2 },
        layout: { randomSeed: 42 }
      }

      this.network = new Network(
        container,
        { nodes: this.nodesDataSet, edges: this.edgesDataSet },
        options
      )

      this.network.on('stabilizationIterationsDone', () => {
        this.network.setOptions({ physics: { enabled: false } })
      })

      this.network.on('click', params => {
        if (params.nodes.length) {
          this.onNodeClick(params.nodes[0])
        } else {
          this.onBlankClick()
        }
      })
    },

    destroyNetwork() {
      if (this.network) {
        this.network.destroy()
        this.network = null
      }
    },

    // ========== 节点点击 ==========
    async onNodeClick(nodeId) {
      const nodeItem = this.nodesDataSet.get(nodeId)
      if (!nodeItem) return
      const nodeData = nodeItem._data

      this.selectedNode = nodeData

      if (nodeData.node_type === 'Course') {
        if (this.expandedNodes.has(nodeId)) {
          // 已展开 -> 收起
          this.collapseNode(nodeId)
        } else {
          // 未展开 -> 展开
          await this.expandNode(nodeId)
        }
      }

      this.applyHighlight(nodeId)
    },

    onBlankClick() {
      this.selectedNode = null
      this.clearHighlight()
    },

    async expandNode(courseCode) {
      try {
        const token = localStorage.getItem('token')
        const res = await fetch(`${BASE_URL}/api/knowledge_graph/expand/${courseCode}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        if (!res.ok) throw new Error('expand API failed')
        const data = await res.json()

        const newNodeItems = (data.nodes || []).map(n => this.buildNodeItem(n))
        const newEdgeItems = (data.edges || []).map((e, i) => this.buildEdgeItem(e, `expand_${courseCode}_${i}`))

        const childIds = newNodeItems.map(n => n.id)
        this.childrenMap[courseCode] = childIds

        this.nodesDataSet.add(newNodeItems)
        this.edgesDataSet.add(newEdgeItems)
        this.expandedNodes.add(courseCode)

        // 临时开启 physics 让节点重新分布
        this.network.setOptions({ physics: { enabled: true } })
        setTimeout(() => {
          if (this.network) {
            this.network.setOptions({ physics: { enabled: false } })
          }
        }, 1500)
      } catch (e) {
        console.warn('展开节点失败', e)
        this.$message && this.$message.warning('暂无该课程的知识点数据')
      }
    },

    collapseNode(courseCode) {
      const children = this.childrenMap[courseCode] || []
      // 移除子节点
      children.forEach(id => {
        try { this.nodesDataSet.remove(id) } catch (_) {}
      })
      // 移除相关边
      const edgesToRemove = this.edgesDataSet.getIds().filter(eid => {
        const e = this.edgesDataSet.get(eid)
        return e && (children.includes(e.from) || children.includes(e.to))
      })
      edgesToRemove.forEach(eid => {
        try { this.edgesDataSet.remove(eid) } catch (_) {}
      })
      this.expandedNodes.delete(courseCode)
      delete this.childrenMap[courseCode]
    },

    // ========== 高亮逻辑 ==========
    applyHighlight(selectedId) {
      if (!this.nodesDataSet || !this.network) return

      const connectedNodeIds = new Set(this.network.getConnectedNodes(selectedId))
      const connectedEdgeIds = new Set(this.network.getConnectedEdges(selectedId))

      const allNodeIds = this.nodesDataSet.getIds()
      const allEdgeIds = this.edgesDataSet.getIds()

      const nodeUpdates = allNodeIds.map(id => {
        const item = this.nodesDataSet.get(id)
        const nd = item._data
        if (id === selectedId) {
          return {
            id,
            color: { background: NODE_COLORS.selected.bg, border: NODE_COLORS.selected.border },
            size: (item.size || 20) * 1.3,
            font: { color: '#ffffff', size: 13, bold: true }
          }
        } else if (connectedNodeIds.has(id)) {
          const base = this.getBaseColor(nd)
          return {
            id,
            color: { background: base.bg, border: '#ffffff' },
            borderWidth: 3,
            font: { color: '#ffffff' }
          }
        } else {
          return {
            id,
            color: { background: NODE_COLORS.dimmed.bg, border: NODE_COLORS.dimmed.border },
            opacity: 0.4,
            font: { color: '#9ca3af' }
          }
        }
      })
      this.nodesDataSet.update(nodeUpdates)

      const edgeUpdates = allEdgeIds.map(eid => {
        if (connectedEdgeIds.has(eid)) {
          return { id: eid, color: { color: '#f59e0b', highlight: '#f59e0b' }, width: 2 }
        } else {
          return { id: eid, color: { color: '#1e2a3a' }, width: 0.5 }
        }
      })
      this.edgesDataSet.update(edgeUpdates)
    },

    clearHighlight() {
      if (!this.nodesDataSet) return
      const allNodeIds = this.nodesDataSet.getIds()
      const nodeUpdates = allNodeIds.map(id => {
        const item = this.nodesDataSet.get(id)
        const nd = item._data
        const base = this.getBaseColor(nd)
        const size = nd.node_type === 'Course' ? Math.max(20, (nd.credit || 3) * 7) :
          nd.node_type === 'KnowledgePoint' ? 14 : 12
        return {
          id,
          color: { background: base.bg, border: base.border },
          size,
          opacity: 1,
          borderWidth: 2,
          font: { color: '#ffffff', size: nd.node_type === 'Course' ? 12 : 11, bold: nd.node_type === 'Course' }
        }
      })
      this.nodesDataSet.update(nodeUpdates)

      const allEdgeIds = this.edgesDataSet.getIds()
      const edgeUpdates = allEdgeIds.map(eid => ({
        id: eid,
        color: { color: '#94a3b8', highlight: '#f59e0b' },
        width: 1.2
      }))
      this.edgesDataSet.update(edgeUpdates)
    },

    getBaseColor(nd) {
      if (nd.node_type === 'Course') {
        return nd.course_type === '必修' ? NODE_COLORS.course_required : NODE_COLORS.course_elective
      } else if (nd.node_type === 'KnowledgePoint') {
        return NODE_COLORS.knowledge_point
      } else {
        return NODE_COLORS.skill
      }
    },

    // ========== 搜索 ==========
    onSearch() {
      if (!this.nodesDataSet) return
      const q = this.searchText.trim().toLowerCase()
      if (!q) {
        this.clearHighlight()
        return
      }
      const allNodeIds = this.nodesDataSet.getIds()
      const nodeUpdates = allNodeIds.map(id => {
        const item = this.nodesDataSet.get(id)
        const nd = item._data
        const match = nd.label && nd.label.toLowerCase().includes(q)
        if (match) {
          return {
            id,
            color: { background: '#f59e0b', border: '#d97706' },
            opacity: 1,
            font: { color: '#ffffff' }
          }
        } else {
          return {
            id,
            color: { background: NODE_COLORS.dimmed.bg, border: NODE_COLORS.dimmed.border },
            opacity: 0.3,
            font: { color: '#6b7280' }
          }
        }
      })
      this.nodesDataSet.update(nodeUpdates)
    },

    // ========== 筛选 ==========
    setFilter(val) {
      this.filter = val
      this.selectedNode = null
      this.searchText = ''
      this.initGraph()
    },

    // ========== 工具栏操作 ==========
    zoomIn() {
      if (!this.network) return
      const scale = this.network.getScale()
      this.network.moveTo({ scale: scale * 1.2 })
    },
    zoomOut() {
      if (!this.network) return
      const scale = this.network.getScale()
      this.network.moveTo({ scale: scale * 0.8 })
    },
    resetView() {
      if (!this.network) return
      this.network.fit({ animation: { duration: 500, easingFunction: 'easeInOutQuad' } })
    },
    toggleFullscreen() {
      const el = this.$refs.graphWrap
      if (!el) return
      if (!document.fullscreenElement) {
        el.requestFullscreen()
        document.addEventListener('fullscreenchange', this.onFullscreenChange)
      } else {
        document.exitFullscreen()
      }
    },
    onFullscreenChange() {
      this.isFullscreen = !!document.fullscreenElement
      if (this.network) {
        setTimeout(() => this.network.fit(), 300)
      }
    },

    // ========== 辅助 ==========
    getPrerequisiteNames(prerequisite) {
      if (!prerequisite) return '无'
      return prerequisite.split(',').map(code => {
        const c = this.allNodes.find(n => n.id === code.trim())
        return c ? c.label : code.trim()
      }).join('、')
    },

    difficultyStyle(level) {
      const map = {
        '简单': { background: 'rgba(16,185,129,0.2)', color: '#34d399' },
        '中等': { background: 'rgba(245,158,11,0.2)', color: '#fbbf24' },
        '困难': { background: 'rgba(239,68,68,0.2)', color: '#f87171' },
      }
      return map[level] || { background: 'rgba(100,116,139,0.2)', color: '#94a3b8' }
    }
  }
}
</script>

<style scoped>
/* ===== 整体容器 ===== */
.kg-wrapper {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 64px);
  background: #f1f5f9;
  padding: 16px;
  box-sizing: border-box;
  gap: 12px;
}

/* ===== 工具栏 ===== */
.kg-toolbar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  background: #161b22;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
  flex-shrink: 0;
}

.toolbar-search {
  flex-shrink: 0;
}

.toolbar-search :deep(.el-input__wrapper) {
  background: #0d1117;
  border: 1px solid #30363d;
  box-shadow: none;
}
.toolbar-search :deep(.el-input__wrapper):hover {
  border-color: #0ea5e9;
}
.toolbar-search :deep(.el-input__wrapper.is-focus) {
  border-color: #0ea5e9;
  box-shadow: 0 0 0 2px rgba(14, 165, 233, 0.2);
}
.toolbar-search :deep(.el-input__inner) {
  color: #e2e8f0;
  font-size: 13px;
}
.toolbar-search :deep(.el-input__inner::placeholder) {
  color: #4b5563;
}
.toolbar-search :deep(.el-icon) {
  color: #64748b;
}
.toolbar-search :deep(.el-input__clear) {
  color: #64748b;
}

.toolbar-filters {
  display: flex;
  gap: 6px;
}

.filter-btn {
  padding: 5px 14px;
  border-radius: 6px;
  border: 1px solid #30363d;
  background: transparent;
  color: #94a3b8;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}
.filter-btn:hover {
  border-color: #0ea5e9;
  color: #e2e8f0;
}
.filter-btn.active {
  background: #0ea5e9;
  border-color: #0ea5e9;
  color: #ffffff;
  font-weight: 600;
}

.toolbar-actions {
  display: flex;
  gap: 4px;
  margin-left: auto;
}

.action-btn {
  width: 34px;
  height: 34px;
  border-radius: 6px;
  border: 1px solid #30363d;
  background: transparent;
  color: #94a3b8;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 16px;
}
.action-btn:hover {
  border-color: #0ea5e9;
  color: #0ea5e9;
  background: rgba(14, 165, 233, 0.08);
}

/* ===== 主体 ===== */
.kg-body {
  display: flex;
  flex: 1;
  gap: 12px;
  min-height: 0;
}

/* ===== 图谱区域 ===== */
.kg-graph-wrap {
  flex: 1;
  position: relative;
  border-radius: 10px;
  overflow: hidden;
  background: #0d1117;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.4);
}

.kg-graph {
  width: 100%;
  height: 100%;
  background: #0d1117;
  background-image: radial-gradient(circle, #1c2433 1px, transparent 1px);
  background-size: 32px 32px;
}

/* loading */
.kg-loading {
  position: absolute;
  inset: 0;
  background: rgba(13, 17, 23, 0.85);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  color: #94a3b8;
  font-size: 14px;
  z-index: 10;
}

.loading-spinner {
  width: 36px;
  height: 36px;
  border: 3px solid #1e293b;
  border-top-color: #0ea5e9;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 图例 */
.kg-legend {
  position: absolute;
  bottom: 16px;
  left: 16px;
  display: flex;
  gap: 14px;
  background: rgba(22, 27, 34, 0.9);
  border: 1px solid #30363d;
  border-radius: 8px;
  padding: 8px 14px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #94a3b8;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

/* ===== 详情面板 ===== */
.kg-detail {
  width: 300px;
  flex-shrink: 0;
  background: #161b22;
  border-radius: 10px;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 空状态 */
.detail-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  color: #4b5563;
  padding: 24px;
  text-align: center;
}

.empty-icon {
  font-size: 40px;
  color: #30363d;
}

.detail-empty p {
  margin: 0;
  font-size: 14px;
  color: #6b7280;
}

.empty-sub {
  font-size: 12px !important;
  color: #374151 !important;
}

/* 类型颜色条 */
.detail-type-bar {
  height: 4px;
  flex-shrink: 0;
}

/* 内容区 */
.detail-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  scrollbar-width: thin;
  scrollbar-color: #30363d transparent;
}

.detail-content::-webkit-scrollbar {
  width: 4px;
}
.detail-content::-webkit-scrollbar-track {
  background: transparent;
}
.detail-content::-webkit-scrollbar-thumb {
  background: #30363d;
  border-radius: 4px;
}

.detail-header {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 12px;
}

.detail-type-icon {
  font-size: 22px;
  color: #0ea5e9;
  flex-shrink: 0;
  margin-top: 2px;
}

.detail-title {
  font-size: 16px;
  font-weight: 700;
  color: #e2e8f0;
  line-height: 1.4;
}

.detail-code {
  font-size: 12px;
  color: #64748b;
  margin-top: 2px;
}

.detail-divider {
  height: 1px;
  background: #21262d;
  margin: 12px 0;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 10px;
  padding: 6px 0;
  font-size: 13px;
}

.detail-key {
  color: #64748b;
  flex-shrink: 0;
  font-size: 12px;
  padding-top: 1px;
}

.detail-val {
  color: #cbd5e1;
  text-align: right;
  line-height: 1.5;
}

.detail-val.prereq {
  color: #0ea5e9;
}

.detail-val.muted {
  color: #374151;
}

.detail-desc {
  padding: 4px 0;
  font-size: 13px;
}

.detail-desc .detail-key {
  margin-bottom: 6px;
  display: block;
}

.detail-desc-text {
  color: #94a3b8;
  line-height: 1.7;
  font-size: 13px;
}

.detail-expand-state {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #64748b;
  background: #0d1117;
  border-radius: 6px;
  padding: 8px 10px;
  border: 1px solid #21262d;
}

.difficulty-tag {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

/* ===== 全屏状态 ===== */
.kg-graph-wrap:fullscreen {
  border-radius: 0;
}
.kg-graph-wrap:fullscreen .kg-graph {
  height: 100vh;
}
</style>
