import Loading from "@/components/loading/Loading";
import { Button } from "@/components/ui/button";
import { usePatientProfile } from "@/hooks/use-profile";
import { useNavigate } from "react-router-dom";

const PatientProfile = () => {
  const { data, isLoading } = usePatientProfile();
  const navigate = useNavigate();

  if (isLoading) {
    return (
      <div className="flex items-center h-screen justify-center">
        <Loading />
      </div>
    );
  }

  return (
    <div className="flex justify-center my-10">
      <div>
        <p className="mb-6 text-2xl font-bold">Profile</p>

        <div className="grid grid-cols-2 border p-4 rounded-md shadow-md">
          <div className="space-y-10">
            <Title
              title={"Fist name"}
              subTitle={data?.user.first_name || "-"}
            />
            <Title title={"Last name"} subTitle={data?.user.last_name || "-"} />
            <Title title={"Username"} subTitle={data?.user.username || "-"} />
            <Title title={"Email"} subTitle={data?.user.email || "-"} />
            <Title
              title={"Phone number"}
              subTitle={data?.user.phone_number || "-"}
            />
            <Title title={"Address"} subTitle={data?.user.address || "-"} />
          </div>
          <div className="space-y-10">
            <Title title={"Gender"} subTitle={data?.user.gender || "-"} />
            <Title
              title={"Date of Birth"}
              subTitle={data?.user.date_of_birth || "-"}
            />
            <Title
              title={"Emergency contact name"}
              subTitle={data?.user.emergency_contact_name || "-"}
            />
            <Title
              title={"Emergency contact phone number"}
              subTitle={data?.user.emergency_contact_number || "-"}
            />
            <Title
              title={"Medical History"}
              subTitle={data?.medical_history || "-"}
            />
            <Title title={"Allergies"} subTitle={data?.allergies || "-"} />
          </div>
        </div>

        <Button
          className="mt-6"
          onClick={() => navigate("/patient/edit-profile")}
        >
          Edit profile
        </Button>
      </div>
    </div>
  );
};

export default PatientProfile;

interface TitleProps {
  title: string;
  subTitle?: string;
}

const Title = ({ title, subTitle = "-" }: TitleProps) => {
  return (
    <div>
      <h1 className="font-bold text-lg">{title}</h1>
      <h4 className="font-light">{subTitle || "-"}</h4>
    </div>
  );
};
