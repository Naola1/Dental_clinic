import { AlertMessage } from "@/components/alert/Alert";
import { InputForm } from "@/components/input-form/input";
import Loading from "@/components/loading/Loading";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Form } from "@/components/ui/form";
import { useUpdateProfile } from "@/hooks/use-auth";
import { usePatientProfile } from "@/hooks/use-profile";
import { UpdateProfileSchema } from "@/schema/auth";
import { zodResolver } from "@hookform/resolvers/zod";
import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { z } from "zod";

const EditProfileReceptionist = () => {
  const { data, isLoading } = usePatientProfile();
  const navigate = useNavigate();

  const [error, setError] = useState(undefined);

  const updateProfile = useUpdateProfile();

  const form = useForm<z.infer<typeof UpdateProfileSchema>>({
    resolver: zodResolver(UpdateProfileSchema),
    defaultValues: {
      user: {
        email: data?.user.email,
        username: data?.user.username,
        first_name: data?.user.first_name,
        middle_name: data?.user.middle_name,
        last_name: data?.user.last_name,
        gender: data?.user.gender,
        date_of_birth: data?.user.date_of_birth,
        phone_number: data?.user.phone_number,
        address: data?.user.address,
        emergency_contact_name: data?.user.emergency_contact_name,
        emergency_contact_number: data?.user.emergency_contact_number,
      },
      medical_history: "",
      allergies: "",
    },
  });

  async function onSubmit(data: z.infer<typeof UpdateProfileSchema>) {
    setError(undefined);
    await updateProfile.mutateAsync(data);
  }

  useEffect(() => {
    if (updateProfile.isSuccess) {
      navigate("/receptionist/profile");
    }
  }, [updateProfile.isSuccess]);

  if (isLoading) {
    return (
      <div className="flex justify-center py6">
        <Loading />
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center justify-center py-10 w-full">
      <Card className="max-w-lg">
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)}>
            <CardContent className="space-y-3 py-4">
              <div className="flex flex-col md:flex-row gap-6">
                <InputForm
                  control={form.control}
                  label={"Username"}
                  placeholder={"Enter your username"}
                  name={"user.username"}
                />

                <InputForm
                  control={form.control}
                  label={"Email"}
                  placeholder={"Enter your email"}
                  name={"user.email"}
                />
              </div>
              <div className="flex flex-col md:flex-row gap-6">
                <InputForm
                  control={form.control}
                  label={"First Name"}
                  placeholder={"Enter your first name"}
                  name={"user.first_name"}
                />
                <InputForm
                  control={form.control}
                  label={"Middle name"}
                  placeholder={"Enter your middle name"}
                  name={"user.middle_name"}
                />
              </div>
              <div className="flex flex-col md:flex-row gap-6">
                <InputForm
                  control={form.control}
                  label={"Last name"}
                  placeholder={"Enter your last name"}
                  name={"user.last_name"}
                />

                <InputForm
                  control={form.control}
                  label={"Gender"}
                  placeholder={"Enter your gender"}
                  name={"user.gender"}
                />
              </div>
              <div className="flex flex-col md:flex-row gap-6">
                <InputForm
                  control={form.control}
                  label={"Date of birth"}
                  placeholder={"Enter your date of birth"}
                  name={"user.date_of_birth"}
                  type="date"
                />
                <InputForm
                  control={form.control}
                  label={"Phone number"}
                  placeholder={"Enter your phone number"}
                  name={"user.phone_number"}
                />
              </div>
              <div className="flex flex-col md:flex-row gap-6">
                <InputForm
                  control={form.control}
                  label={"Address"}
                  placeholder={"Enter your address"}
                  name={"user.address"}
                />

                <InputForm
                  control={form.control}
                  label={"Emergency Contact Name"}
                  placeholder={"Enter your emergency contact name"}
                  name={"user.emergency_contact_name"}
                />
              </div>
              <InputForm
                control={form.control}
                label={"Emerygency Contact Number"}
                placeholder={"Enter your emerygency contact number"}
                name={"user.emergency_contact_number"}
              />
            </CardContent>

            {error && (
              <div className="px-6">
                <AlertMessage
                  message={error ?? ""}
                  variant={"destructive"}
                  header={"Error"}
                />
              </div>
            )}

            <div className="flex flex-col justify-end px-6 py-3">
              <Button
                disabled={updateProfile.isPending}
                className="flex items-center"
              >
                {updateProfile.isPending ? <Loading /> : "Update"}
              </Button>
            </div>
          </form>
        </Form>
      </Card>
    </div>
  );
};

export default EditProfileReceptionist;
