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

Vue.use(Router)

export default new Router({
    routes: [{
        path: '/',
        name: 'Main',
        component: Main
    }, {
        path: '/signals',
        name: 'Signals',
        component: SignalList
    }, {
        path: '/signal/:id',
        name: 'Signal',
        component: SignalForm,
        props: true
    }, {
        path: '/cases',
        name: 'Cases',
        component: CaseList
    }, {
        path: '/case/:id',
        name: 'Case',
        component: CaseForm,
        props: true
    }, {
        path: '/instruments/:inn?',
        name: 'Instruments',
        component: Instruments,
        props: true
    }, {
        path: '/transactiongraph/:inn',
        name: 'Transaction Graph',
        component: TransactionGraph,
        props: true
    }]
})