import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000',
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

const login = async (phone: string, password: string) => {
    return (await api.post('/api/login', { phone, password })).data;
};

const loginCheck = async () => {
    return api.get('/api/login').then((res) => true).catch((err) => false);
};

const getStatus = async () => {
    return (await api.get('/api/config')).data;
}

export default {
    login,
    loginCheck,
    getStatus,
};