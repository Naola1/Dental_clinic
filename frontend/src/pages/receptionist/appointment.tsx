import { DoctorAppointmentTable } from "@/components/doctor/doctor-appointment";

const ReceptionistAppointment = () => {
  return (
    <div>
      <h1 className="py-4 text-xl font-bold px-6">Doctor Appointment</h1>

      <DoctorAppointmentTable showSearch={false} />
    </div>
  );
};

export default ReceptionistAppointment;
