import * as React from "react";
import {
  ColumnDef,
  ColumnFiltersState,
  SortingState,
  VisibilityState,
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
} from "@tanstack/react-table";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import Loading from "../loading/Loading";
import { useDADashboard, useSearchAppointment } from "@/hooks/use-patient";
import moment from "moment";
import { Input } from "../ui/input";
import { useDebouncedCallback } from "use-debounce";

export type DoctorAvailability = {
  id: number;
  patient: string;
  doctor: string;
  appointment_date: string;
  status: string;
};

export const columns: ColumnDef<DoctorAvailability>[] = [
  {
    accessorKey: "patient",
    header: "Patient",
    cell: ({ row }) => (
      <div className="capitalize">{row.getValue("patient")}</div>
    ),
  },
  {
    accessorKey: "doctor",
    header: "Doctor",
    cell: ({ row }) => (
      <div className="capitalize">{row.getValue("doctor")}</div>
    ),
  },
  {
    accessorKey: "appointment_date",
    header: "Appointment Date",
    cell: ({ row }) => (
      <div className="capitalize">
        {moment(row.getValue("appointment_date")).format("DD/MM/YYYY")}
      </div>
    ),
  },
  {
    accessorKey: "status",
    header: "Status",
    cell: ({ row }) => (
      <div className="capitalize">{row.getValue("status")}</div>
    ),
  },
];

interface DoctorAppointmentTablePops {
  showSearch?: boolean;
}

export function DoctorAppointmentTable({
  showSearch = true,
}: DoctorAppointmentTablePops) {
  const [sorting, setSorting] = React.useState<SortingState>([]);
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>(
    []
  );
  const [columnVisibility, setColumnVisibility] =
    React.useState<VisibilityState>({});
  const [rowSelection, setRowSelection] = React.useState({});
  const [searchItem, setSearchItem] = React.useState("");

  const handleInputChange = useDebouncedCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      console.log("asd");
      const searchTerm = e.target.value;
      setSearchItem(searchTerm);
    },
    700
  );

  const { data: doctors, isPending } = useDADashboard("10");

  const { data: searchData, isPending: searchPendig } =
    useSearchAppointment(searchItem);

  const data: DoctorAvailability[] =
    searchData && searchData.length > 0
      ? searchData?.map((search) => {
          return {
            id: search.id,
            patient:
              search.patient.user.first_name +
              " " +
              search.patient.user.last_name,
            appointment_date: search.appointment_date,
            status: search.status,
            doctor:
              search.doctor.user.first_name +
              " " +
              search.doctor.user.last_name,
          };
        })
      : doctors?.results.map((doc) => {
          return {
            id: doc.id,
            patient:
              doc.patient.user.first_name + " " + doc.patient.user.last_name,
            appointment_date: doc.appointment_date,
            status: doc.status,
            doctor:
              doc.doctor.user.first_name + " " + doc.doctor.user.last_name,
          };
        }) ?? [];

  const table = useReactTable({
    data,
    columns,
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    onColumnVisibilityChange: setColumnVisibility,
    onRowSelectionChange: setRowSelection,
    state: {
      sorting,
      columnFilters,
      columnVisibility,
      rowSelection,
    },
  });

  if (isPending) {
    return (
      <div className="flex items-center py-10 justify-center">
        <Loading />
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <p className="text-center">You don&apos;t have any appointments yet :)</p>
    );
  }

  return (
    <div className="w-full px-6">
      {showSearch && (
        <div className="max-w-sm my-4">
          <Input
            placeholder="Search..."
            type="text"
            defaultValue={searchItem}
            onChange={handleInputChange}
          />
        </div>
      )}

      {searchPendig ? (
        <div className="flex items-center py-10 justify-center">
          <Loading />
        </div>
      ) : (
        <div className="rounded-md border">
          <Table>
            <TableHeader>
              {table.getHeaderGroups().map((headerGroup) => (
                <TableRow key={headerGroup.id}>
                  {headerGroup.headers.map((header) => {
                    return (
                      <TableHead key={header.id}>
                        {header.isPlaceholder
                          ? null
                          : flexRender(
                              header.column.columnDef.header,
                              header.getContext()
                            )}
                      </TableHead>
                    );
                  })}
                </TableRow>
              ))}
            </TableHeader>
            <TableBody>
              {table.getRowModel().rows?.length ? (
                table.getRowModel().rows.map((row) => (
                  <TableRow
                    key={row.id}
                    data-state={row.getIsSelected() && "selected"}
                  >
                    {row.getVisibleCells().map((cell) => (
                      <TableCell key={cell.id}>
                        {flexRender(
                          cell.column.columnDef.cell,
                          cell.getContext()
                        )}
                      </TableCell>
                    ))}
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell
                    colSpan={columns.length}
                    className="h-24 text-center"
                  >
                    No results.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </div>
      )}
    </div>
  );
}
