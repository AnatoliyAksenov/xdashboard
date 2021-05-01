<template>
  <div>
    <span>INN: {{ inn }}</span>
  </div>
</template>

<script>
  export default {
    props: [
      'inn',
      'date',
      'summ'
      ],    
    name: 'TransactionGraph',
    data: () => ({    
    }),
    methods: {
    }
  }
</script>