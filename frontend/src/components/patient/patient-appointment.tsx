import { usePADashboard } from "@/hooks/use-patient";
import Loading from "../loading/Loading";
import moment from "moment";

const PatientAppointmentDashboard = () => {
  const { data, isLoading } = usePADashboard();

  if (isLoading)
    return (
      <div className="flex justify-center">
        <Loading />
      </div>
    );

  if (data?.count === 0) {
    return (
      <p className="text-center py-4">You don&apos; have any appoinments yet</p>
    );
  }

  const item = data?.results[data?.results.length - 1];

  return (
    <div className="mt-6">
      <div className="flex border p-4 rounded-md gap-10">
        <div>
          <p className="font-bold">Date</p>
          <p>{moment(item?.appointment_date).format("DD/MM/YYYY")}</p>
        </div>

        <div>
          <p className="font-bold">Doctor</p>
          <p>
            {item?.doctor.user.first_name +
              " " +
              item?.doctor.user.first_name || "-"}
          </p>
        </div>
        <div>
          <p className="font-bold">Specialization</p>
          <p>{item?.doctor.specialization}</p>
        </div>

        <div>
          <p className="font-bold">Status</p>
          <p>{item?.status}</p>
        </div>
      </div>
    </div>
  );
};

export default PatientAppointmentDashboard;
