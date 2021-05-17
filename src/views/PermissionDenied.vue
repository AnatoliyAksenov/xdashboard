<template>
<div>
  <md-content>

        <h3>Отказано в доступе</h3>
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

<style>

</style>