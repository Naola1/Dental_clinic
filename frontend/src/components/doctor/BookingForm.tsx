import { Button } from "@/components/ui/button";

import { BookingSchema } from "@/schema/doctors";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Form } from "../ui/form";
import { InputForm } from "../input-form/input";
import Loading from "../loading/Loading";
import { useEffect, useState } from "react";
import { AlertMessage } from "../alert/Alert";
import { useBooking, usePDA } from "@/hooks/use-doctor";
import moment from "moment";
import { toast } from "@/hooks/use-toast";
import { AxiosError } from "axios";
import { useNavigate } from "react-router-dom";

interface BookingFormSchema {
  id: number;
  doctorName: string;
}

export function BookingForm({ id, doctorName }: BookingFormSchema) {
  const [error, setError] = useState<string | undefined>(undefined);
  const navigate = useNavigate();

  const form = useForm<z.infer<typeof BookingSchema>>({
    resolver: zodResolver(BookingSchema),
    defaultValues: {
      appointment_date: new Date(Date.now()),
    },
  });

  const { data, isLoading } = usePDA(id);
  const book = useBooking();

  async function onSubmit(data: z.infer<typeof BookingSchema>) {
    setError(undefined);
    await book.mutateAsync({
      id: id,
      data: {
        appointment_date: moment(data.appointment_date)
          .add(1, "days")
          .format("DD-MM-YYYY"),
      },
    });
  }

  useEffect(() => {
    if (book.isError) {
      if (book.error instanceof AxiosError)
        setError(book.error.response?.data?.detail);
    }

    if (book.isSuccess) {
      toast({
        title: "Appointment successfully booked",
      });
      navigate(0);
    }
  }, [book.error, book.isSuccess]);

  if (isLoading) {
    return (
      <div className="flex justify-center p-4">
        <Loading />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="space-y-3">
        <p>Dr. {doctorName} availablity day&apos;s.</p>
        <div className="flex flex-wrap gap-3">
          {data?.map((item) => {
            return (
              <div key={item.id} className="border rounded-md p-2">
                {item.day_of_week}
              </div>
            );
          })}
        </div>
      </div>

      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
          <InputForm
            control={form.control}
            label={"Date"}
            placeholder={"Date"}
            name={"appointment_date"}
            type="date"
          />

          {error && (
            <AlertMessage
              message={error ?? ""}
              variant="destructive"
              header={"Error"}
            />
          )}

          <Button disabled={book.isPending}>
            {book.isPending ? <Loading /> : "Submit"}
          </Button>
        </form>
      </Form>
    </div>
  );
}
