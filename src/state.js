import Vue from 'vue'
import Vuex from 'vuex'
import * as actions from './actions'
import * as getters from './getters'

Vue.use(Vuex)


const state = {    
    auth: localStorage.getItem('auth') || false,
    username: localStorage.getItem('username'),
    expired: localStorage.getItem('expired'),
    me: JSON.parse( localStorage.getItem('me') || '{}' )
}


const mutations = {
    setme(state, me) {
        state.me = me;
        localStorage.setItem('me', JSON.stringify(me) );
    },
    login(state) {
        state.auth = true;
        localStorage.setItem('auth', true);
    },
    logoff(state){
        state.auth = false;
        localStorage.setItem('auth', false);
        localStorage.setItem('me', '');
        localStorage.setItem('username', '');
        localStorage.setItem('expired', new Date() );
    },
    setusername(state, username) {
        state.username = username;
        localStorage.setItem('username', username);
    },
    setexpired(state, expired) {
        state.expired = expired;
        localStorage.setItem('expired', expired);
    }
}


export default new Vuex.Store({
    actions,
    getters,
    state,
    mutations
})