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

import { Button } from "@/components/ui/button";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import Loading from "../loading/Loading";
import { useDoctorTreatment } from "@/hooks/use-treatment";
import { useSearchRecord } from "@/hooks/use-patient";
import { useDebouncedCallback } from "use-debounce";
import { Input } from "../ui/input";

export type DoctorAvailability = {
  id: number;
  date: string;
  treatment: string;
  description: string;
};

export const columns: ColumnDef<DoctorAvailability>[] = [
  {
    accessorKey: "date",
    header: "Date",
    cell: ({ row }) => <div className="capitalize">{row.getValue("date")}</div>,
  },
  {
    accessorKey: "doctor",
    header: "Patient Name",
    cell: ({ row }) => (
      <div className="capitalize">{row.getValue("doctor")}</div>
    ),
  },
  {
    accessorKey: "treatment",
    header: "Treatment",
    cell: ({ row }) => (
      <div className="capitalize">{row.getValue("treatment")}</div>
    ),
  },
  {
    accessorKey: "description",
    header: "Description",
    cell: ({ row }) => (
      <div className="capitalize">{row.getValue("description")}</div>
    ),
  },
];

export function DoctorTreatmentTable() {
  const [sorting, setSorting] = React.useState<SortingState>([]);
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>(
    []
  );
  const [columnVisibility, setColumnVisibility] =
    React.useState<VisibilityState>({});
  const [rowSelection, setRowSelection] = React.useState({});
  const [searchItem, setSearchItem] = React.useState("");

  const { data: doctors, isPending } = useDoctorTreatment();

  const { data: searchData, isPending: searchPendig } =
    useSearchRecord(searchItem);

  const handleInputChange = useDebouncedCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      console.log("asd");
      const searchTerm = e.target.value;
      setSearchItem(searchTerm);
    },
    700
  );

  const data: DoctorAvailability[] =
    searchData && searchData.length > 0
      ? searchData.map((search) => {
          return {
            id: search.id,
            date: search.treatment_date,
            doctor: search.patient.first_name + " " + search.patient.last_name,
            treatment: search.treatment.name,
            description: search?.description ?? "",
          };
        })
      : doctors?.results.map((doc) => {
          return {
            id: doc.id,
            date: doc.treatment_date,
            doctor: doc.patient.first_name + " " + doc.patient.last_name,
            treatment: doc.treatment.name,
            description: doc.description,
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
      <p className="text-center">
        You don&apos;t have any treatment history yet :)
      </p>
    );
  }

  return (
    <div className="w-full px-6">
      <div className="max-w-sm my-4">
        <Input
          placeholder="Search..."
          type="text"
          defaultValue={searchItem}
          onChange={handleInputChange}
        />
      </div>
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
      <div className="flex items-center justify-end space-x-2 py-4">
        <div className="flex-1 text-sm text-muted-foreground">
          {table.getFilteredSelectedRowModel().rows.length} of{" "}
          {table.getFilteredRowModel().rows.length} row(s) selected.
        </div>
        <div className="space-x-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => table.previousPage()}
            disabled={!table.getCanPreviousPage()}
          >
            Previous
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => table.nextPage()}
            disabled={!table.getCanNextPage()}
          >
            Next
          </Button>
        </div>
      </div>
    </div>
  );
}
