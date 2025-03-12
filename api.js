import axios from "axios"

const api = axios.create({
  baseURL: "http://your-backend-url/api", // Replace with your actual backend URL
  timeout: 5000,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
})

export default api

