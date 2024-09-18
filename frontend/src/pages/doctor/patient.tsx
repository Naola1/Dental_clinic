import { DoctorTreatmentTable } from "@/components/doctor/doctor-treatment-table";

const DoctorPatient = () => {
  return (
    <div>
      <h1 className="py-4 text-xl font-bold px-6">Patient Record</h1>

      <DoctorTreatmentTable />
    </div>
  );
};

export default DoctorPatient;
