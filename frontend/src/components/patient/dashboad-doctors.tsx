import { useAllDoctors } from "@/hooks/use-doctor";
import Loading from "../loading/Loading";

export const PatientDashboardDoctors = () => {
  const { data: doctors, isLoading } = useAllDoctors();

  if (isLoading) {
    return (
      <div className="flex justify-center py-6">
        <Loading />
      </div>
    );
  }
  return (
    <div className="mx-6 my-3">
      <div className="grid grid-cols-1 md:grid-cols-2 lg-grid-cols-3 xl:grid-cols-4 gap-4">
        {doctors?.results.map((item) => {
          const name = item.user.first_name + " " + item.user.last_name;
          return (
            <div
              className="border p-3 rounded-md shadow-sm hover:shadow-md transition-all duration-150 cursor-pointer"
              key={item.id}
            >
              <div>
                <p className="font-bold">Name</p>
                <p>{name || "-"}</p>
              </div>
              <div>
                <p className="font-bold">Specialization</p>
                <p>{item.specialization || "-"}</p>
              </div>
              <div>
                <p className="font-bold">Qualification</p>
                <p>{item.qualification || "-"}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
