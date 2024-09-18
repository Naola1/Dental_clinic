import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useChangeStatus } from "@/hooks/use-doctor";

interface SelectStatusProps {
  placeholder: string;
  appointmentId: number;
}

export function SelectStatus({
  placeholder,
  appointmentId,
}: SelectStatusProps) {
  const status_mutate = useChangeStatus();
  return (
    <Select
      onValueChange={(val) => {
        status_mutate.mutateAsync({
          id: appointmentId,
          data: { status: val },
        });
      }}
    >
      <SelectTrigger className="max-w-[280px]">
        <SelectValue placeholder={placeholder} />
      </SelectTrigger>
      <SelectContent>
        <SelectGroup>
          <SelectLabel>Status</SelectLabel>
          <SelectItem value="Scheduled">Scheduled</SelectItem>
          <SelectItem value="Completed">Completed</SelectItem>
          <SelectItem value="Canceled">Canceled</SelectItem>
        </SelectGroup>
      </SelectContent>
    </Select>
  );
}
