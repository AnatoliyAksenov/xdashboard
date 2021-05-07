<template>
<div>
  <md-content>

        <h3>Ошибка авторизации</h3>
        <md-button class="md-raised md-primary" @click="$router.go(-2)">
          Назад
        </md-button>
        <md-button class="md-raised md-accent">
          Запросить права
        </md-button>

  </md-content>
</div>
</template>

<script>
  export default {
  }
</script>

<style scoped>
  .md-content {
    width: 200px;
    height: 200px;
    display: inline-flex;
    justify-content: center;
    align-items: center;
  }
</style>