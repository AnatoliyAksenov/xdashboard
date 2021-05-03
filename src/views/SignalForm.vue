<template>
  <div class="md-layout md-gutter">
    <div class="md-layout-item md-size-100">
      <h1>{{ main.signal_type }} {{ main.name }}</h1>
      <h3>{{ main.signal_date }}</h3>
      <h3>{{ main.inn }}</h3>
    </div>
    <div class="md-layout-item md-size-100">
      <md-tabs class="md-transparent" md-active-tab="0">        
        <md-tab v-for="(tab, index) in visible_tabs" :key="index" v-bind:md-label="tab.title">
          <!--Show tab data like key-value dictionary-->
          <md-tab-body v-if="tab.content_type == 'dict'">
            <h3>{{ tab.title }}</h3>
            <md-table>
              <md-table-row v-for="(value, name, index) in tab.data[0]" :key="name" >
                <md-table-cell>{{ tab.columns[ index ] }}</md-table-cell>
                <md-table-cell v-if="name != 'comment'">{{ value }}</md-table-cell>
                <md-table-cell v-if="name == 'comment'"><pre>{{ value }}</pre></md-table-cell>
              </md-table-row>
            </md-table>
          </md-tab-body>
          <md-tab-body v-if="tab.content_type == 'list'">
            <h3>{{ tab.title }}</h3>
            <md-table>
              <md-table-row>
                <md-table-head v-for="(col, index) in tab.sp_cols" :key="index">
                  {{col}}
                </md-table-head>  
              </md-table-row>
              <md-table-row v-for="(item, index) in tab.data" :key="index">                
                <md-table-cell v-for="(cell, index) in item" :key="index">
                  {{cell}}
                </md-table-cell>                
              </md-table-row>
            </md-table>
          </md-tab-body>
        </md-tab>
        
      </md-tabs>
    </div>
  </div>
</template>

<script>
  import { getSignal } from '../api/signals';

  export default {
    props: ['id'],
    name: 'CaseForm',
    data: () => ({
      main: {},
      tabs: []      
    }),
    methods: {
      fetchData(){
        return getSignal(this.id);
      },
      updateForm(){
        this.fetchData().then( data => {
          const tabs = data[0];
          const prep = tabs.reduce( (r, e) => [...r, Object.assign(e, {"columns": e.columns.split(',').map(ee => ee.trim())})], []);
          this.all_tabs = prep;
          this.visible_tabs = this.all_tabs.filter( e => e.visible == 1);

          this.main = data[1];
          console.log(this.all_tabs);
          console.log(this.main)
        })
      }
    },
    created(){
      this.updateForm();
    },
    watch: {
      '$route': 'updateForm',
    }
  }
</script>