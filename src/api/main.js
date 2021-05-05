import axios from 'axios';

import { BASE_URL } from '../api/default';

export default {
    get_signal_stat: function() {
        // get signal statistic for donuts
        axios.get(`${BASE_URL}/main/stat/signals_info`).then(res => res.data).then(data => {
            return data;
        }).catch( err => {
            console.log(err);
            return [];
        });
    },
    get_dictionary: function(key, fmt) {
        // gets dictionary data
        // available formats: list and dict
        // list: [{dict_val, dict_key}, ... ]
        // dict: {dict_key: dict_val, ... }
        return axios.get(`${BASE_URL}/main/dict/${key}/${fmt}`).then(res => res.data);
        
    }
};