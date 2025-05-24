<template>
  <div id="app">
    <Navigation v-if="isAuthenticated" />
    <div class="main-content" :class="{ 'with-nav': isAuthenticated }">
      <router-view/>
    </div>
  </div>
</template>

<script>
import Navigation from './components/Navigation'

export default {
  name: 'App',
  components: {
    Navigation
  },
  computed: {
    isAuthenticated() {
      return !!localStorage.getItem('token')
    }
  }
}
</script>

<style>
@import './assets/styles.css';

#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.main-content {
  padding: 20px;
  min-height: 100vh;
}

.main-content.with-nav {
  margin-left: 250px;
  padding: 20px 40px;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}</style>