import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

import { ResetPasswordSchema } from "@/schema/auth";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { useNavigate, useSearchParams } from "react-router-dom";
import { z } from "zod";
import { Form } from "../ui/form";
import { InputForm } from "../input-form/input";
import { useResetPassword } from "@/hooks/use-auth";
import Loading from "../loading/Loading";
import { useEffect, useState } from "react";
import { AlertMessage } from "../alert/Alert";
import { AxiosError } from "axios";

export function ResetPasswordForm() {
  const navigate = useNavigate();
  const [error, setError] = useState(undefined);
  const [searchParams] = useSearchParams();

  const token = searchParams.get("token");

  const form = useForm<z.infer<typeof ResetPasswordSchema>>({
    resolver: zodResolver(ResetPasswordSchema),
    defaultValues: {
      token: token ?? "",
      password: "",
      confirmPassword: "",
    },
  });

  const reset_password = useResetPassword();

  async function onSubmit(data: z.infer<typeof ResetPasswordSchema>) {
    setError(undefined);
    await reset_password.mutateAsync({
      token: data.token ?? "",
      password: data.password,
    });
  }

  useEffect(() => {
    if (reset_password.data?.status === "OK") {
      navigate("/login");
    }
    if (reset_password.isError) {
      if (reset_password.error instanceof AxiosError) {
        setError(reset_password.error.response?.data);
      }
    }
  }, [reset_password.error, reset_password.data]);

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <Card className="w-[350px]">
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)}>
            <CardHeader>
              <CardTitle>Reset your Password</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <InputForm
                control={form.control}
                label={"Password"}
                placeholder={"Enter your new password"}
                name={"password"}
                type="password"
              />

              <InputForm
                control={form.control}
                label={"Confirm password"}
                placeholder={"Confirm password"}
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
                disabled={reset_password.isPending}
                className="flex items-center"
              >
                {reset_password.isPending ? <Loading /> : "Change Password"}
              </Button>
            </div>
          </form>
        </Form>
      </Card>
    </div>
  );
}
