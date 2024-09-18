import { AlertCircle } from "lucide-react";

import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

interface AlertMessageProps {
  message: string;
  variant: "default" | "destructive" | null | undefined;
  header: string;
}

export function AlertMessage({ message, variant, header }: AlertMessageProps) {
  return (
    <Alert variant={variant}>
      <AlertCircle className="h-4 w-4" />
      <AlertTitle>{header}</AlertTitle>
      <AlertDescription>{message}</AlertDescription>
    </Alert>
  );
}
