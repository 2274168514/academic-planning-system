<template>
  <div class="landing">
    <!-- Nav -->
    <nav class="lp-nav">
      <div class="lp-nav-inner">
        <div class="lp-logo">
          <span class="logo-mark">智</span>
          <span class="logo-name">学规划</span>
        </div>
        <div class="lp-nav-right">
          <button class="btn-ghost" @click="$router.push('/login')">登录</button>
          <button class="btn-gold" @click="$router.push('/register')">免费注册</button>
        </div>
      </div>
    </nav>

    <!-- Hero -->
    <section class="lp-hero">
      <div class="hero-bg">
        <img
          src="https://images.unsplash.com/photo-1481627834876-b7833e8f5570?auto=format&fit=crop&w=1920&q=80"
          alt=""
          class="hero-img"
        />
        <div class="hero-overlay"></div>
      </div>

      <div class="lp-container hero-content">
        <div class="hero-left">
          <div class="hero-badge">
            <span class="badge-pulse"></span>
            DeepSeek AI · 智能学业引擎
          </div>
          <h1 class="hero-title">
            <span class="title-main">智能规划</span>
            <span class="title-accent">你的学业未来</span>
          </h1>
          <p class="hero-desc">
            专为大学生打造的 AI 学业助手，融合知识图谱与大模型，
            提供个性化课程推荐、学习路径规划与全程学业陪伴
          </p>
          <div class="hero-cta">
            <button class="btn-primary" @click="$router.push('/login')">
              开始使用
              <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 10h12M10 4l6 6-6 6"/></svg>
            </button>
            <button class="btn-outline-white" @click="scrollTo('features')">了解更多</button>
          </div>
          <div class="hero-stats">
            <div class="stat-item">
              <span class="stat-num">{{ stats.courses }}+</span>
              <span class="stat-label">课程资源</span>
            </div>
            <div class="stat-sep"></div>
            <div class="stat-item">
              <span class="stat-num">{{ stats.users }}+</span>
              <span class="stat-label">在校学生</span>
            </div>
            <div class="stat-sep"></div>
            <div class="stat-item">
              <span class="stat-num">{{ stats.accuracy }}%</span>
              <span class="stat-label">规划准确率</span>
            </div>
          </div>
        </div>

        <div class="hero-right">
          <div class="chat-card">
            <div class="chat-card-header">
              <img src="https://cdn.deepseek.com/platform/favicon.png" class="chat-avatar" alt="AI" />
              <div class="chat-card-info">
                <span class="chat-name">DeepSeek 学习顾问</span>
                <span class="chat-online"><em></em>在线</span>
              </div>
            </div>
            <div class="chat-card-body">
              <div class="chat-bubble ai" :class="{ visible: bubble1 }">
                你好！我是你的 AI 学业规划助手，请问你目前就读什么专业？
              </div>
              <div class="chat-bubble user" :class="{ visible: bubble2 }">
                计算机科学大二，想往人工智能方向发展
              </div>
              <div class="chat-bubble ai" :class="{ visible: bubble3 }">
                为你规划学习路径：数据结构 → 机器学习 → 深度学习 → 项目实战<span class="cursor">|</span>
              </div>
            </div>
            <div class="chat-card-footer">
              <div class="chat-input-mock">输入你的问题...</div>
              <div class="chat-send">
                <svg viewBox="0 0 24 24" fill="currentColor"><path d="M2 21l21-9L2 3v7l15 2-15 2v7z"/></svg>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="scroll-hint" @click="scrollTo('features')">
        <div class="scroll-line"></div>
        <span>向下探索</span>
      </div>
    </section>

    <!-- Features -->
    <section class="lp-features" id="features" ref="featuresRef">
      <div class="lp-container">
        <div class="section-header">
          <p class="section-tag">核心功能</p>
          <h2 class="section-title">一站式学业规划平台</h2>
          <p class="section-sub">从入学到毕业，AI 全程陪伴你的大学四年</p>
        </div>
        <div class="features-grid">
          <div
            v-for="(f, i) in features"
            :key="i"
            class="feature-card"
            :class="{ visible: featuresVisible }"
            :style="{ animationDelay: `${i * 0.08}s` }"
          >
            <div class="feature-icon" v-html="f.icon"></div>
            <h3 class="feature-name">{{ f.title }}</h3>
            <p class="feature-desc">{{ f.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Showcase -->
    <section class="lp-showcase">
      <div class="lp-container">
        <div class="showcase-row" v-for="(s, i) in showcases" :key="i" :class="{ rev: i % 2 === 1 }">
          <div class="showcase-text">
            <p class="section-tag">{{ s.tag }}</p>
            <h2 class="showcase-title">{{ s.title }}</h2>
            <p class="showcase-desc">{{ s.desc }}</p>
            <ul class="showcase-list">
              <li v-for="p in s.points" :key="p"><span class="list-dot"></span>{{ p }}</li>
            </ul>
            <button class="btn-primary sm" @click="$router.push('/register')">立即体验</button>
          </div>
          <div class="showcase-img-wrap">
            <img :src="s.img" :alt="s.title" />
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="lp-cta">
      <div class="lp-container">
        <div class="cta-box">
          <h2 class="cta-title">准备好开启你的智能学习之旅了吗？</h2>
          <p class="cta-sub">免费注册，AI 助你规划更好的大学生涯</p>
          <button class="btn-primary lg" @click="$router.push('/register')">
            立即免费注册
            <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 10h12M10 4l6 6-6 6"/></svg>
          </button>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="lp-footer">
      <div class="lp-container footer-inner">
        <div class="lp-logo">
          <span class="logo-mark">智</span>
          <span class="logo-name" style="color:#1a1a2e">学规划</span>
        </div>
        <p class="footer-copy">© 2024 学业规划智能系统 · Powered by DeepSeek AI</p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'LandingPage',
  data() {
    return {
      featuresVisible: false,
      bubble1: false,
      bubble2: false,
      bubble3: false,
      stats: { courses: 0, users: 0, accuracy: 0 },
      features: [
        {
          title: 'AI 智能对话',
          desc: '基于 DeepSeek 大模型，24小时在线解答学业疑问，制定个性化学习计划',
          icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" stroke-linecap="round" stroke-linejoin="round"/></svg>`
        },
        {
          title: '知识图谱',
          desc: '可视化课程知识体系，清晰展示学科关联与先修关系，帮你找到最优学习路径',
          icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="2.5"/><circle cx="4" cy="6" r="2"/><circle cx="20" cy="6" r="2"/><circle cx="4" cy="18" r="2"/><circle cx="20" cy="18" r="2"/><line x1="11" y1="10" x2="5.5" y2="7.2"/><line x1="13" y1="10" x2="18.5" y2="7.2"/><line x1="11" y1="14" x2="5.5" y2="16.8"/><line x1="13" y1="14" x2="18.5" y2="16.8"/></svg>`
        },
        {
          title: '学习进度追踪',
          desc: '实时记录课程完成情况与成绩，可视化呈现学业进展，激励持续前进',
          icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" stroke-linecap="round" stroke-linejoin="round"/></svg>`
        },
        {
          title: '课程智能推荐',
          desc: '基于你的专业、兴趣和学习历史，AI 精准推荐最适合你的下一门课程',
          icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" stroke-linecap="round" stroke-linejoin="round"/></svg>`
        },
        {
          title: '学业规划',
          desc: '从大一到大四，AI 帮你制定完整的学业路线图，确保每学期课程安排科学合理',
          icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" stroke-linecap="round" stroke-linejoin="round"/></svg>`
        },
        {
          title: '职业路径规划',
          desc: '结合专业方向与职业目标，为你绘制清晰的成长路径，提前规划未来发展',
          icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" stroke-linecap="round" stroke-linejoin="round"/></svg>`
        }
      ],
      showcases: [
        {
          tag: 'AI 对话助手',
          title: '随时随地，问就有答',
          desc: '接入 DeepSeek 大语言模型，你的专属学业顾问24小时在线。无论是课程疑问、考研规划还是就业方向，一问便知。',
          points: ['智能理解上下文，对话更自然', '专注学业场景，回答更专业', '支持连续追问，深入探讨'],
          img: 'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=700&q=80'
        },
        {
          tag: '知识图谱',
          title: '知识脉络，一目了然',
          desc: '将课程体系以可视化知识图谱呈现，直观展示各课程之间的先修关系与知识联结，助你把握全局，规划最优学习顺序。',
          points: ['交互式节点图，支持点击探索', '清晰标注先修课程依赖关系', '覆盖全专业课程知识体系'],
          img: 'https://images.unsplash.com/photo-1513258496099-48168024aec0?auto=format&fit=crop&w=700&q=80'
        }
      ]
    }
  },
  mounted() {
    this.animateStats()
    this.animateBubbles()
    this.observeFeatures()
  },
  methods: {
    scrollTo(id) {
      document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })
    },
    animateStats() {
      const targets = { courses: 120, users: 2000, accuracy: 94 }
      const steps = 60
      let step = 0
      const timer = setInterval(() => {
        step++
        const ease = 1 - Math.pow(1 - step / steps, 3)
        this.stats.courses = Math.floor(targets.courses * ease)
        this.stats.users = Math.floor(targets.users * ease)
        this.stats.accuracy = Math.floor(targets.accuracy * ease)
        if (step >= steps) clearInterval(timer)
      }, 30)
    },
    animateBubbles() {
      setTimeout(() => { this.bubble1 = true }, 600)
      setTimeout(() => { this.bubble2 = true }, 1500)
      setTimeout(() => { this.bubble3 = true }, 2500)
    },
    observeFeatures() {
      const observer = new IntersectionObserver(
        (entries) => { if (entries[0].isIntersecting) this.featuresVisible = true },
        { threshold: 0.1 }
      )
      if (this.$refs.featuresRef) observer.observe(this.$refs.featuresRef)
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.landing {
  font-family: 'DM Sans', sans-serif;
  background: #f7f5f0;
  color: #1a1a2e;
  overflow-x: hidden;
}

.lp-container {
  max-width: 1160px;
  margin: 0 auto;
  padding: 0 32px;
}

/* NAV */
.lp-nav {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 100;
  padding: 18px 0;
  background: rgba(10, 12, 26, 0.55);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255,255,255,0.08);
}
.lp-nav-inner {
  max-width: 1160px;
  margin: 0 auto;
  padding: 0 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.lp-logo { display: flex; align-items: center; gap: 8px; cursor: pointer; text-decoration: none; }
.logo-mark {
  width: 34px; height: 34px;
  background: #c9a84c;
  color: #0a0c1a;
  font-family: 'Playfair Display', serif;
  font-weight: 900;
  font-size: 18px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 7px;
}
.logo-name {
  font-family: 'Playfair Display', serif;
  font-size: 17px;
  font-weight: 700;
  color: #ffffff;
}
.lp-nav-right { display: flex; align-items: center; gap: 10px; }

.btn-ghost {
  background: transparent;
  border: 1px solid rgba(255,255,255,0.3);
  color: #ffffff;
  padding: 8px 20px;
  border-radius: 6px;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s;
}
.btn-ghost:hover { border-color: #c9a84c; background: rgba(201,168,76,0.1); }

.btn-gold {
  background: #c9a84c;
  border: none;
  color: #0a0c1a;
  padding: 8px 20px;
  border-radius: 6px;
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s, transform 0.15s;
}
.btn-gold:hover { background: #e0bc66; transform: translateY(-1px); }

/* HERO */
.lp-hero {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  overflow: hidden;
}
.hero-bg { position: absolute; inset: 0; z-index: 0; }
.hero-img {
  width: 100%; height: 100%;
  object-fit: cover;
  filter: brightness(0.45) saturate(1.3);
}
.hero-overlay {
  position: absolute; inset: 0;
  background: linear-gradient(
    120deg,
    rgba(10, 12, 26, 0.88) 0%,
    rgba(10, 12, 26, 0.65) 50%,
    rgba(10, 12, 26, 0.82) 100%
  );
}

.hero-content {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 72px;
  align-items: center;
  padding-top: 96px;
  padding-bottom: 80px;
  width: 100%;
}
.hero-left { display: flex; flex-direction: column; gap: 26px; }

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  background: rgba(201,168,76,0.15);
  border: 1px solid rgba(201,168,76,0.35);
  color: #e8c97a;
  font-size: 13px;
  padding: 7px 16px;
  border-radius: 100px;
  width: fit-content;
  animation: fadeUp 0.6s ease both;
}
.badge-pulse {
  width: 7px; height: 7px;
  background: #c9a84c;
  border-radius: 50%;
  animation: pulse 1.8s infinite;
}
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.5;transform:scale(1.5)} }

.hero-title {
  font-family: 'Playfair Display', serif;
  display: flex; flex-direction: column; gap: 2px;
  animation: fadeUp 0.6s 0.1s ease both;
}
.title-main {
  font-size: clamp(48px, 5.5vw, 76px);
  font-weight: 900;
  color: #ffffff;
  line-height: 1.1;
  letter-spacing: -0.02em;
}
.title-accent {
  font-size: clamp(36px, 4.5vw, 60px);
  font-weight: 700;
  color: #c9a84c;
  line-height: 1.15;
}

.hero-desc {
  font-size: 16px;
  line-height: 1.8;
  color: rgba(255,255,255,0.78);
  max-width: 440px;
  animation: fadeUp 0.6s 0.2s ease both;
}

.hero-cta {
  display: flex; gap: 14px; align-items: center;
  animation: fadeUp 0.6s 0.3s ease both;
}

.btn-primary {
  display: inline-flex; align-items: center; gap: 8px;
  background: #c9a84c;
  color: #0a0c1a;
  border: none;
  padding: 13px 28px;
  border-radius: 8px;
  font-family: 'DM Sans', sans-serif;
  font-size: 15px; font-weight: 500;
  cursor: pointer;
  transition: background 0.2s, transform 0.15s, box-shadow 0.2s;
}
.btn-primary:hover {
  background: #e0bc66;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(201,168,76,0.35);
}
.btn-primary svg { width: 16px; height: 16px; }
.btn-primary.lg { padding: 15px 36px; font-size: 16px; }
.btn-primary.sm { padding: 10px 22px; font-size: 14px; }

.btn-outline-white {
  background: transparent;
  border: 1px solid rgba(255,255,255,0.35);
  color: rgba(255,255,255,0.85);
  padding: 13px 24px;
  border-radius: 8px;
  font-family: 'DM Sans', sans-serif;
  font-size: 15px;
  cursor: pointer;
  transition: border-color 0.2s, color 0.2s, background 0.2s;
}
.btn-outline-white:hover {
  border-color: #c9a84c;
  color: #c9a84c;
  background: rgba(201,168,76,0.07);
}

.hero-stats {
  display: flex; align-items: center; gap: 28px;
  animation: fadeUp 0.6s 0.4s ease both;
}
.stat-item { display: flex; flex-direction: column; gap: 3px; }
.stat-num {
  font-family: 'Playfair Display', serif;
  font-size: 28px; font-weight: 700;
  color: #c9a84c; line-height: 1;
}
.stat-label { font-size: 12px; color: rgba(255,255,255,0.6); letter-spacing: 0.04em; }
.stat-sep { width: 1px; height: 32px; background: rgba(255,255,255,0.15); }

/* CHAT CARD */
.hero-right { animation: fadeUp 0.7s 0.25s ease both; }
.chat-card {
  background: #ffffff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 40px 100px rgba(0,0,0,0.5);
}
.chat-card-header {
  display: flex; align-items: center; gap: 12px;
  padding: 16px 20px;
  background: #f8f6f2;
  border-bottom: 1px solid #ece9e2;
}
.chat-avatar { width: 36px; height: 36px; border-radius: 50%; }
.chat-card-info { display: flex; flex-direction: column; gap: 2px; }
.chat-name { font-size: 14px; font-weight: 500; color: #1a1a2e; }
.chat-online { display: flex; align-items: center; gap: 5px; font-size: 12px; color: #22c55e; }
.chat-online em { display: block; width: 6px; height: 6px; background: #22c55e; border-radius: 50%; animation: pulse 2s infinite; }

.chat-card-body {
  padding: 20px;
  display: flex; flex-direction: column; gap: 12px;
  min-height: 190px;
  background: #ffffff;
}
.chat-bubble {
  max-width: 84%;
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 13px; line-height: 1.6;
  opacity: 0; transform: translateY(6px);
  transition: opacity 0.4s ease, transform 0.4s ease;
}
.chat-bubble.visible { opacity: 1; transform: none; }
.chat-bubble.ai {
  background: #f3f0ea;
  color: #2a2a3e;
  align-self: flex-start;
  border-bottom-left-radius: 3px;
}
.chat-bubble.user {
  background: #c9a84c;
  color: #0a0c1a;
  align-self: flex-end;
  border-bottom-right-radius: 3px;
}
.cursor { color: #c9a84c; animation: blink 0.9s step-start infinite; }
@keyframes blink { 50%{opacity:0} }

.chat-card-footer {
  display: flex; align-items: center; gap: 10px;
  padding: 12px 16px;
  border-top: 1px solid #ece9e2;
  background: #f8f6f2;
}
.chat-input-mock {
  flex: 1; background: #fff;
  border: 1px solid #e0ddd5;
  border-radius: 8px; padding: 8px 12px;
  font-size: 13px; color: #aaa;
}
.chat-send {
  width: 32px; height: 32px;
  background: #c9a84c; border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; flex-shrink: 0;
}
.chat-send svg { width: 14px; height: 14px; color: #0a0c1a; }

.scroll-hint {
  position: absolute; bottom: 28px; left: 50%;
  transform: translateX(-50%);
  display: flex; flex-direction: column; align-items: center; gap: 8px;
  cursor: pointer;
  color: rgba(255,255,255,0.5);
  font-size: 11px; letter-spacing: 0.1em;
  z-index: 1;
  animation: fadeUp 1s 0.9s ease both;
}
.scroll-line {
  width: 1px; height: 36px;
  background: linear-gradient(to bottom, #c9a84c, transparent);
  animation: scrollAnim 1.6s ease-in-out infinite;
}
@keyframes scrollAnim {
  0%{transform:scaleY(0);transform-origin:top}
  50%{transform:scaleY(1);transform-origin:top}
  51%{transform:scaleY(1);transform-origin:bottom}
  100%{transform:scaleY(0);transform-origin:bottom}
}

/* FEATURES */
.lp-features {
  padding: 96px 0;
  background: #ffffff;
}
.section-header {
  text-align: center; margin-bottom: 56px;
  display: flex; flex-direction: column; align-items: center; gap: 12px;
}
.section-tag {
  color: #c9a84c; font-size: 12px; font-weight: 500;
  letter-spacing: 0.12em; text-transform: uppercase;
}
.section-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(28px, 3.5vw, 42px); font-weight: 700;
  color: #1a1a2e; letter-spacing: -0.01em;
}
.section-sub { font-size: 16px; color: #6b6b8a; max-width: 460px; text-align: center; }

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}
.feature-card {
  background: #faf8f4;
  border: 1px solid #e8e4dc;
  border-top: 3px solid #c9a84c;
  border-radius: 12px;
  padding: 28px 22px;
  display: flex; flex-direction: column; gap: 12px;
  opacity: 0; transform: translateY(20px);
  transition: box-shadow 0.2s, transform 0.2s;
}
.feature-card.visible { animation: fadeUp 0.55s ease both; }
.feature-card:hover {
  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
  transform: translateY(-4px);
}
.feature-icon { width: 38px; height: 38px; color: #c9a84c; }
.feature-icon svg { width: 100%; height: 100%; }
.feature-name { font-size: 16px; font-weight: 500; color: #1a1a2e; }
.feature-desc { font-size: 14px; line-height: 1.7; color: #6b6b8a; }

/* SHOWCASE */
.lp-showcase { padding: 96px 0; background: #f7f5f0; }
.showcase-row {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 72px; align-items: center; margin-bottom: 88px;
}
.showcase-row:last-child { margin-bottom: 0; }
.showcase-row.rev .showcase-text { order: 2; }
.showcase-row.rev .showcase-img-wrap { order: 1; }
.showcase-text { display: flex; flex-direction: column; gap: 16px; }
.showcase-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(26px, 3vw, 36px); font-weight: 700;
  color: #1a1a2e; line-height: 1.25;
}
.showcase-desc { font-size: 15px; line-height: 1.8; color: #6b6b8a; }
.showcase-list { display: flex; flex-direction: column; gap: 10px; list-style: none; }
.showcase-list li { display: flex; align-items: center; gap: 10px; font-size: 14px; color: #4a4a6a; }
.list-dot { width: 6px; height: 6px; background: #c9a84c; border-radius: 50%; flex-shrink: 0; }
.showcase-img-wrap {
  border-radius: 14px; overflow: hidden;
  aspect-ratio: 4/3;
  box-shadow: 0 16px 48px rgba(0,0,0,0.12);
}
.showcase-img-wrap img { width: 100%; height: 100%; object-fit: cover; }

/* CTA */
.lp-cta { padding: 80px 0; background: #0f1623; }
.cta-box {
  text-align: center;
  display: flex; flex-direction: column; align-items: center; gap: 18px;
  padding: 20px;
}
.cta-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(24px, 3.5vw, 40px); font-weight: 700;
  color: #ffffff; max-width: 580px; line-height: 1.3;
}
.cta-sub { font-size: 16px; color: rgba(255,255,255,0.6); }

/* FOOTER */
.lp-footer { padding: 36px 0; background: #ffffff; border-top: 1px solid #e8e4dc; }
.footer-inner { display: flex; align-items: center; justify-content: space-between; }
.footer-copy { font-size: 13px; color: #9a97b0; }

/* ANIMATIONS */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* RESPONSIVE */
@media (max-width: 900px) {
  .hero-content { grid-template-columns: 1fr; gap: 48px; padding-top: 110px; }
  .hero-right { display: none; }
  .features-grid { grid-template-columns: 1fr 1fr; }
  .showcase-row { grid-template-columns: 1fr; gap: 36px; }
  .showcase-row.rev .showcase-text { order: 0; }
  .showcase-row.rev .showcase-img-wrap { order: 0; }
  .footer-inner { flex-direction: column; gap: 12px; text-align: center; }
}
@media (max-width: 600px) {
  .features-grid { grid-template-columns: 1fr; }
  .lp-container { padding: 0 20px; }
}
</style>
