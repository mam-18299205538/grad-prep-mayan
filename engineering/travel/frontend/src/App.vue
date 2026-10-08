<template>
  <a-config-provider :theme="theme">
    <div class="app-shell">
      <header class="site-nav">
        <router-link to="/" class="brand" aria-label="返回旅行助手首页">
          <span class="brand-mark" aria-hidden="true">✦</span>
          <span>旅程设计</span>
        </router-link>

        <nav class="site-nav-links" aria-label="主导航">
          <router-link to="/">规划旅程</router-link>
          <a href="/#how-it-works">使用方式</a>
        </nav>

        <div class="nav-status">
          <span class="status-dot" aria-hidden="true"></span>
          <span>智能规划已就绪</span>
        </div>
      </header>

      <main class="app-main">
        <router-view />
      </main>

      <footer class="site-footer">
        <span>旅行，不必赶路。</span>
        <span>AI Trip Planner</span>
      </footer>
    </div>
  </a-config-provider>
</template>

<script setup lang="ts">
const theme = {
  token: {
    colorPrimary: '#5b5b61',
    colorInfo: '#5b5b61',
    borderRadius: 16,
    fontFamily:
      '-apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "PingFang SC", "Segoe UI", sans-serif'
  }
}
</script>

