

<template>
  <div>
    <md-table v-model="filtered" :md-sort.sync="currentSort" :md-sort-order.sync="currentSortOrder" :md-sort-fn="customSort" md-card>
      <md-table-toolbar>
        <div class="md-toolbar-section-start">
          <div class="md-layout md-gutter">
            <div class="md-layout-item md-size-50">
              <md-datepicker v-model="date_from" :md-model-type="string" :md-immediately="true">
                <label>Период с</label>
              </md-datepicker>              
            </div>
            <div class="md-layout-item md-size-50">
              <md-datepicker v-model="date_to" :md-model-type="string" :md-immediately="true">
                <label>Период по</label>
              </md-datepicker>  
            </div>
          </div>
        </div>
        <div class="md-toolbar-section-end">
            <md-button class="md-icon-button md-primary">
              <md-icon>more_horiz</md-icon>            
            </md-button>
        </div>
      </md-table-toolbar>

      <md-table-empty-state
        md-label="No data found"
        :md-description="`No data found for this '${search}' query. Try a different search term.`">
      </md-table-empty-state>

      <md-table-row slot="md-table-row" slot-scope="{ item }">
        <md-table-cell md-label="ID" md-numeric>            
            <md-button class="md-primary" @click="formActive = true; formData = item">{{ item.id }} </md-button>
        </md-table-cell>
        <md-table-cell md-label="Name" md-sort-by="name">{{ item.name }}</md-table-cell>
        <md-table-cell md-label="Email" md-sort-by="email">{{ item.email }}</md-table-cell>
        <md-table-cell md-label="Gender" md-sort-by="gender">{{ item.gender }}</md-table-cell>
        <md-table-cell md-label="Job Title" md-sort-by="title">{{ item.title }}</md-table-cell>
      </md-table-row>
    </md-table>

    <!--Modal forms-->
    <md-dialog :md-active.sync="formActive">
        <md-dialog-title>Сводка по кейсу</md-dialog-title>
        <md-tabs md-dynamic-height>          
          <md-tab :md-label="'Заголовок'" v-for="tab in tabs" :key="tab.id">
              {{ tab.content }}
          </md-tab>
        </md-tabs>
    </md-dialog>
  </div>  
</template>

<script>
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
      sending: false,
      form: {},
      users: [
        {
          id: 1,
          name: 'Shawna Dubbin',
          email: 'sdubbin0@geocities.com',
          gender: 'Male',
          title: 'Assistant Media Planner'
        },
        {
          id: 2,
          name: 'Odette Demageard',
          email: 'odemageard1@spotify.com',
          gender: 'Female',
          title: 'Account Coordinator'
        },
        {
          id: 3,
          name: 'Lonnie Izkovitz',
          email: 'lizkovitz3@youtu.be',
          gender: 'Female',
          title: 'Operator'
        },
        {
          id: 4,
          name: 'Thatcher Stave',
          email: 'tstave4@reference.com',
          gender: 'Male',
          title: 'Software Test Engineer III'
        },
        {
          id: 5,
          name: 'Clarinda Marieton',
          email: 'cmarietonh@theatlantic.com',
          gender: 'Female',
          title: 'Paralegal'
        }
      ],
      tabs: [
          {
              title: "Default",
              content: "test",
              id: 1
          },
          {
              title: "Default2",
              content: "test2",
              id: 2
          },
      ]
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
      }
    },
    created(){
        this.filtered = this.users;
        //console.log(this.data);
    }
  }
</script>

<style>

</style>
