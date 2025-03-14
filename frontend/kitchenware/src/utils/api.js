import axios from 'axios';

const backendURL = 'http://localhost:8000/api/';
const backend_api_version = 'v1';

const apiClient = axios.create({
  baseURL: `${backendURL}${backend_api_version}`
});

export default apiClient;