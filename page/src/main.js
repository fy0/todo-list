import Vue from 'vue'
import VueRouter from 'vue-router'

import "lodash"
import "purecss"
import "./assets/css/base.css"
import api from "./netapi.js"
import tools from "./tools.js"
import state from "./state.js"

import App from './app.vue'
import Index from './components/index.vue'
import SignIn from './components/signin.vue'
import SignUp from './components/signup.vue'

Vue.use(VueRouter)

let signOut = function (to, from, next) {
    api.userSignout();
}

var routes = [
    { path: '/', component: Index, meta: {visibility: 'all'} },
    { path: '/active', component: Index, meta: {visibility: 'active'} },
    { path: '/completed', component: Index, meta: {visibility: 'completed'} },
    { path: '/signin', component: SignIn },
    { path: '/signup', component: SignUp },
    { path: '/signout', template: '', beforeEnter: signOut },
]

var router = new VueRouter({
    routes: routes
})

new Vue({
    el: '#app',
    router: router,
    render: h => h(App),
}).$mount('#app')
