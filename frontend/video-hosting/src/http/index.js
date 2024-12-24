import axios from "axios";


export const APIUrl = "http://localhost:8000";

axios.defaults.withCredentials = true;
const api = axios.create({
    withCredentials: true,
    baseURL: APIUrl,
});


api.interceptors.request.use((config) => {
    config.headers.Authorization = `Bearer ${localStorage.getItem("token")}`;
    return config;
});


api.interceptors.response.use(
    (config) => {
        return config;
    },
    async (error) => {
        const originalRequest = error.config;
        if (error?.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            try {
                const response = await axios.post(`${APIUrl}/auth/refresh`);
                localStorage.setItem('token', response.data.access_token);
                return api.request(originalRequest);
            } catch (error) {
                console.log(error);
            }
        }
        throw error;
    }
);


export default api;