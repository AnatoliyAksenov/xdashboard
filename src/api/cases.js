import { get, post, del } from '../utils/http'; 

import { BASE_URL } from '../api/default';
import { getHash } from '../utils/hash';

export function getCases(params){ 
    const hash = getHash(params || {});
    return get(`${BASE_URL}/cases/all` + hash )
                .then(res => res.data);
};

export function getCase(id){
    return get(`${BASE_URL}/cases/${id}`).then(res => res.data);
}

export function getUsers(){
    return get(`${BASE_URL}/cases/ui/users`).then(res => res.data);
}