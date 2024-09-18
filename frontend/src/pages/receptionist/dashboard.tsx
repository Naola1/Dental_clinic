import { DoctorAppointmentTable } from "@/components/doctor/doctor-appointment";

const ReceptionistDashboard = () => {
  return (
    <div>
      <h1 className="py-4 text-xl font-bold px-6">Appointments</h1>

      <DoctorAppointmentTable />
    </div>
  );
};

export default ReceptionistDashboard;
