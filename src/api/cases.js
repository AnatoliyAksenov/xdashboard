import axios from 'axios';

import { BASE_URL } from '../api/default';
import { getHash } from '../utils/hash';

import router from '../router/index';

export function getCases(params){ 
    const hash = getHash(params || {});
    return axios.get(`${BASE_URL}/cases/all` + hash )
                .then(res => res.data)
                .catch( err => {
                    console.log(err);
                    router.push({'path': '/unauthorized'})
                });
};

export function getCase(id){
    return axios.get(`${BASE_URL}/cases/${id}`).then(res => res.data);
}

export function getUsers(){
    return axios.get(`${BASE_URL}/cases/ui/users`).then(res => res.data);
}