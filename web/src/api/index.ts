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

const getConfig = async () => {
    return (await api.get('/api/config')).data;
}

const getPlans = async () => {
    return api.get('/api/plan').then((res) => res.data.data).catch((err) => []);
}

const getLocations = async (location: string) => {
    return api.get(`/api/place/search?location=${location}`).then((res) => res.data).catch((err) => []);
}

const saveConfig = async (config: any) => {
    return api.post('/api/config', config).then((res) => res.data).catch((err) => []);
}

export default {
    login,
    loginCheck,
    getConfig,
    getPlans,
    getLocations,
    saveConfig,
};