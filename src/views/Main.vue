<template>
	<donut v-bind:param="'drops'" v-bind:idname="'drops'" v-bind:data="signal_data.filter( e => e.signal_type == 'drops' )"/>
</template>

<script>
    import donut from '../components/Donut'
    import {get_signal_stat} from '../api/main'

	export default {
        components: { donut },
        data: () => ({
            signal_data: []
        }),
        beforeCreate(){
            this.signal_data = get_signal_stat()
        }
	}

</script>

<style scoped>

</style>