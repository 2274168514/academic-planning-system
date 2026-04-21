<template>
  <div class="dashboard">
    <!-- 欢迎区 -->
    <div class="welcome-bar">
      <div>
        <div class="welcome-title">{{ greeting }}，{{ username }}</div>
        <div class="welcome-date">{{ currentDate }}</div>
      </div>
      <el-button type="primary" size="small" plain @click="$router.push('/academic-planning')">
        查看学习计划
      </el-button>
    </div>

    <!-- 统计卡片 -->
    <div class="stat-grid">
      <div class="stat-card" v-for="card in statCards" :key="card.title">
        <div class="stat-top" :style="{ background: card.color }"></div>
        <div class="stat-body">
          <div class="stat-header">
            <span class="stat-label">{{ card.title }}</span>
            <el-icon class="stat-icon" :style="{ color: card.color }">
              <component :is="card.icon" />
            </el-icon>
          </div>
          <div class="stat-value">
            {{ card.value }}<span class="stat-unit">{{ card.unit }}</span>
          </div>
          <div class="stat-trend" :class="card.trendType">
            {{ card.trend }}
          </div>
        </div>
      </div>
    </div>

    <!-- 图表区 -->
    <div class="chart-grid">
      <div class="chart-card">
        <div class="card-head">
          <span class="card-head-title">课程学习进度</span>
          <el-tag size="small" type="info">本学期</el-tag>
        </div>
        <div ref="progressChart" class="chart-box"></div>
      </div>

      <div class="chart-card">
        <div class="card-head">
          <span class="card-head-title">学分分布</span>
          <el-tag size="small" type="info">全部</el-tag>
        </div>
        <div ref="distChart" class="chart-box"></div>
      </div>
    </div>

    <!-- 最近活动 -->
    <div class="activity-card">
      <div class="card-head">
        <span class="card-head-title">最近学习动态</span>
      </div>
      <el-timeline>
        <el-timeline-item
          v-for="item in activities"
          :key="item.time"
          :timestamp="item.time"
          :color="item.color"
          placement="top"
        >
          <div class="timeline-content">
            <div class="timeline-title">{{ item.title }}</div>
            <div class="timeline-desc">{{ item.desc }}</div>
          </div>
        </el-timeline-item>
      </el-timeline>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import {
  Reading, TrendCharts, Trophy, AlarmClock
} from '@element-plus/icons-vue'

export default {
  name: 'Dashboard',
  components: { Reading, TrendCharts, Trophy, AlarmClock },
  data() {
    const hour = new Date().getHours()
    const greeting = hour < 12 ? '早上好' : hour < 18 ? '下午好' : '晚上好'
    const now = new Date()
    const currentDate = `${now.getFullYear()} 年 ${now.getMonth() + 1} 月 ${now.getDate()} 日，${['周日','周一','周二','周三','周四','周五','周六'][now.getDay()]}`

    return {
      greeting,
      currentDate,
      username: '同学',
      chartInstances: [],
      statCards: [
        { title: '我的课程', value: 6, unit: '门', trend: '较上学期 +1', trendType: 'up', color: '#0ea5e9', icon: 'Reading' },
        { title: '学习进度', value: 78, unit: '%', trend: '较上周 +3%', trendType: 'up', color: '#10b981', icon: 'TrendCharts' },
        { title: '掌握技能', value: 24, unit: '项', trend: '本月新增 4 项', trendType: 'up', color: '#f59e0b', icon: 'Trophy' },
        { title: '学习时长', value: 127, unit: 'h', trend: '本学期累计', trendType: 'neutral', color: '#ef4444', icon: 'AlarmClock' }
      ],
      activities: [
        { time: '今天 14:30', title: '完成《数据结构》第5章学习', desc: '已掌握二叉树相关知识点', color: '#10b981' },
        { time: '昨天 10:15', title: '参与《软件工程》在线讨论', desc: '发表3条讨论内容，获得5个点赞', color: '#0ea5e9' },
        { time: '2天前 16:00', title: '提交《计算机网络》实验报告', desc: 'HTTP协议分析实验，得分94分', color: '#f59e0b' },
        { time: '3天前 09:00', title: '完成算法设计第3章习题', desc: '动态规划相关题目，正确率 88%', color: '#8b5cf6' }
      ]
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initProgressChart()
      this.initDistChart()
      window.addEventListener('resize', this.handleResize)
    })
  },
  beforeUnmount() {
    this.chartInstances.forEach(c => c.dispose())
    window.removeEventListener('resize', this.handleResize)
  },
  methods: {
    handleResize() {
      this.chartInstances.forEach(c => c.resize())
    },

    initProgressChart() {
      const el = this.$refs.progressChart
      if (!el) return
      const chart = echarts.init(el)
      this.chartInstances.push(chart)
      chart.setOption({
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' }, formatter: '{b}: {c}%' },
        grid: { left: 16, right: 48, top: 12, bottom: 12, containLabel: true },
        xAxis: {
          type: 'value', max: 100,
          axisLabel: { formatter: '{value}%', color: '#94a3b8', fontSize: 11 },
          splitLine: { lineStyle: { color: '#f1f5f9' } }
        },
        yAxis: {
          type: 'category',
          data: ['软件工程', '计算机网络', '操作系统', '数据结构', '数据库系统'],
          axisLabel: { color: '#64748b', fontSize: 12 },
          axisLine: { show: false },
          axisTick: { show: false }
        },
        series: [{
          type: 'bar',
          data: [
            { value: 90, itemStyle: { color: '#10b981' } },
            { value: 62, itemStyle: { color: '#0ea5e9' } },
            { value: 45, itemStyle: { color: '#f59e0b' } },
            { value: 85, itemStyle: { color: '#10b981' } },
            { value: 75, itemStyle: { color: '#0ea5e9' } }
          ],
          barMaxWidth: 18,
          itemStyle: { borderRadius: [0, 6, 6, 0] },
          label: { show: true, position: 'right', color: '#64748b', fontSize: 11, formatter: '{c}%' }
        }]
      })
    },

    initDistChart() {
      const el = this.$refs.distChart
      if (!el) return
      const chart = echarts.init(el)
      this.chartInstances.push(chart)
      chart.setOption({
        tooltip: { trigger: 'item', formatter: '{b}: {c} 学分 ({d}%)' },
        legend: {
          orient: 'vertical', right: '8%', top: 'center',
          textStyle: { color: '#64748b', fontSize: 12 },
          itemWidth: 10, itemHeight: 10
        },
        series: [{
          type: 'pie',
          radius: ['42%', '68%'],
          center: ['38%', '50%'],
          data: [
            { value: 60, name: '专业必修', itemStyle: { color: '#0ea5e9' } },
            { value: 24, name: '专业选修', itemStyle: { color: '#10b981' } },
            { value: 36, name: '通识教育', itemStyle: { color: '#f59e0b' } },
            { value: 40, name: '实践环节', itemStyle: { color: '#6366f1' } }
          ],
          itemStyle: { borderRadius: 4, borderColor: '#fff', borderWidth: 2 },
          label: { show: false },
          emphasis: { scale: true, scaleSize: 6 }
        }]
      })
    }
  }
}
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 欢迎区 */
.welcome-bar {
  background: #ffffff;
  border-radius: 10px;
  padding: 18px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

.welcome-title {
  font-size: 18px;
  font-weight: 600;
  color: #0f172a;
  margin-bottom: 4px;
}

.welcome-date {
  font-size: 13px;
  color: #94a3b8;
}

/* 统计卡片 */
.stat-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.stat-card {
  background: #ffffff;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

.stat-top {
  height: 4px;
}

.stat-body {
  padding: 16px 20px 18px;
}

.stat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.stat-label {
  font-size: 13px;
  color: #64748b;
  font-weight: 500;
}

.stat-icon {
  font-size: 18px;
  opacity: 0.8;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #0f172a;
  line-height: 1;
  margin-bottom: 8px;
}

.stat-unit {
  font-size: 14px;
  font-weight: 400;
  color: #94a3b8;
  margin-left: 3px;
}

.stat-trend {
  font-size: 12px;
}

.stat-trend.up { color: #10b981; }
.stat-trend.down { color: #ef4444; }
.stat-trend.neutral { color: #94a3b8; }

/* 图表区 */
.chart-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.chart-card, .activity-card {
  background: #ffffff;
  border-radius: 10px;
  padding: 18px 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

.card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.card-head-title {
  font-size: 15px;
  font-weight: 600;
  color: #0f172a;
}

.chart-box {
  height: 220px;
}

/* 时间线 */
.timeline-title {
  font-size: 14px;
  font-weight: 500;
  color: #1e293b;
  margin-bottom: 4px;
}

.timeline-desc {
  font-size: 13px;
  color: #94a3b8;
}

/* 响应式 */
@media (max-width: 1200px) {
  .stat-grid { grid-template-columns: repeat(2, 1fr); }
  .chart-grid { grid-template-columns: 1fr; }
}

@media (max-width: 768px) {
  .stat-grid { grid-template-columns: 1fr; }
  .welcome-bar { flex-direction: column; align-items: flex-start; gap: 12px; }
}
</style>
