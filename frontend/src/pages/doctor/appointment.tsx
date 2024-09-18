import { DoctorAppointmentAppointmentTable } from "@/components/doctor/doctor-appointment-appointment";

const DoctorAppointment = () => {
  return (
    <div>
      <h1 className="py-4 text-xl font-bold px-6">Doctor Appointment</h1>

      <DoctorAppointmentAppointmentTable page_size="10" />
    </div>
  );
};

export default DoctorAppointment;
