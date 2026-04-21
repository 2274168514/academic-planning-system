<template>
  <div class="dashboard-container">
    <h1 class="page-title">学习仪表盘</h1>
    
    <div class="data-overview">
      <div class="data-card">
        <div class="card-icon" style="background-color: #1890ff;">
          <i class="el-icon-reading"></i>
        </div>
        <div class="card-content">
          <div class="card-title">我的课程</div>
          <div class="card-value">6<span class="card-unit">门</span></div>
          <div class="card-desc">当前学期课程</div>
        </div>
      </div>
      
      <div class="data-card">
        <div class="card-icon" style="background-color: #52c41a;">
          <i class="el-icon-document-checked"></i>
        </div>
        <div class="card-content">
          <div class="card-title">学习进度</div>
          <div class="card-value">78<span class="card-unit">%</span></div>
          <div class="card-desc">整体完成度</div>
        </div>
      </div>
      
      <div class="data-card">
        <div class="card-icon" style="background-color: #faad14;">
          <i class="el-icon-trophy"></i>
        </div>
        <div class="card-content">
          <div class="card-title">掌握技能</div>
          <div class="card-value">24<span class="card-unit">项</span></div>
          <div class="card-desc">关键技能点</div>
        </div>
      </div>
      
      <div class="data-card">
        <div class="card-icon" style="background-color: #f5222d;">
          <i class="el-icon-alarm-clock"></i>
        </div>
        <div class="card-content">
          <div class="card-title">学习时长</div>
          <div class="card-value">127<span class="card-unit">小时</span></div>
          <div class="card-desc">本学期总计</div>
        </div>
      </div>
    </div>
    
    <div class="chart-section">
      <div class="chart-container">
        <div class="chart-header">
          <h3>课程学习进度</h3>
        </div>
        <div class="chart-placeholder" ref="progressChart">
          <!-- 这里将通过echarts生成图表 -->
          图表加载中...
        </div>
      </div>
      
      <div class="chart-container">
        <div class="chart-header">
          <h3>知识点分布</h3>
        </div>
        <div class="chart-placeholder" ref="knowledgeChart">
          <!-- 这里将通过echarts生成图表 -->
          图表加载中...
        </div>
      </div>
    </div>
    
    <div class="recent-section">
      <h2 class="section-title">最近学习活动</h2>
      <div class="activity-list">
        <div class="activity-item">
          <div class="activity-time">今天 14:30</div>
          <div class="activity-content">
            <div class="activity-title">完成《数据结构》第5章课程学习</div>
            <div class="activity-desc">已掌握二叉树相关知识点</div>
          </div>
        </div>
        
        <div class="activity-item">
          <div class="activity-time">昨天 10:15</div>
          <div class="activity-content">
            <div class="activity-title">参与《软件工程》在线讨论</div>
            <div class="activity-desc">发表3条讨论内容，获得5个点赞</div>
          </div>
        </div>
        
        <div class="activity-item">
          <div class="activity-time">2天前</div>
          <div class="activity-content">
            <div class="activity-title">提交《计算机网络》实验报告</div>
            <div class="activity-desc">HTTP协议分析实验，得分94分</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Dashboard",
  data() {
    return {
      // 可以添加仪表盘数据
    }
  },
  mounted() {
    // 这里可以初始化图表
    this.initCharts();
  },
  methods: {
    initCharts() {
      // 初始化echarts的方法
      console.log('初始化图表');
      // 此处应该有echarts的初始化代码
      // 如果项目中已经集成了echarts，可以实现具体的图表
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.page-title {
  margin-bottom: 24px;
  font-size: 24px;
  color: #333;
}

.data-overview {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.data-card {
  background: white;
  border-radius: 4px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  display: flex;
}

.card-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  color: white;
  font-size: 24px;
}

.card-content {
  flex: 1;
}

.card-title {
  color: #666;
  font-size: 14px;
}

.card-value {
  font-size: 24px;
  font-weight: bold;
  margin: 8px 0;
  color: #333;
}

.card-unit {
  font-size: 14px;
  margin-left: 4px;
  font-weight: normal;
}

.card-desc {
  color: #999;
  font-size: 13px;
}

.chart-section {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.chart-container {
  background: white;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  padding: 15px;
}

.chart-header {
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: 10px;
  margin-bottom: 15px;
}

.chart-header h3 {
  margin: 0;
  font-size: 16px;
}

.chart-placeholder {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
}

.section-title {
  font-size: 18px;
  margin-bottom: 15px;
}

.activity-list {
  background: white;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.activity-item {
  display: flex;
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-time {
  width: 120px;
  color: #666;
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-weight: 500;
  margin-bottom: 5px;
}

.activity-desc {
  color: #666;
  font-size: 14px;
}

/* 响应式布局 */
@media (max-width: 1200px) {
  .data-overview {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .chart-section {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .data-overview {
    grid-template-columns: 1fr;
  }
  
  .activity-item {
    flex-direction: column;
  }
  
  .activity-time {
    margin-bottom: 8px;
  }
}
</style>
