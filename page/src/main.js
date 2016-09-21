import Vue from 'vue'
import VueRouter from 'vue-router'

import "purecss"
import "./assets/css/base.css"
import tools from "./tools.js"
import state from "./state.js"

import App from './app.vue'
import Index from './components/index.vue'
import SignIn from './components/signin.vue'
import SignUp from './components/signup.vue'

Vue.use(VueRouter)

var routes = [
    { path: '/', component: Index, meta: {visibility: 'all'} },
    { path: '/active', component: Index, meta: {visibility: 'active'} },
    { path: '/completed', component: Index, meta: {visibility: 'completed'} },
    { path: '/signin', component: SignIn },
    { path: '/signup', component: SignUp },
]

var router = new VueRouter({
    routes: routes
})

new Vue({
    el: '#app',
    router: router,
    render: h => h(App),
}).$mount('#app')
