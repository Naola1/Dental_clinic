import { DoctorsAvailablityTable } from "@/components/doctor";
import DashboardHeader from "@/components/header/dashboard-header";

const DoctorsAvailablity = () => {
  return (
    <div>
      <DashboardHeader name={"Doctors Availability"} showWelcome={false} />
      <DoctorsAvailablityTable />
    </div>
  );
};

export default DoctorsAvailablity;
