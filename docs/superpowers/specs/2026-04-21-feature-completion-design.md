# 功能完善设计文档

**日期：** 2026-04-21  
**项目：** 大学生学业规划系统  
**范围：** 三个核心页面的功能完善

---

## 背景

项目登录注册已通，但以下三个页面功能不完整：
- `LearningProgress.vue` — ECharts 图表是占位符，未初始化
- `AcademicPlanning.vue` — 所有 CRUD 操作只弹提示消息，未接 API
- `KnowledgeGraph.vue` — 页面完全空白

数据策略：学业规划接真实后端 API，其余两个页面使用 mock 数据（后期有真实数据时替换）。

---

## 模块一：学习进度图表（LearningProgress）

### 变更范围
仅修改 `frontend/src/views/LearningProgress.vue`，不新增文件。

### ECharts 时间图表（柱状图）
- 替换 `.time-chart` 内的占位符 div
- 展示过去 7 天每天学习时长（小时）
- 样式：蓝色渐变柱体，X 轴为星期，Y 轴为小时数
- Mock 数据示例：`[2.5, 3.0, 1.5, 4.0, 2.0, 3.5, 2.5]`（周一到周日）

### ECharts 技能雷达图
- 替换 `.skill-radar` 内的占位符 div
- 6 个维度：编程能力、算法基础、系统知识、网络协议、数据库、软件工程
- 两组数据：当前水平（实线蓝色填充）、目标水平（虚线浅蓝填充）
- Mock 数据：当前 `[80, 65, 70, 55, 75, 60]`，目标 `[90, 85, 80, 80, 90, 80]`

### 实现要点
- 在 `mounted()` 中初始化两个 echarts 实例
- 监听 `selectedTimeRange` 变化时重绘时间图表
- 组件销毁时调用 `echarts.dispose()` 防止内存泄漏
- 图表容器设置明确高度（`height: 220px`，已有 CSS）

---

## 模块二：学业规划管理（AcademicPlanning）

### 变更范围
仅修改 `frontend/src/views/AcademicPlanning.vue`，使用 `src/utils/api.js` 中已有的 `planningApi`。

### 布局调整
将现有 tab 结构中的「学期规划」tab 改为真实数据驱动：
- 页面顶部：计划列表（el-select 下拉切换当前计划）+ 新建计划按钮
- 主体：当前计划的课程列表（el-table）
- 保留学位要求、毕业审计两个 tab，数据不动

### API 调用
| 操作 | 接口 | 时机 |
|------|------|------|
| 加载计划列表 | GET `/api/study_plans` | 页面 mounted |
| 新建计划 | POST `/api/study_plans` | 弹窗确认 |
| 删除计划 | DELETE `/api/study_plans/:id` | 二次确认后 |
| 加载计划课程 | GET `/api/study_plans/:id` | 切换计划时 |
| 添加课程 | POST `/api/study_plans/:id/details` | 选课弹窗确认 |
| 移除课程 | DELETE `/api/study_plans/:id/details/:detail_id` | 二次确认后 |
| 加载课程列表（选课用） | GET `/api/courses` | 打开选课弹窗时 |

### 弹窗设计
**新建计划弹窗：**
- 字段：计划名称（必填）、描述（选填）
- 提交后刷新计划列表，自动切换到新计划

**添加课程弹窗：**
- 字段：课程（el-select 从课程列表选择）、学期（文本输入）、优先级（1-5 数字）
- 提交后刷新当前计划课程列表

### 状态管理
- `plans` — 计划列表
- `currentPlanId` — 当前选中计划 ID
- `planDetails` — 当前计划的课程列表
- `loading` — 请求中状态（展示 el-loading）

---

## 模块三：知识图谱（KnowledgeGraph）

### 变更范围
完全重写 `frontend/src/views/KnowledgeGraph.vue`，不新增文件。

### 数据
使用本地 mock 数据，包含 12 门课程及先修关系（与 `init_db.py` 一致）：

**节点（课程）：**
CS101 计算机导论、CS102 程序设计基础、CS201 数据结构、CS301 算法设计、CS302 操作系统、CS303 计算机网络、CS304 数据库系统、CS401 软件工程、CS402 人工智能、CS403 机器学习、CS404 深度学习、CS405 计算机图形学

**边（先修关系）：**
CS102→CS201、CS201→CS301、CS201→CS302、CS101→CS303、CS201→CS304、CS304→CS401、CS301→CS402、CS402→CS403、CS403→CS404、CS201→CS405

### 图谱样式
- 必修课节点：蓝色 (`#409EFF`)，圆形
- 选修课节点：绿色 (`#67C23A`)，圆形
- 节点大小：学分 × 8（如 4 学分 = 32px）
- 边：灰色有向箭头，标签显示"先修"
- 布局：`hierarchical`（从上到下层次布局）

### 页面布局
```
[ 顶部工具栏：搜索框 | 全部/必修/选修 筛选按钮 ]
[                                    |              ]
[     图谱区域（Vis.js canvas）        | 详情面板      ]
[     占 70% 宽度                     | 占 30% 宽度   ]
[                                    | （点击节点显示）]
```

### 详情面板内容
- 课程名称、课程编号
- 学分、课程类型（必修/选修）
- 所属院系
- 课程描述
- 先修课程列表

### 交互
- 点击节点 → 详情面板滑入显示
- 搜索输入 → 匹配节点变为高亮橙色，其余变暗
- 筛选按钮 → 重新渲染图谱，只显示对应类型节点及其关联边
- 鼠标悬停节点 → tooltip 显示课程名

---

## 不在本次范围内

- AI 助手功能（无 API key，跳过）
- 后端知识图谱 API（Neo4j 未配置）
- MySQL 迁移（保持 SQLite 开发环境）
- 前端整体 UI 优化（单独迭代）
