<template>
  <div>
    <span v-if="value">Value: {{ value }}</span>
    <span>Id: {{ username }}</span>
    <span>IID: {{ id }}</span>
  </div>
</template>

<script>
  export default {
    props: ['id'],
    name: 'SignalForm',
    data: () => ({
      active: false,
      value: null,      
    }),
    computed: {
      username() {
        return this.$route.params.id
      }
    },
    methods: {
    }
  }
</script>