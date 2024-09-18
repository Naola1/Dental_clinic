import axiosInstance from "./axios";
import { IDoctorTreatment, IPatientTreatment } from "../../types/treatment";

export const getPatientTreatment = async (): Promise<IPatientTreatment> => {
  const response = await axiosInstance.get("/patient/history/");
  return response.data;
};

export const getDoctorTreatment = async (): Promise<IDoctorTreatment> => {
  const response = await axiosInstance.get("/doctor/history/");
  return response.data;
};
