import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000',
});

const login = async (phone: string, password: string) => {
    return (await api.post('/api/login', { phone, password })).data;
};

export default {
    login,
};