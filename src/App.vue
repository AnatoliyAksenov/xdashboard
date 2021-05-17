<template>
  <div class="page-container">
    <div v-if="auth">
      <md-toolbar class="md-primary">
        <md-button class="md-icon-button" @click="sn = true">
          <md-icon>menu</md-icon>
        </md-button>
        <span class="md-title">X-Factor</span>

        <div class="md-toolbar-section-end">
          <md-button>{{ me.username }}</md-button>
          <md-button @click="logout()">
            <md-icon>logout</md-icon>
            Выход</md-button>
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
            <md-icon>gears</md-icon>
            <a class="md-list-item-text" href="/#/instruments" @click="sn = false">Инструменты</a>
          </md-list-item>

          <md-list-item>
            <md-icon>delete</md-icon>
            <a class="md-list-item-text" href="/#/cases" @click="sn = false">Кейсы</a>
          </md-list-item>

          <md-list-item>
            <md-icon>error</md-icon>
            <a class="md-list-item-text" href="/#/transactiongraph" @click="sn = false">Граф транзакций</a>
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
    <!-- LOGIN PAGE -->
    <div v-if="auth == false">
        <div class="centered-container">
    <md-content class="md-elevation-3">

      <div class="title">
        <img src="/static/X.png" style="width: 50px; height: 70px">
        <div class="md-title">X-Factor</div>
        <div class="md-body-1">Analitics board and monitoring.</div>
      </div>

      <div class="form">
        <md-field>
          <label>Логин</label>
          <md-input v-model="name" autofocus></md-input>
        </md-field>

        <md-field md-has-password>
          <label>Пароль</label>
          <md-input v-model="password" type="password"></md-input>
        </md-field>
      </div>

      <div class="actions md-layout md-alignment-center-space-between">
        <a href="/resetpassword">Reset password</a>
        <md-button class="md-raised md-primary" @click="process()">Log in</md-button>
      </div>

      <div class="loading-overlay" v-if="loading">
        <md-progress-spinner md-mode="indeterminate" :md-stroke="2"></md-progress-spinner>
      </div>

    </md-content>
    <div class="background" />
  </div>

    </div>  
  </div>
</template>


<script>
import { getToken, getMe, delToken } from './api/auth';
import SignalForm from './views/SignalForm.vue';

import * as d3 from 'd3-time';

import { mapGetters } from 'vuex';
import { mapActions } from 'vuex';

export default {
  components: { SignalForm },
  name: 'App',
  computed: {
  	...mapGetters([
      'auth',
      'username',
      'expired',
      'me'
    ])
    
  },
  data: () => ({
      sn: false,
      name: undefined,
      password: undefined,
      // auth: localStorage.getItem('auth') || false,
      // username: localStorage.getItem('username'),
      // expired: localStorage.getItem('expired'),
      // me: JSON.parse( localStorage.getItem('me') || '{}' )
  }),
  methods: {
    ...mapActions([
      'setme', 
      'login',
      'logoff',
      'setusername',
      'setexpired'
    ]),
    process(){
      const username = this.name;
      const password = this.password;
      getToken(username, password).then( data => {
        // console.log(data);
        if( data == 'Success'){
          this.login();
          //this.auth = true;
          //localStorage.setItem('auth', true);

          const expired = d3.timeMinute(new Date(), 45);
          this.setexpired(expired);
          //this.expired = expired;
          //localStorage.setItem('expired', expired);
          this.password = 'deleted;';
          getMe().then( data => {
            this.setme(data);
            //this.me = data;
            //localStorage.setItem('me', JSON.stringify(data))
            //console.log(data)
          });

          const returnto = localStorage.getItem('returnto');
          localStorage.setItem('returnto', '');
          if(returnto.length > 0){
            this.$router.push({'path': returnto});
          }
        }
      })
    },
    logout(){
      delToken().then( res => {
        if(res == 'Success'){
          //this.auth = false;
          //localStorage.setItem('auth', false);
          this.logoff();
          //this.me = {};
          //localStorage.setItem('me', '');
          this.setme('');
          //this.expired = undefined;
          //localStorage.setItem('expired', this.expired);
          this.setexpired(undefined);
          //this.$route.redirect('/logout');
        }
      })
    }
  },
  created(){

  }
}
</script>

<style >
  .centered-container {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  height: 100vh;
  }

  .centered-container .title {
    text-align: center;
    margin-bottom: 30px;
  }

  .centered-container .title img {
      margin-bottom: 16px;
      max-width: 80px;
  }
  
  .centered-container .title .actions {
  }

  .centered-container .title .actions .md-button {
    margin: 0;
  }
  
  .centered-container .form {
    margin-bottom: 60px;
  }

  .centered-container .background {
    /*background: url('/static/X.png');*/
    position: absolute;
    height: 100%;
    width: 100%;
    top: 0;
    bottom: 0;
    right: 0;
    left: 0;
    z-index: 0;
    background-size: 700px;
    background-repeat: no-repeat;
    background-position: center;
  }
  .centered-container .md-content {
    z-index: 1;
    padding: 40px;
    width: 100%;
    max-width: 400px;
    position: relative;
  }
  .centered-container .loading-overlay {
    z-index: 10;
    top: 0;
    left: 0;
    right: 0;
    position: absolute;
    width: 100%;
    height: 100%;
    background: rgba(255, 255, 255, 0.9);
    display: flex;
    align-items: center;
    justify-content: center;
  }

</style>

