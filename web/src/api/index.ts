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

const getPlans = async () => {
    return api.get('/api/plan').then((res) => res.data.data).catch((err) => []);
}

const getLocations = async () => {
    return api.get('https://api.map.baidu.com/place/v2/search?query=公司$汽车$餐饮$购物$生活$体育$医院$住宿$风景$学校&location=27.256842,110.820747&radius=1000&output=json&ak=key').then((res) => res.data.results).catch((err) => []);
}

export default {
    login,
    loginCheck,
    getStatus,
    getPlans,
    getLocations,
};