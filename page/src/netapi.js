
import config from "./config.js"

let API_SERVER = config.remote.API_SERVER;

let info_post = {credentials: 'include', 'method': 'POST'};
let info_get = {credentials: 'include', 'method': 'GET'};

async function do_fetch (url, method, data, fix) {
    return fetch(url, {
        method: method,
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
        credentials: 'include'
    })
}

async function get (url, data, fix) { return do_fetch(url, "GET", data, fix); }
async function post (url, data, fix) { return do_fetch(url, "POST", data, fix); }


export default {
    todoGet: async function () {
        try {
            let resp = await get(`${API_SERVER}/api/get_all`);
            if (!resp.ok) throw "NOT 200";
            let data = await resp.json();
            for (let i of data.data) {
                i.completed = i.state == 80;
            }
            return data;
        } catch(e) {
            console.log("Oops, error", e);
        }
    },

    todoAdd: async function (title, content) {
        try {
            let resp = await post(`${API_SERVER}/api/todo/add`, {title, content});
            if (!resp.ok) throw "NOT 200";
            let data = await resp.json();
            return data;
        } catch(e) {
            console.log("Oops, error", e);
        }
    },

    todoRemove: async function (todo_id) {
        try {
            let resp = await post(`${API_SERVER}/api/todo/remove`, {'todo_id': todo_id});
            if (!resp.ok) throw "NOT 200";
            let data = await resp.json();
            return data;
        } catch(e) {
            console.log("Oops, error", e);
        }
    },

    todoBatchSave: async function (todos) {
        try {
            let todo_lst = JSON.stringify(todos);
            let resp = await post(`${API_SERVER}/api/todo/batch_save`, {todo_lst});
            if (!resp.ok) throw "NOT 200";
            let data = await resp.json();
            return data;
        } catch(e) {
            console.log("Oops, error", e);
        }
    },

    userInfo: async function () {
        try {
            let resp = await post(`${API_SERVER}/api/userinfo`);
            if (!resp.ok) throw "NOT 200";
            let data = await resp.json();
            return data;
        } catch(e) {
            console.log("Oops, error", e);
        }
    },

    userSignup: async function (username, password) {
        try {
            let resp = await post(`${API_SERVER}/api/signup`, {username, password});
            if (!resp.ok) throw "NOT 200";
            let data = await resp.json();
            return data;
        } catch(e) {
            console.log("Oops, error", e);
        }
    },

    userSignin: async function (username, password) {
        try {
            let resp = await post(`${API_SERVER}/api/signin`, {username, password});
            if (!resp.ok) throw "NOT 200";
            let data = await resp.json();
            return data;
        } catch(e) {
            console.log("Oops, error", e);
        }
    },

    userSignout: async function() {
        try {
            let resp = await get(`${API_SERVER}/api/signout`);
            if (!resp.ok) throw "NOT 200";
            let data = await resp.json();
            return data;
        } catch(e) {
            console.log("Oops, error", e);
        }
    },
}
