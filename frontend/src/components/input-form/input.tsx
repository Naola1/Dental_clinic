import {
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Control, FieldValues, Path } from "react-hook-form";

interface InputFormProps<TFormValues extends FieldValues> {
  control: Control<TFormValues> | undefined;
  label: string;
  placeholder: string;
  name: Path<TFormValues>;
  type?: React.HTMLInputTypeAttribute | undefined;
}

export const InputForm = <TFormValues extends FieldValues>({
  control,
  label,
  placeholder,
  name,
  type,
}: InputFormProps<TFormValues>) => {
  return (
    <FormField
      control={control}
      name={name}
      render={({ field }) => (
        <FormItem>
          <FormLabel htmlFor={name}>{label}</FormLabel>
          <FormControl>
            <Input placeholder={placeholder} {...field} type={type} />
          </FormControl>
          <FormMessage />
        </FormItem>
      )}
    />
  );
};
