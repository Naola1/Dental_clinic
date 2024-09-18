interface DashboardHeaderProps {
  name: string;
  showWelcome?: boolean;
}

const DashboardHeader = ({
  name,
  showWelcome = true,
}: DashboardHeaderProps) => {
  return (
    <div className="flex items-center justify-center  w-full mx-6 my-6 border rounded-md p-4">
      <p className="text-2xl font-light">
        {showWelcome && "Welocome,"}
        <strong> {name}</strong>
      </p>
    </div>
  );
};

export default DashboardHeader;
