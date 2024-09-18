import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import { LoginSchema } from "@/schema/auth";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { z } from "zod";
import { Form } from "../ui/form";
import { InputForm } from "../input-form/input";
import { useLogin } from "@/hooks/use-auth";
import Loading from "../loading/Loading";
import { useEffect, useState } from "react";
import { AxiosError } from "axios";
import { AlertMessage } from "../alert/Alert";

export function LoginForm() {
  const navigate = useNavigate();
  const [error, setError] = useState(undefined);

  const form = useForm<z.infer<typeof LoginSchema>>({
    resolver: zodResolver(LoginSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const login = useLogin();

  async function onSubmit(data: z.infer<typeof LoginSchema>) {
    setError(undefined);
    await login.mutateAsync(data);
  }

  useEffect(() => {
    if (login.isError && login.error instanceof AxiosError) {
      if (login.error.response?.data?.error) {
        setError(login.error.response?.data?.error);
      }
    }

    if (login.data?.role === "patient") {
      navigate("/patient/dashboard");
    }

    if (login.data?.role === "doctor") {
      navigate("/doctor/dashboard");
    }

    if (login.data?.role === "receptionist") {
      navigate("/receptionist/dashboard");
    }
  }, [login.error, login.data]);

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <Card className="w-[350px]">
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)}>
            <CardHeader>
              <CardTitle>Login into your account</CardTitle>
              <CardDescription>Lily dental clinic</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
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
              <Button disabled={login.isPending} className="flex items-center">
                {login.isPending ? <Loading /> : "Login"}
              </Button>
            </div>

            <div className="flex justify-end items-center px-3 gap-2">
              <Button
                variant="link"
                type="button"
                onClick={() => navigate("/forgot-password")}
              >
                Forget Password?
              </Button>
            </div>

            <div className="flex justify-center items-center my-6 gap-2">
              Don&apos;t you have an account{" "}
              <Button variant="link" onClick={() => navigate("/register")}>
                Register
              </Button>
            </div>
          </form>
        </Form>
      </Card>
    </div>
  );
}
