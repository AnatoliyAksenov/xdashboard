<template>
	<donut v-if="isMounted" v-bind:param="this.param" v-bind:idname="this.name" v-bind:data="signal_data.filter( e => e.name == this.name && e.report_date == this.report_date )"/>
</template>

<script>
    import donut from '../components/Donut'
    import {get_signal_stat} from '../api/main'

	export default {
        components: { donut },
        data: () => ({
            signal_data: [],
            isMounted: false,
            report_date: '2020-09-30',
            param: 'summ',
            name: 'drops'
        }),
        methods: {
            getData(){
                return get_signal_stat();
            }
        },
        beforeMount(){
             this.getData().then( data => {
                 this.signal_data = data;
                 window.signal_data = data;
                 this.isMounted = true;
             })
        }
	}

</script>

<style scoped>

</style>