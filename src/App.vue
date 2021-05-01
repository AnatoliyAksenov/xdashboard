<template>
  <div class="page-container">
    <md-toolbar class="md-primary">
      <md-button class="md-icon-button" @click="sn = true">
        <md-icon>menu</md-icon>
      </md-button>
      <span class="md-title">X-Factor</span>

      <div class="md-toolbar-section-end">
        <!-- <md-button @click="showSidepanel = true">Favorites</md-button> -->
      </div>
    </md-toolbar>

    <md-drawer :md-active.sync="sn" md-swipeable style="width:250px">
      <md-toolbar class="md-transparent" md-elevation="0">
        <span class="md-title">X-Factor</span>
      </md-toolbar>

      <md-list>
        <md-list-item>
          <md-icon>move_to_inbox</md-icon>
          <a class="md-list-item-text" href="/#/" @click="sn = false">Статистика</a>
        </md-list-item>

        <md-list-item>
          <md-icon>move_to_inbox</md-icon>
          <a class="md-list-item-text" href="/#/signals" @click="sn = false">Сигналы</a>
        </md-list-item>

        <md-list-item>
          <md-icon>gear</md-icon>
          <a class="md-list-item-text" href="/#/instruments" @click="sn = false">Инструменты</a>
        </md-list-item>

        <md-list-item>
          <md-icon>delete</md-icon>
          <a class="md-list-item-text" href="/#/cases" @click="sn = false">Кейсы</a>
        </md-list-item>

        <md-list-item>
          <md-icon>error</md-icon>
          <a class="md-list-item-text" href="/#/transactoingraph" @click="sn = false">Граф транзакций</a>
        </md-list-item>
      </md-list>
    </md-drawer>

    <!-- <md-drawer class="md-right" :md-active.sync="showSidepanel">
      <md-toolbar class="md-transparent" md-elevation="0">
        <span class="md-title">Favorites</span>
      </md-toolbar>

      <md-list>
        <md-list-item>
          <span class="md-list-item-text">Abbey Christansen</span>

          <md-button class="md-icon-button md-list-action">
            <md-icon class="md-primary">chat_bubble</md-icon>
          </md-button>
        </md-list-item>

        <md-list-item>
          <span class="md-list-item-text">Alex Nelson</span>

          <md-button class="md-icon-button md-list-action">
            <md-icon class="md-primary">chat_bubble</md-icon>
          </md-button>
        </md-list-item>

        <md-list-item>
          <span class="md-list-item-text">Mary Johnson</span>

          <md-button class="md-icon-button md-list-action">
            <md-icon>chat_bubble</md-icon>
          </md-button>
        </md-list-item>
      </md-list>
    </md-drawer> -->

    <md-content>
      <router-view/>
    </md-content>
  </div>
</template>


<script>
export default {
  name: 'App',
  data: () => ({
      sn: false
  })
}
</script>

<style>
  
</style>

