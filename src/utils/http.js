import axios from 'axios';
import router from '../router';

import store from '../state';


export function get(url) {
    return axios.get( url )
                .catch( err => {
                    //Process errors
                    if(err.response.status == '403'){
                        router.push({'path': '/permissiondenied'});
                    }

                    if(err.response.status == '401'){
                        localStorage.setItem('returnto', router.currentRoute.path);
                        store.commit('logoff');
                        
                    }

                    if(err.response.status == '500'){
                        
                        console.log(err);
                                                
                    }

                    console.log(err);
                    
                });

}

export function post(url, data) {
    return axios.post( url, data )
                .catch( err => {
                    if(err.response.status == '403'){
                                               
                        router.push({'path': '/permissiondenied'});
                    }

                    if(err.response.status == '401'){
                        
                        localStorage.setItem('returnto', router.currentRoute.path);
                        store.commit('logoff');
                                                
                    }

                    if(err.response.status == '500'){
                        
                        console.log(err);
                                                
                    }

                    console.log(err);
                    
                });

}

export function del(url) {
    return axios.delete( url )
                .catch( err => {
                    if(err.response.status == '403'){
                        router.push({'path': '/permissiondenied'});
                    }

                    if(err.response.status == '401'){
                        store.commit('logoff');
                    }

                    if(err.response.status == '500'){
                        
                        console.log(err);
                                                
                    }

                    console.log(err);
                    
                });

}