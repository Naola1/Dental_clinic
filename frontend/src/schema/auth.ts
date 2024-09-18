import { z } from "zod";

export const LoginSchema = z.object({
  email: z.string().email({
    message: "Enter valid email address",
  }),
  password: z.string().min(6, {
    message: "Password must be greater that 6 characters",
  }),
});

export const ForgotPasswordSchema = z.object({
  email: z.string().email({
    message: "Enter valid email address",
  }),
});

export const ResetPasswordSchema = z
  .object({
    token: z.string().optional(),
    password: z.string().min(6, {
      message: "Password must be greater that 6 characters",
    }),

    confirmPassword: z.string().min(6, {
      message: "Confirm password must be greater that 6 characters",
    }),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "Password must match",
    path: ["confirmPassword"],
  });

export const RegisterSchema = z
  .object({
    email: z.string({
      required_error: "Email is required",
    }),
    username: z.string({
      required_error: "Username is required",
    }),

    password: z.string().min(6, {
      message: "Password must be greater that 6 characters",
    }),

    confirmPassword: z.string().min(6, {
      message: "Confirm password must be greater that 6 characters",
    }),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "Password must match",
    path: ["confirmPassword"],
  });

const UserSchema = z.object({
  username: z.string().optional(),
  email: z.string().optional(),
  first_name: z.string().optional(),
  middle_name: z.string().optional(),
  last_name: z.string().optional(),
  gender: z.string().optional(),
  date_of_birth: z.string().optional().nullable(),
  phone_number: z.string().optional(),
  address: z.string().optional(),
  emergency_contact_name: z.string().optional(),
  emergency_contact_number: z.string().optional(),
});

export const UpdateProfileSchema = z.object({
  user: UserSchema.optional(),
  medical_history: z.string().optional(),
  allergies: z.string().optional(),
});

export const DocAddRecord = z.object({
  patient: z.coerce.number().optional(),
  treatment: z.coerce.number().optional(),
  treatment_date: z.string().optional(),
  description: z.string().optional(),
});

const DocUserSchema = z.object({
  username: z.string().optional(),
  email: z.string().optional(),
  first_name: z.string().optional(),
  middle_name: z.string().optional(),
  last_name: z.string().optional(),
  gender: z.string().optional(),
  date_of_birth: z.string().optional().nullable(),
  phone_number: z.string().optional(),
  address: z.string().optional(),
  emergency_contact_name: z.string().optional(),
  emergency_contact_number: z.string().optional(),
});

export const DocUpdateProfileSchema = z.object({
  user: DocUserSchema.optional(),
  bio: z.string().optional(),
  specialization: z.string().optional(),
  experience: z.coerce.number().optional(),
  qualification: z.string().optional(),
});
