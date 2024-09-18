import { z } from "zod";

export const BookingSchema = z.object({
  appointment_date: z.coerce.date(),
});
