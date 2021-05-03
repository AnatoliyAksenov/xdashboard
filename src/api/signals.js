import axios from 'axios';

import { BASE_URL } from '../api/default';
import { getHash } from '../utils/hash';

export function getSignals(params){ 
    const hash = getHash(params);
    return axios.get(`${BASE_URL}/signals/all` + hash ).then(res => res.data);
};

export function getSignal(id){
    return axios.get(`${BASE_URL}/signals/${id}`).then(res => res.data);
}
