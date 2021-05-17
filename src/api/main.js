import { get, post, del } from '../utils/http'; 

import { BASE_URL } from '../api/default';


export function get_signal_stat() {
        // get signal statistic for donuts
        return get(`${BASE_URL}/main/signals_stat`)
               .then(res => res.data);
    }
export function get_dictionary(key, fmt) {
        // gets dictionary data
        // available formats: list and dict
        // list: [{dict_val, dict_key}, ... ]
        // dict: {dict_key: dict_val, ... }
        return get(`${BASE_URL}/main/dict/${key}/${fmt}`)
               .then(res => res.data);
        
    }
