import { IPatientProfile } from "types/profile";
import axiosInstance from "./axios";
import { IProfileUpdate, ITreatmentRes } from "types/auth";
import { z } from "zod";
import {
  DocAddRecord,
  DocUpdateProfileSchema,
  UpdateProfileSchema,
} from "@/schema/auth";
import moment from "moment";

export const getPatientProfile = async (): Promise<IPatientProfile> => {
  const response = await axiosInstance.get("/user/profile/");
  return response.data;
};

export const profileUpdate = async (
  data: z.infer<typeof UpdateProfileSchema>
): Promise<IProfileUpdate> => {
  const response = await axiosInstance.put("/user/profile/", {
    ...data,
    user: {
      ...data.user,
      date_of_birth: moment(data.user?.date_of_birth).format("YYYY-MM-DD"),
    },
  });
  return response.data;
};

export const profileUpdateDoctor = async (
  data: z.infer<typeof DocUpdateProfileSchema>
) => {
  const response = await axiosInstance.put("/user/profile/", data);
  return response.data;
};

export const docAddRecrord = async (data: z.infer<typeof DocAddRecord>) => {
  const response = await axiosInstance.post("/doctor/history/", data);
  return response.data;
};

export const getTreatments = async (): Promise<ITreatmentRes> => {
  const response = await axiosInstance.get("/treatments");
  return response.data;
};
