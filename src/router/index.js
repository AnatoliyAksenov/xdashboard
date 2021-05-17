import Vue from 'vue'
import Router from 'vue-router'
import Main from '@/views/Main'
import SignalList from '@/views/SignalList'
import SignalForm from '@/views/SignalForm'
// import SignalDialog from '@/views/SignalDialog'
import CaseList from '@/views/CaseList'
import CaseForm from '@/views/CaseForm'
import Instruments from '@/views/Instruments'
import TransactionGraph from '@/views/TransactionGraph'

import Unauthorized from '@/views/Unauthorized'
import PermissionDenied from '@/views/PermissionDenied'

Vue.use(Router)

const header = 'X-Factor';

const router = new Router({
    routes: [{
        path: '/',
        name: 'Main',
        component: Main,
        meta:{ title: 'Статистика по сигналам ' + header}
    }, {
        path: '/signals',
        name: 'Signals',
        component: SignalList,
        meta:{ title: 'Список сигналов ' + header}
    }, {
        path: '/signal/:id',
        name: 'Signal',
        component: SignalForm,
        props: true,
        meta:{ title: 'Сигнал ' + header}
    }, {
        path: '/cases',
        name: 'Cases',
        component: CaseList,
        meta:{ title: 'Список кейсов ' + header}
    }, {
        path: '/case/:id',
        name: 'Case',
        component: CaseForm,
        props: true,
        meta:{ title: 'Кейс ' + header}
    }, {
        path: '/instruments/:inn?',
        name: 'Instruments',
        component: Instruments,
        props: true,
        meta:{ title: 'Инструменты '  + header}
    }, {
        path: '/transactiongraph/:inn?',
        name: 'Transaction Graph',
        component: TransactionGraph,
        props: true,
        meta:{ titile: 'Граф по транзакциям ' + header}
    },{
        path: '/unauthorized',
        name: 'Unauthorized',
        component: Unauthorized,
        meta:{ title: 'Ошибка авторизации ' + header}
    },{
        path: '/permissiondenied',
        name: 'PermissionDenied',
        component: PermissionDenied,
        meta:{ title: 'Доступ заблокирован ' + header}
    }]
});

router.beforeEach((to, from, next) => {
    console.log(to);
    //const toto = to.matched[0];
    //document.title = toto.meta.title;
    document.title = to.meta.title;
    next();

})

export default router;