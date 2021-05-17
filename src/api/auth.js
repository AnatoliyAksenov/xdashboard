import { get, post, del } from '../utils/http'; 
import { BASE_URL } from '../api/default';
import { getHash } from '../utils/hash';

import router from '../router/index';

export function getToken(username, password){   
    const data = {"username": username, "password": password};

    return post(`${BASE_URL}/auth/token`, data)
           .then(res => res.data);
};

export function delToken(){
    return del(`${BASE_URL}/auth/token`)
           .then(res => res.data);
};

export function getMe(){
    return get(`${BASE_URL}/auth/me`)
                .then(res => res.data);
};
