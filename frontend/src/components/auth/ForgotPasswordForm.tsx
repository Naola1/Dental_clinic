import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

import { ForgotPasswordSchema } from "@/schema/auth";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { z } from "zod";
import { Form } from "../ui/form";
import { InputForm } from "../input-form/input";
import { useForgotPassword } from "@/hooks/use-auth";
import Loading from "../loading/Loading";
import { useEffect, useState } from "react";
import { AlertMessage } from "../alert/Alert";

export function ForgotPasswordForm() {
  const navigate = useNavigate();
  const [error, setError] = useState(undefined);

  const form = useForm<z.infer<typeof ForgotPasswordSchema>>({
    resolver: zodResolver(ForgotPasswordSchema),
    defaultValues: {
      email: "",
    },
  });

  const forgot_password = useForgotPassword();

  async function onSubmit(data: z.infer<typeof ForgotPasswordSchema>) {
    setError(undefined);
    await forgot_password.mutateAsync(data);
  }

  useEffect(() => {
    if (forgot_password.data?.status === "OK") {
      navigate("/login");
    }
  }, [forgot_password.error, forgot_password.data]);

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <Card className="w-[350px]">
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)}>
            <CardHeader>
              <CardTitle>Forget Password</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <InputForm
                control={form.control}
                label={"Email"}
                placeholder={"Enter your email"}
                name={"email"}
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
                disabled={forgot_password.isPending}
                className="flex items-center"
              >
                {forgot_password.isPending ? <Loading /> : "Forget Password"}
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
