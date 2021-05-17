export const setme = (state, me) => {
    state.commit('setme', me);
}

export const login = (state) => {
    state.commit('login');
}

export const logoff = (state) => {
    state.commit('logoff');
}

export const setusername = (state, username) => {
    state.commit('setusername', username);
}

export const setexpired = (state, expired) => {
    state.commit('setexpired', expired);
}