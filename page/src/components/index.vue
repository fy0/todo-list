<template>
<div class="container">
    <div class="nav" v-if="state.data.user">
        你好，{{state.data.user.username}}
        <router-link :to="{ path: '/signout' }">注销</router-link>

    </div>
    <div class="nav" v-else>
        <router-link :to="{ path: '/signup' }">注册</router-link>
        <router-link :to="{ path: '/signin' }">登录</router-link>
    </div>
    <section class="todoapp">
        <header class="header">
            <h1>todos</h1>
            <input class="new-todo"
                autofocus autocomplete="off"
                placeholder="我们准备做些什么？"
                v-model="newTodo"
                @keyup.enter="addTodo">
        </header>
        <section class="main" v-show="todos.length" v-cloak>
            <input class="toggle-all" type="checkbox" v-model="allDone">
            <ul class="todo-list">
                <li v-for="todo in filteredTodos"
                    class="todo"
                    :key="todo.id"
                    :class="{ completed: todo.completed, editing: todo == editedTodo }">
                    <div class="view">
                        <input class="toggle" type="checkbox" v-model="todo.completed">
                        <label @dblclick="editTodo(todo)">{{ todo.title }}</label>
                        <span class="info">
                            <div>
                                <span class="author">{{todo.user.username}}</span>
                                <span class="time">{{time_to_text(todo.time)}}</span>
                            </div>
                            <div v-if="todo.completed">
                                <span>{{time_to_text(todo.done_time)}}</span>
                                <span style="color:#000">完成</span>
                            </div>
                            <div v-if="todo.completed">
                                <span>by:</span>
                                <span class="partner" v-if="todo.partner1">{{todo.partner1.username}}</span>
                            </div>
                        </span>
                        <div class="right">
                            <button class="destroy" @click="removeTodo(todo)"></button>
                        </div>
                    </div>
                    <input class="edit" type="text"
                        v-model="todo.title"
                        v-todo-focus="todo == editedTodo"
                        @blur="doneEdit(todo)"
                        @keyup.enter="doneEdit(todo)"
                        @keyup.esc="cancelEdit(todo)">
                </li>
            </ul>
        </section>
        <footer class="footer" v-show="todos.length" v-cloak>
            <span class="todo-count">
                <strong>{{ remaining }}</strong> {{ remaining | pluralize }} 剩余
            </span>
            <ul class="filters">
                <li><router-link :class="{ selected: visibility == 'all' }" :to="{ path: '/' }">全部</router-link></li>
                <li><router-link :class="{ selected: visibility == 'active' }" :to="{ path: '/active' }">待做</router-link></li>
                <li><router-link :class="{ selected: visibility == 'completed' }" :to="{ path: '/completed' }">已完成</router-link></li>
            </ul>
            <button style="display:none" class="clear-completed" @click="removeCompleted">
                清除已完成
            </button>
        </footer>
    </section>
    <footer class="info">
        <p>双击编辑待做事项</p>
    </footer>
</div>
</template>

<style>
.nav {
    top: 2%;
    right: 3%;
    position: absolute;
}

.view > .info {
    position: absolute;
    right: 38px;
    top: 0;
    bottom: 0;
    margin: auto 0;
    text-align: right;
    display: table;
}

.view > .info > div:first-child {
}

.view > .info div {
    line-height: 15px;
}

.view > .info .author {
    color: rgb(15, 175, 175);
    font-size: small;
}

.view > .info .time {
    color: rgb(153, 153, 153);
    font-size: small;
}

.view > .info .partner {
    color: rgb(175, 15, 175);
}
</style>

<script>
import Vue from 'vue'
import api from "../netapi.js"
import state from "../state.js"

let vm = null; // tmp fix for router callback bug

// visibility filters
var filters = {
    all: function (todos) {
        return todos
    },
    active: function (todos) {
        return todos.filter(function (todo) {
            return !todo.completed
        })
    },
    completed: function (todos) {
        return todos.filter(function (todo) {
            return todo.completed
        })
    }
}

export default {
    data () {
        return {
            state: state,
            todos: [],
            last_save: {},
            newTodo: '',
            editedTodo: null,
            visibility: 'all',
            saveEnable: false
        }
    },

    filters: {
        pluralize: function (n) {
            //return n === 1 ? 'item' : 'items'
            return '项'
        }
    },

    computed: {
        filteredTodos: function () {
            return filters[this.visibility](this.todos)
        },
        remaining: function () {
            return filters.active(this.todos).length
        },
        allDone: {
            get: function () {
                return this.remaining === 0
            },
            set: function (value) {
                // TODO: 这一下把任务全都完成了，可不能要。临时隐藏起来以作他用
                /*this.todos.forEach(function (todo) {
                    todo.completed = value
                })*/
            }
        }
    },
    methods: {
        addTodo: async function () {
            var value = this.newTodo && this.newTodo.trim()
            if (!value) {
                return
            }
            if (!state.data.user) {
                alert('请先登录！');
                return;
            }
            let ret = await api.todoAdd(value);
            if (ret.code == 0) {
                ret.todo.completed = false;
                this.todos.splice(0, 0, ret.todo);
                this.newTodo = '';
            } else {
                alert(`发生了错误，文本是不是过长了？ ${ret.code}`);
            }
        },

        removeTodo: async function (todo) {
            let ret = await api.todoRemove(todo.id);
            if (ret.code == 0) {
                this.todos.splice(this.todos.indexOf(todo), 1)
            } else {
                alert(`发生了错误，你是否在试图删除他人建立的 TODO？ ${ret.code}`);
            }
        },

        editTodo: function (todo) {
            this.beforeEditCache = todo.title
            this.editedTodo = todo
        },

        doneEdit: function (todo) {
            if (!this.editedTodo) {
                return
            }
            this.editedTodo = null
            todo.title = todo.title.trim()
            if (!todo.title) {
                this.removeTodo(todo)
            }
        },

        cancelEdit: function (todo) {
            this.editedTodo = null
            todo.title = this.beforeEditCache
        },

        removeCompleted: function () {
            this.todos = filters.active(this.todos)
        },

        time_to_text: $.time_to_text,

        doSave: _.debounce(async function () {
            if (this.saveEnable) {
                let todos = {}
                let modified = []
                for (let i of this.todos) todos[i.id] = i;

                for (let i of this.todos) {
                    let old = this.last_save[i.id];
                    if (!_.isEqual(i, old)) {
                        modified.push(i);
                    }
                }

                let ret = await api.todoBatchSave(this.todos);
                if (ret.code != 0) return;
                for (let i of ret.modified) {
                    for (let k of Object.keys(i)) {
                        todos[i.id][k] = i[k];
                        if (this.last_save[i.id] == null) this.last_save[i.id] = {};
                        this.last_save[i.id][k] = i[k];
                    }
                }
                console.log('保存完毕', ret)
            }
        }, 700)
    },
    mounted: async function () {
        vm = this;
        let ret = await api.todoGet();
        Vue.set(this, 'todos', ret.data);

        for (let i of _.cloneDeep(ret.data)) {
            this.last_save[i.id] = i;
        }

        if (this.$route.meta.visibility) {
            Vue.set(this, 'visibility', this.$route.meta.visibility);
        }

        let uret = await api.userInfo();
        if (uret.code == 0) {
            Vue.set(state.data, 'user', uret.user);
            Vue.nextTick(() => {
                // 我本来希望操作一系列完成后才可以保存
                // 避免操作中就触发 watch
                // 可是事与愿违
                this.saveEnable = true;
            })
        }
    },
    beforeRouteEnter: (to, from, next) => {
        /*next(vm => {
            Vue.set(vm, 'visibility', vm.$route.meta.visibility);
        });*/
        Vue.nextTick(() => {
            if (vm) {
                Vue.set(vm, 'visibility', vm.$route.meta.visibility);
            }
        })
        next();
    },
    watch: {
        todos: {
            handler: function (todos) {
                this.doSave();
            },
            deep: true
        }
    },

  // a custom directive to wait for the DOM to be updated
  // before focusing on the input field.
  // https://vuejs.org/guide/custom-directive.html
    directives: {
        'todo-focus': function (el, value) {
            if (value) {
                el.focus()
            }
        }
    }
}

</script>

<style>
    .nav {
        float: right;
    }

    .topic-item {
    }

    .divider-line {
        border-bottom: #EBF2F6 1px solid;
        width: 50%;
    }

    .avatar {
        float: left;
        width: 50px;
        height: 50px;
        min-height: 50px;
        border-bottom-width: 0px !important; /* fix for entry.css */
    }
</style>
