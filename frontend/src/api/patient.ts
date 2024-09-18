import {
  IDoctorAppointmentDashboard,
  IPAppointmentDashboard,
  ISearch,
  ISearchRecord,
} from "../../types/patient";
import axiosInstance from "./axios";

export const getPatientDashboardAppointment =
  async (): Promise<IPAppointmentDashboard> => {
    const response = await axiosInstance.get("/appointments/?page=1");
    return response.data;
  };

export const getDoctorDashboardAppointment = async ({
  page_size,
}: {
  page_size: string;
}): Promise<IDoctorAppointmentDashboard> => {
  const response = await axiosInstance.get(
    `/appointments/?page_size=${page_size}`
  );
  return response.data;
};

export const searchAppointment = async ({
  q,
}: {
  q?: string;
}): Promise<ISearch[]> => {
  const response = await axiosInstance.get(`/appointments/search?query=${q}`);
  return response.data;
};

export const searchRecord = async ({
  q,
}: {
  q?: string;
}): Promise<ISearchRecord[]> => {
  const response = await axiosInstance.get(`/search?query=${q}`);
  return response.data;
};
