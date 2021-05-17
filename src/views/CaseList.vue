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
        <md-table-cell md-label="Заголовок" md-sort-by="caption">{{ item.caption }}</md-table-cell>
        <md-table-cell md-label="Сумма риска" md-sort-by="risk_amount">{{ item.risk_amount }}</md-table-cell>
        <md-table-cell md-label="Дата риска" md-sort-by="risk_date">{{ item.risk_date }}</md-table-cell>
        <md-table-cell md-label="Изменено" md-sort-by="last_update">{{ item.last_update }}</md-table-cell>
        <md-table-cell md-label="Обоснование" md-sort-by="report">{{ item.report }}</md-table-cell>
      </md-table-row>
    </md-table>

    <!--Modal forms-->
    <md-dialog :md-active.sync="formActive">
        <md-dialog-title>Сводка по кейсу</md-dialog-title>
        <md-dialog-content>
          <div :id="formData.id"></div>
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
  import { getCases } from '../api/cases';
  import { getSearch, getKey, updateHash } from '../utils/hash';

  import * as d3 from 'd3-time';

  export default {
    name: 'CaseList',
    data: () => ({
      currentSort: 'name',
      currentSortOrder: 'asc',
      search: null,
      filtered: [],
      formActive: false,
      date_from: new Date(),
      date_to:   new Date(),
      limit: 1000,
      offset: 0,
      sending: false,
      data: [],
      formData: {}
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
        return getCases();
      },
      updateTable(){
        const params = getSearch() || {};

        this.date_from = params['date_from'] || d3.timeDay.offset(new Date(), -3);
        this.date_to = params['date_to'] || d3.timeDay.offset(new Date(), 3);
        this.limit = params['limit'] || 1000;
        this.offset = params['offset'] || 0;

        this.fetchData().then( data => {
          this.data = data;
        });
      }
    },
    mounted(){
        this.updateTable()
    },
    watch: {
      // call again the method if the route changes
      '$route': 'updateTable',
    }
  }
</script>

<style>

</style>
