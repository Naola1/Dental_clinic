import DashboardHeader from "@/components/header/dashboard-header";
import { PatientDashboardDoctors } from "@/components/patient";
import PatientAppointmentDashboard from "@/components/patient/patient-appointment";
import { PatientTreatmentTable } from "@/components/treatment/patient-treatment-table";

const PatientDashboard = () => {
  return (
    <div>
      <DashboardHeader name={""} />

      <div className="mx-8">
        <h1 className="font-bold text-lg ">Upcoming appointment</h1>
        <PatientAppointmentDashboard />
      </div>
      <div>
        <h1 className="font-bold text-lg mx-8">Our Doctors</h1>
        <PatientDashboardDoctors />
      </div>

      <div className="border space-y-6 rounded-md p-6 shadow-sm mx-6">
        <h1>Treatment History </h1>
        <PatientTreatmentTable />
      </div>
    </div>
  );
};

export default PatientDashboard;
