<template>
  <div id="app">
    <feedbackPopup/>
  </div>
</template>

<script>
import feedbackPopup from './components/feedbackPopup.vue'

export default {
  name: 'App',
  components: {
    feedbackPopup
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
