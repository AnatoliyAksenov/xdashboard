<template>
<div>
  <div class="md-layout md-gutter">
    <div class="md-layout-item md-size-100" style="padding-left: 20px;">
      <h3>Кейс {{main.id}}</h3>
    </div>
  </div>
  <div class="md-layout md-gutter">  
    <div class="md-layout-item md-size-100" style="padding-left: 20px;">
      <md-table>
        <md-table-row>
          <md-table-cell>Заголовок</md-table-cell>
          <md-table-cell>{{main.caption}}</md-table-cell>
        </md-table-row>
        <md-table-row>
          <md-table-cell>Статус</md-table-cell>
          <md-table-cell>{{ case_status[ main.status_id ] }}</md-table-cell>
        </md-table-row>
        <md-table-row>
          <md-table-cell>Риск руб</md-table-cell>
          <md-table-cell>{{main.risk_amount}} руб. на {{main.risk_date}}</md-table-cell>
        </md-table-row>
        <md-table-row>
          <md-table-cell>Уровень</md-table-cell>
          <md-table-cell>{{ hazard_level[ main.hazard_level] }}</md-table-cell>
        </md-table-row>
        <md-table-row>
          <md-table-cell>Основная идея</md-table-cell>
          <md-table-cell><pre>{{main.report}}</pre></md-table-cell>
        </md-table-row>
        <md-table-row>
          <md-table-cell>Аналитик</md-table-cell>
          <md-table-cell>{{ users[main.user_id].cn }}</md-table-cell>
        </md-table-row>
      </md-table>
    </div>


    <div class="md-layout-item md-size-100">
      <md-tabs class="md-transparent" md-active-tab="0">        
        <md-tab id="0">
        </md-tab>
      </md-tabs>
    </div>
  </div>
</div>
</template>


<script>
  import { getCase, getUsers } from '../api/cases';
  import main from '../api/main';

  export default {
    props: ['id'],
    name: 'SignalForm',
    data: () => ({
      main: {},
      tabs: [],
      hazard_level: {},
      case_status: {},
      users: {},
    }),
    methods: {
      fetchData(){
        return getCase(this.id);
      },
      fetchUsers(){
        return getUsers();
      },
      updateForm(){
        this.fetchData().then( data => {
          this.main = data[0][0];
          this.signals = data[1];
          this.actions = data[2];
          this.attachments = data[3];
          this.accounts = data[4];

          console.log(this.main);
        })
      }
    },
    mounted(){
        this.updateForm();
        main.get_dictionary('HAZARD_LEVEL', 'dict').then( data => {
          this.hazard_level = data;
        });
        main.get_dictionary('CASE_STATUS', 'dict').then( data => {
          this.case_status = data;
        });
        this.fetchUsers().then( data => {
          this.users = data.reduce( (r, e) => Object.assign(r, {[e['id']]: e}), {});
        })

    },
    watch: {
      // call again the method if the route changes
      '$route': 'updateForm',
    }
  }
</script>