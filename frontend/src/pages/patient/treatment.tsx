import DashboardHeader from "@/components/header/dashboard-header";
import { PatientTreatmentTable } from "@/components/treatment/patient-treatment-table";

const PatientTreatment = () => {
  return (
    <div>
      <DashboardHeader name={"Treatment"} showWelcome={false} />
      <PatientTreatmentTable />
    </div>
  );
};

export default PatientTreatment;
