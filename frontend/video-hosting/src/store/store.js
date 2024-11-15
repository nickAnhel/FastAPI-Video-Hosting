import { makeAutoObservable, set } from "mobx";
import axios from "axios";

import { APIUrl } from "../http";
import AuthService from "../service/AuthService";
import UserService from "../service/UserService";


export default class Store {
    user = {}
    isAuthenticated = false
    isLoading = false

    constructor() {
        makeAutoObservable(this);
    }

    setAuthenticated(value) {
        this.isAuthenticated = value
    }

    setUser(user) {
        this.user = user
    }

    setLoading(value) {
        this.isLoading = value
    }

    async register(data) {
        // try {
        const response = await AuthService.register(data);
        this.setUser(response.data);
        await this.login(data.username, data.password);
        // } catch (e) {
        //     console.log(e.response?.data?.detail)
        // }
    }

    async login(username, password) {
        // try {
        const response = await AuthService.login(username, password);
        localStorage.setItem('token', response.data.access_token);
        this.setAuthenticated(true);

        const userRes = await UserService.getMe();
        let userData = userRes.data;
        delete userData.subscribers;
        delete userData.subscribed;
        this.setUser(userData);
        // } catch (e) {
        //     console.log(e.response?.data?.detail)
        // }
    }

    async logout() {
        try {
            await AuthService.logout();
            localStorage.removeItem('token');
            this.setAuthenticated(false);
            this.setUser({});
        } catch (e) {
            console.log(e.response?.data?.detail)
        }
    }

    async checkAuth() {
        this.setLoading(true);
        try {
            const response = await axios.post(`${APIUrl}/auth/refresh`);
            localStorage.setItem('token', response.data.access_token);
            this.setAuthenticated(true);

            const userRes = await UserService.getMe();
            let userData = userRes.data;
            delete userData.subscribers;
            delete userData.subscribed;
            this.setUser(userData);
        } catch (e) {
            console.log(e.response?.data?.detail);

            localStorage.removeItem('token');
            this.setAuthenticated(false);
            this.setUser({});
        } finally {
            this.setLoading(false);
        }
    }
}