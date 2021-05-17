export function getSearch(){
    // The real window.location.search unavailable because the hash was used.

    const hash = window.location.hash;
    if( hash.split("?").length == 2  ){
        const query = hash.split('?')[1].split('&');
        const keys = query.reduce((r, e) => [...r, e.split('=')[0]], []);
        const values = query.reduce((r, e) => [...r, e.split('=').length == 2 ? e.split('=')[1]: undefined ], []);
        const result = keys.reduce( (r, e, i) => Object.assign(r, {[e]: values[i]}), {});

        return result
    }

    return undefined
}

export function getKey(key){
    const query = getQuery();
    if(query)
        return query[key]

    return undefined    
}

export function getHash(params){
    return '?' + Object.keys(params).reduce( (r, e) => r + '&' + e + (params[e] ? '='+ params[e]: ""), '').substr(1);
}

export function updateHash(param, newVal, oldVal){
    const hash = getSearch() || {};
    const start = window.location.hash.split('?')[0];
    if (newVal.length > 0){
        hash[param] = newVal;        
    } else {
        //clear 
        delete hash[param];
    }
    
    window.location.hash = start + getHash(hash);
    
}