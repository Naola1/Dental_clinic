import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { RegisterSchema } from "@/schema/auth";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { z } from "zod";
import { Form } from "../ui/form";
import { InputForm } from "../input-form/input";
import Loading from "../loading/Loading";
import { useRegister } from "@/hooks/use-auth";
import { useEffect, useState } from "react";
import { AlertMessage } from "../alert/Alert";
import { AxiosError } from "axios";

export function RegisterForm() {
  const navigate = useNavigate();

  const [error, setError] = useState(undefined);

  const register = useRegister();

  const form = useForm<z.infer<typeof RegisterSchema>>({
    resolver: zodResolver(RegisterSchema),
    defaultValues: {
      email: "",
      username: "",
      password: "",
      confirmPassword: "",
    },
  });

  async function onSubmit(data: z.infer<typeof RegisterSchema>) {
    setError(undefined);
    await register.mutateAsync(data);
  }

  useEffect(() => {
    if (register.isError && register.error instanceof AxiosError) {
      if (register.error.response?.data?.email) {
        setError(register.error.response?.data?.email);
      }
      if (register.error.response?.data?.username) {
        setError(register.error.response?.data?.username);
      }
    }

    if (register.isSuccess) {
      navigate("/login");
    }
  }, [register.error, register.data]);

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <Card className="w-[350px]">
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)}>
            <CardHeader>
              <CardTitle>Register a new account</CardTitle>
              <CardDescription>Lily dental clinic</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <InputForm
                control={form.control}
                label={"username"}
                placeholder={"Enter your username"}
                name={"username"}
              />

              <InputForm
                control={form.control}
                label={"Email"}
                placeholder={"Enter your email"}
                name={"email"}
              />

              <InputForm
                control={form.control}
                label={"Password"}
                placeholder={"Enter your password"}
                name={"password"}
                type="password"
              />

              <InputForm
                control={form.control}
                label={"Confirm password"}
                placeholder={"Enter your confirm password"}
                name={"confirmPassword"}
                type="password"
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
                disabled={register.isPending}
                className="flex items-center"
              >
                {register.isPending ? <Loading /> : "Register"}
              </Button>
            </div>

            <div className="flex justify-center items-center my-6 gap-2">
              Already have an account{" "}
              <Button variant="link" onClick={() => navigate("/login")}>
                Login
              </Button>
            </div>
          </form>
        </Form>
      </Card>
    </div>
  );
}
