import BASE_URL from './default'

export default {
    get_signal_stat: function() {
        // get signal statistic for donuts
        const response = fetch(BASE_URL + '/stat/signals_info'); //
        const data = response.json();
        return data;
    }
};