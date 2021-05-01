import BASE_URL from './default'

export default {
    get_signals: function() {
        const response = fetch(BASE_URL + '/signals/all'); //
        const data = response.json();
        return data;
    }
};