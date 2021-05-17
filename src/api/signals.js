import { get, post, del } from '../utils/http'; 

import { BASE_URL } from '../api/default';
import { getHash } from '../utils/hash';

export function getSignals(params){ 
    const hash = getHash(params);
    return get(`${BASE_URL}/signals/all` + hash ).then(res => res.data);
};

export function getSignal(id){
    return get(`${BASE_URL}/signals/${id}`).then(res => res.data);
}
