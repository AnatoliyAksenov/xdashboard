<template>
  <div>
    <md-table v-model="data" :md-sort.sync="currentSort" :md-sort-order.sync="currentSortOrder" :md-sort-fn="customSort" md-card>
      <md-table-toolbar>
        <div class="md-toolbar-section-start">
          <div class="md-layout md-gutter">
            <div class="md-layout-item md-size-50">
              <md-datepicker v-model="date_from" :md-model-type="String" :md-immediately="true">
                <label>Период с</label>
              </md-datepicker>              
            </div>
            <div class="md-layout-item md-size-50">
              <md-datepicker v-model="date_to" :md-model-type="String" :md-immediately="true">
                <label>Период по</label>
              </md-datepicker>  
            </div>
          </div>
          <md-button class="md-icon-button" @click="showFilter=true;">
            <md-icon>more_horiz</md-icon>
          </md-button>
        </div>
        <div class="md-toolbar-section-end">
            <md-button class="md-icon-button md-primary" @click="updateTable();">
              <md-icon>refresh</md-icon>            
            </md-button>
        </div>
      </md-table-toolbar>

      <md-table-empty-state
        md-label="Загрузка данных"
        :md-description="`Загрузка данных еще идёт или возникли проблемы с загрузкой.`">
      </md-table-empty-state>

      <md-table-row slot="md-table-row" slot-scope="{ item }">
        <md-table-cell md-label="#" md-numeric>            
            <md-button class="md-primary md-dense" @click="formActive = true; formData = item">{{ item.id }} </md-button>
        </md-table-cell>
        <md-table-cell md-label="Событие" md-sort-by="type">{{ item.signal_type }}</md-table-cell>
        <md-table-cell md-label="Дата" md-sort-by="signal_date">{{ item.signal_date }}</md-table-cell>
        <md-table-cell md-label="Компания" md-sort-by="name">{{ item.name }}</md-table-cell>
        <md-table-cell md-label="Сумма" md-sort-by="summ">{{ item.signal_sum }}</md-table-cell>
        <md-table-cell md-label="ИНН" md-sort-by="inn">{{ item.inn }}</md-table-cell>
        <md-table-cell md-label="Аналитик" md-sort-by="analist">{{ item.os_user }}</md-table-cell>
      </md-table-row>
    </md-table>

    <!--Modal forms-->
    <md-dialog :md-active.sync="formActive">
        <md-dialog-title>Сводка по сигналу</md-dialog-title>
        <md-dialog-content>
          <signal-form :id="formData.id" />
        </md-dialog-content>
        <md-dialog-actions>
          <md-button class="md-primary" @click="formActive = false">Close</md-button>
        </md-dialog-actions>
    </md-dialog>
    <!--FILTER dialoge-->
    <md-dialog :md-active.sync="showFilter">
      <md-dialog-title>Расширенный фильтр</md-dialog-title>
      <md-dialog-content style="width: 300px; height: 350px;">
        <div class="md-layout md-gutter">
          <div class="md-layout-item">
            <md-field>
                <label>Сигналы</label>
                <md-select v-model="lst" name="sig_type" id="sig_type" multiple>
                  <md-option v-for="item in available_signals" :key="item.signal_type" :value="item.signal_type">
                    {{item.signal_type}}
                  </md-option>                      
                </md-select>  
            </md-field>
            <md-field>
              <label for="limit">Лимит строк</label>
              <md-select id="limit" name="limit" v-model="limit">
                <md-option value="50" key="50">{{50}}</md-option>
                <md-option value="100" key="100">{{100}}</md-option>
                <md-option value="500" key="500">{{500}}</md-option>
                <md-option value="1000" key="1000">{{1000}}</md-option>
              </md-select>
            </md-field>
          </div>
        </div>
      </md-dialog-content>  
      <md-dialog-actions>
        <md-button class="md-primary" @click="showFilter = false">Close</md-button>
      </md-dialog-actions>
    </md-dialog>
  </div>  
</template>

<script>
  import { getSignals } from '../api/signals';
  import { getSearch, getKey, updateHash } from '../utils/hash';

  import * as d3 from 'd3-time';
  import * as d3tf from 'd3-time-format';
  import SignalForm from './SignalForm.vue';

  //TODO: Move to utils
  const formatDate = d3tf.timeFormat('%Y-%m-%d')

  export default {
  components: { SignalForm },
    name: 'SignalList',
    data: () => ({
      currentSort: 'name',
      currentSortOrder: 'asc',
      search: null,
      formActive: false,
      formData: {},
      date_from: formatDate(new Date()),
      date_to:   formatDate(new Date()),
      sending: false,
      form: {},
      data: [],
      available_signals: [],
      count: 0,
      showFilter: false,
      //filter
      limit: 1000,
      offset: 0,
      order: 'n',
      lst: [], // list of selected signals
    }),
    methods: {
      customSort (value) {
        return value.sort((a, b) => {
          const sortBy = this.currentSort

          if (this.currentSortOrder === 'desc') {
            return a[sortBy].localeCompare(b[sortBy])
          }

          return b[sortBy].localeCompare(a[sortBy])
        })
      },
      searchOnTable(){
        this.filtered = this.users.filter( (e, v) => { e.name.toLowerCase().includes( this.search ) });
        //console.log(this.search);
      },
      fetchData(){
        const params = getSearch() || {};   
            
        return getSignals(params);
      },
      updateTable(){
        //resurrecting query params
        // const params = getSearch() || {};
        
        // this.date_from = params['date_from'] || formatDate( d3.timeDay.offset(new Date(), -3) );
        // this.date_to = params['date_to'] || formatDate( d3.timeDay.offset(new Date(), 3) );
        // this.limit = params['limit'] || 1000;
        // this.offset = params['offset'] || 0;
        // this.order = params['order'] || 'n';
        // this.lst = (params['lst'] || '').split(',');

        this.fetchData().then( data => {
          this.data = data[0];
          this.count = data[1];
          this.available_signals = data[2];
          
          console.log(this.available_signals);
        });          
      },
      updateDateFrom(newVal, oldVal){
        // const nv = window.location.hash.replace(`date_from=${oldVal}`, `date_from=${newVal}`);
        // window.location.hash = nv;
        updateHash('date_from', newVal, oldVal);
      },
      updateDateTo(newVal, oldVal){
        // const nv = window.location.hash.replace(`date_to=${oldVal}`, `date_to=${newVal}`);
        // window.location.hash = nv;
        updateHash('date_to', newVal, oldVal);
      },
      updateLimit(newVal, oldVal){
        // const nv = window.location.hash.replace(`limit=${oldVal}`, `limit=${newVal}`);
        // window.location.hash = nv;
        updateHash('limit', newVal, oldVal);
      },
      updateOffset(newVal, oldVal){
        // const nv = window.location.hash.replace(`offset=${oldVal}`, `offset=${newVal}`);
        // window.location.hash = nv;
        updateHash('offset', newVal, oldVal)
      },
      updateLst(newVal, oldVal){
        const n = newVal.join(',');
        const o = oldVal;
        updateHash('lst', n, o);
      }
    },
    beforeMount(){
      const params = getSearch() || {};
      this.date_from = params['date_from'] || formatDate( d3.timeDay.offset(new Date(), -3) );
      this.date_to = params['date_to'] || formatDate( d3.timeDay.offset(new Date(), 3) );
      this.limit = params['limit'] || 1000;
      this.offset = params['offset'] || 0;
      this.order = params['order'] || 'n';
      this.lst = (params['lst'] || '').split(',');

      updateHash('date_from', this.date_from, '');
      updateHash('date_to', this.date_to, '');
      updateHash('limit', this.limit, '');
      updateHash('offset', this.offset, '');
      updateHash('order', this.order, '');
      updateHash('lst', this.lst, '');
    },
    mounted(){
        // updating table and restore filtering from query params
        this.updateTable();        
    },
    watch: {
      // call again the method if the route changes 
      // or any part of rote hash
      '$route': 'updateTable',
      // call for change location
      'date_from': 'updateDateFrom',
      'date_to': 'updateDateTo',
      'limit': 'updateLimit',
      'offset': 'updateOffset',
      'lst': 'updateLst'
    },
  }
</script>

<style>

</style>
