import { DoctorAppointmentTable } from "@/components/doctor/doctor-appointment";
import { DoctorTreatmentTable } from "@/components/doctor/doctor-treatment-table";
import DashboardHeader from "@/components/header/dashboard-header";

const DoctorDashboard = () => {
  return (
    <div>
      <DashboardHeader name={""} />
      <h1 className="py-4 text-xl font-bold px-6">Your Appointment</h1>

      <DoctorAppointmentTable showSearch={false} />

      <h1 className="py-4 text-xl font-bold px-6">Recent Patient Record</h1>
      <DoctorTreatmentTable />
    </div>
  );
};

export default DoctorDashboard;
