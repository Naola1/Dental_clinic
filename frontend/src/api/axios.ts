import useAuthStore from "@/hooks/zustand/use-auth-store";
import axios from "axios";

const axiosInstance = axios.create({
  baseURL: "https://dental-clinic-lqrz.onrender.com/api/",
});

axiosInstance.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().token;

    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }

    return config;
  },
  function (error) {
    return Promise.reject(error);
  }
);

export default axiosInstance;
