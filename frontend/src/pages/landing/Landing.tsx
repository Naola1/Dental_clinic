import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Mail, Calendar, User, Icon, Folder } from "lucide-react";
import Logo from "../../assets/logo.png";
import Smile from "../../assets/smile.jpg";
import { useNavigate } from "react-router-dom";
import { ReactNode } from "react";

import RegistrationImage from "../../assets/registration.png";
import AvailabilityImage from "../../assets/availability.png";
import TreatmentImage from "../../assets/Treatment.png";
import DoctorsImage from "../../assets/doctors.png";
import Photo from "../../assets/photo1.png";

const LandingPage = () => {
  const navigate = useNavigate();
  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-b from-gray-900 via-blue-900 to-purple-900 text-white">
      <section className="w-full min-h-screen relative overflow-hidden">
        <div className="absolute inset-0 bg-[url('/grid.svg')] bg-center [mask-image:linear-gradient(180deg,white,rgba(255,255,255,0))]"></div>
        <header className="relative z-10 px-4 lg:px-6 h-20 flex items-center">
          <a className="flex items-center justify-center" href="#">
            <img
              src={Logo}
              height={180}
              width={180}
              alt="Dental Clinic Logo"
              className="object-cover"
            />
            <span className="sr-only">Dental Clinic</span>
          </a>
          <nav className="ml-auto flex gap-4 sm:gap-6">
            <button
              className="text-sm font-medium hover:text-blue-400 transition-colors hidden md:flex"
              onClick={() => navigate("/login")}
            >
              Login / Signup
            </button>
            <a
              className="text-sm font-medium hover:text-blue-400 transition-colors"
              href="#features"
            >
              Features
            </a>
            <a
              className="text-sm font-medium hover:text-blue-400 transition-colors"
              href="#about"
            >
              About
            </a>
            <a
              className="text-sm font-medium hover:text-blue-400 transition-colors"
              href="#contact"
            >
              Contact
            </a>
          </nav>
        </header>
        <div className="relative z-10 flex items-center justify-center min-h-[calc(100vh-5rem)]">
          <div className="flex flex-col items-center space-y-4 text-center px-4">
            <div className="space-y-2">
              <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl lg:text-7xl/none py-3 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-600">
                Dental Clinic Management System
              </h1>
              <p className="mx-auto max-w-[700px] text-blue-200 md:text-xl">
                Effortless Management for Exceptional Dental Clinics.
              </p>
            </div>
            <div className="space-x-4">
              <Button
                onClick={() => navigate("/login")}
                className="py-6 px-8 bg-blue-600 hover:bg-blue-700 text-white rounded-full text-lg font-semibold transition-all duration-300 ease-in-out transform hover:scale-105"
              >
                Login/ Sign Up
              </Button>
            </div>
          </div>
        </div>
      </section>

      <main className="flex-1 w-full">
        <section
          id="features"
          className="w-full py-20 md:py-32 lg:py-48 bg-gray-900"
        >
          <div className="container mx-auto px-4">
            <h2 className="text-4xl font-bold tracking-tighter sm:text-5xl text-center mb-16 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-600">
              Web App Features
            </h2>
            <div className="space-y-24">
              <FeatureCard
                icon={<User />}
                title="Secure User Accounts with JWT Authentication"
                description="Streamline patient management with easy account creation and secure JWT authentication. Protect patient information while enabling seamless access 
                to appointments and treatment history. Elevate your clinic's service today!"
                imageUrl={RegistrationImage}
                isReversed={false}
              />
              <FeatureCard
                icon={<Calendar />}
                title="Streamlined Appointment Management"
                description="Optimize your clinic's operations with our easy-to-use system. Allow patients to view doctor availability and book appointments online, reducing 
                administrative tasks and minimizing no-shows. Enhance patient care with a seamless booking experience!"
                imageUrl={AvailabilityImage}
                isReversed={true}
              />
              <FeatureCard
                icon={<Folder />}
                title="Comprehensive Treatment History Access"
                description="Empower patients with easy access to their treatment history, ensuring transparency and better understanding of their care. Doctors can also view 
                and update their patients' treatment records, facilitating informed decision-making and personalized care. Enhance collaboration and continuity of care in your clinic!"
                imageUrl={TreatmentImage}
                isReversed={false}
              />
              <FeatureCard
                icon={<User />}
                title="Doctor Profiles"
                description="Patients can view all clinic doctors, including their qualifications, specializations, and experience. 
                This transparency helps patients make informed choices for their care."
                imageUrl={DoctorsImage}
                isReversed={true}
              />
            </div>
          </div>
        </section>

        <section
          id="about"
          className="w-full py-20 md:py-32 lg:py-48 bg-gray-800"
        >
          <div className="container mx-auto px-4">
            <div className="grid items-center gap-12 lg:grid-cols-2 lg:gap-24">
              <div className="relative">
                <div className="absolute inset-0 bg-blue-500 rounded-full blur-3xl opacity-20"></div>
                <img
                  alt="Futuristic dental care"
                  className="relative rounded-2xl shadow-2xl"
                  src={Smile}
                />
              </div>
              <div className="flex flex-col justify-center space-y-6">
                <h2 className="text-4xl font-bold tracking-tighter sm:text-5xl bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-600">
                  Inspiration Behind the Project
                </h2>
                <p className="text-blue-100 md:text-lg/relaxed lg:text-xl/relaxed xl:text-2xl/relaxed">
                  The Dental clinic Management System was born from the need to
                  improve the efficiency of dental clinic operations. Scheduling
                  appointments, managing patient records, and tracking doctors'
                  availability are essential for providing a high-quality
                  patient experience. This system helps dental clinics automate
                  these processes and offers a simple, user-friendly interface
                  for both patients and staff. This project is also a portfolio
                  piece for Holberton School, where I applied my full-stack
                  development skills to create a real-world solution for
                  clinics.
                </p>
              </div>
            </div>
          </div>
        </section>

        <section
          id="contact"
          className="w-full py-20 md:py-32 lg:py-48 bg-gray-900"
        >
          <div className="container mx-auto px-4">
            <h2 className="text-4xl font-bold tracking-tighter sm:text-5xl text-center mb-16 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-600">
              Connect with the Developer
            </h2>
            <div className="max-w-2xl mx-auto">
              <Card className="overflow-hidden bg-gray-800 border-gray-700">
                <CardContent className="p-6">
                  <div className="flex flex-col items-center text-center">
                    <img
                      src={Photo}
                      height={180}
                      width={180}
                      alt="Naol Mitiku"
                      className="rounded-full w-32 h-32 object-cover mb-4 border-4 border-blue-500"
                    />
                    <h3 className="text-2xl font-bold mb-2 text-blue-400">
                      Naol Mitiku
                    </h3>
                    <p className="text-purple-300 mb-4">
                      Visionary Full Stack Developer
                    </p>
                    <p className="text-blue-100 mb-6">
                      Passionate about pushing the boundaries of dental
                      technology. Let's collaborate on shaping the future of
                      healthcare!
                    </p>
                    <div className="flex flex-wrap justify-center gap-4">
                      <SocialLink
                        href="https://www.linkedin.com/in/naol-mitiku-0a48a423b"
                        icon={<Linkedin className="h-5 w-5" />}
                        label="LinkedIn"
                        color="bg-blue-600"
                      />
                      <SocialLink
                        href="https://github.com/Naola1"
                        icon={<Github className="h-5 w-5" />}
                        label="GitHub"
                        color="bg-gray-700"
                      />
                      <SocialLink
                        href="mailto:naolmitiku@example.com"
                        icon={<Mail className="h-5 w-5" />}
                        label="Email"
                        color="bg-red-600"
                      />
                    </div>
                  </div>
                </CardContent>
              </Card>
              <div className="mt-12 space-y-4">
                <h4 className="text-2xl font-semibold text-center text-blue-400">
                  Project Repositories
                </h4>
                <div className="flex flex-col sm:flex-row justify-center gap-4">
                  <a
                    href="https://github.com/Naola1/dental_clinic_frontend"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center justify-center gap-2 bg-gray-800 hover:bg-gray-700 text-blue-400 px-6 py-3 rounded-full transition-colors"
                    aria-label="Front-end source code on GitHub"
                  >
                    <Github className="h-5 w-5" />
                    <span>Front-end Source</span>
                  </a>
                  <a
                    href="https://github.com/Naola1/dental_clinic-backend"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center justify-center gap-2 bg-gray-800 hover:bg-gray-700 text-blue-400 px-6 py-3 rounded-full transition-colors"
                    aria-label="Back-end source code on GitHub"
                  >
                    <Github className="h-5 w-5" />
                    <span>Back-end Source</span>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
      <footer className="bg-gray-900 border-t border-gray-800">
        <div className="container mx-auto px-4 py-8">
          <div className="flex flex-col sm:flex-row justify-between items-center">
            <p className="text-sm text-gray-400">
              © 2024 Dental Clinic Management.
            </p>
            <nav className="flex gap-4 sm:gap-6 mt-4 sm:mt-0">
              <a
                className="text-sm text-gray-400 hover:text-blue-400 transition-colors"
                href="#"
              >
                Terms of Service
              </a>
              <a
                className="text-sm text-gray-400 hover:text-blue-400 transition-colors"
                href="#"
              >
                Privacy Policy
              </a>
            </nav>
          </div>
        </div>
      </footer>
    </div>
  );
};

interface FeaturesCardProps {
  icon?: ReactNode;
  title: string;
  description: string;
  imageUrl: string;
  isReversed: boolean;
}
const FeatureCard = ({
  icon,
  title,
  description,
  imageUrl,
  isReversed,
}: FeaturesCardProps) => (
  <div
    className={`flex flex-col ${
      isReversed ? "md:flex-row-reverse" : "md:flex-row"
    } items-center gap-8`}
  >
    <div className="md:w-1/2">
      <div className="relative mx-auto w-full max-w-[300px]">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-600 rounded-[48px] blur-lg opacity-75"></div>
        <div className="relative bg-black rounded-[48px] overflow-hidden shadow-xl">
          <div className="absolute top-0 left-1/2 transform -translate-x-1/2 h-6 w-40 bg-black rounded-b-3xl z-10"></div>
          <div className="pt-2 px-4 pb-10">
            <div className="relative bg-gray-800 rounded-[40px] overflow-hidden">
              <img src={imageUrl} alt={title} className="w-full h-auto" />
            </div>
          </div>
          <div className="absolute bottom-2 left-1/2 transform -translate-x-1/2 w-32 h-1 bg-gray-800 rounded-full"></div>
        </div>
      </div>
    </div>
    <div className="md:w-1/2 space-y-4">
      <div className="flex items-center gap-4">
        {icon}
        <h3 className="text-2xl font-semibold text-blue-300">{title}</h3>
      </div>
      <p className="text-blue-100 text-lg">{description}</p>
    </div>
  </div>
);

interface SocialLinkProps {
  href: string;
  icon: ReactNode;
  label: string;
  color: string;
}
const SocialLink = ({ href, icon, label, color }: SocialLinkProps) => (
  <a
    href={href}
    className={`flex items-center gap-2 ${color} hover:opacity-90 text-white px-4 py-2 rounde
d-full transition-all duration-300 ease-in-out transform hover:scale-105`}
    target="_blank"
    rel="noopener noreferrer"
    aria-label={`${label} profile`}
  >
    {icon ?? <Icon className="h-5 w-5" iconNode={[]} />}
    <span>{label}</span>
  </a>
);

export default LandingPage;

function Github(props: any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      x="0px"
      y="0px"
      width="100"
      height="100"
      viewBox="0 0 50 50"
    >
      <path d="M17.791,46.836C18.502,46.53,19,45.823,19,45v-5.4c0-0.197,0.016-0.402,0.041-0.61C19.027,38.994,19.014,38.997,19,39 c0,0-3,0-3.6,0c-1.5,0-2.8-0.6-3.4-1.8c-0.7-1.3-1-3.5-2.8-4.7C8.9,32.3,9.1,32,9.7,32c0.6,0.1,1.9,0.9,2.7,2c0.9,1.1,1.8,2,3.4,2 c2.487,0,3.82-0.125,4.622-0.555C21.356,34.056,22.649,33,24,33v-0.025c-5.668-0.182-9.289-2.066-10.975-4.975 c-3.665,0.042-6.856,0.405-8.677,0.707c-0.058-0.327-0.108-0.656-0.151-0.987c1.797-0.296,4.843-0.647,8.345-0.714 c-0.112-0.276-0.209-0.559-0.291-0.849c-3.511-0.178-6.541-0.039-8.187,0.097c-0.02-0.332-0.047-0.663-0.051-0.999 c1.649-0.135,4.597-0.27,8.018-0.111c-0.079-0.5-0.13-1.011-0.13-1.543c0-1.7,0.6-3.5,1.7-5c-0.5-1.7-1.2-5.3,0.2-6.6 c2.7,0,4.6,1.3,5.5,2.1C21,13.4,22.9,13,25,13s4,0.4,5.6,1.1c0.9-0.8,2.8-2.1,5.5-2.1c1.5,1.4,0.7,5,0.2,6.6c1.1,1.5,1.7,3.2,1.6,5 c0,0.484-0.045,0.951-0.11,1.409c3.499-0.172,6.527-0.034,8.204,0.102c-0.002,0.337-0.033,0.666-0.051,0.999 c-1.671-0.138-4.775-0.28-8.359-0.089c-0.089,0.336-0.197,0.663-0.325,0.98c3.546,0.046,6.665,0.389,8.548,0.689 c-0.043,0.332-0.093,0.661-0.151,0.987c-1.912-0.306-5.171-0.664-8.879-0.682C35.112,30.873,31.557,32.75,26,32.969V33 c2.6,0,5,3.9,5,6.6V45c0,0.823,0.498,1.53,1.209,1.836C41.37,43.804,48,35.164,48,25C48,12.318,37.683,2,25,2S2,12.318,2,25 C2,35.164,8.63,43.804,17.791,46.836z"></path>
    </svg>
  );
}

function Linkedin(props: any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      x="0px"
      y="0px"
      width="100"
      height="100"
      viewBox="0 0 48 48"
    >
      <path
        fill="#0078d4"
        d="M42,37c0,2.762-2.238,5-5,5H11c-2.761,0-5-2.238-5-5V11c0-2.762,2.239-5,5-5h26c2.762,0,5,2.238,5,5	V37z"
      ></path>
      <path
        d="M30,37V26.901c0-1.689-0.819-2.698-2.192-2.698c-0.815,0-1.414,0.459-1.779,1.364	c-0.017,0.064-0.041,0.325-0.031,1.114L26,37h-7V18h7v1.061C27.022,18.356,28.275,18,29.738,18c4.547,0,7.261,3.093,7.261,8.274	L37,37H30z M11,37V18h3.457C12.454,18,11,16.528,11,14.499C11,12.472,12.478,11,14.514,11c2.012,0,3.445,1.431,3.486,3.479	C18,16.523,16.521,18,14.485,18H18v19H11z"
        opacity=".05"
      ></path>
      <path
        d="M30.5,36.5v-9.599c0-1.973-1.031-3.198-2.692-3.198c-1.295,0-1.935,0.912-2.243,1.677	c-0.082,0.199-0.071,0.989-0.067,1.326L25.5,36.5h-6v-18h6v1.638c0.795-0.823,2.075-1.638,4.238-1.638	c4.233,0,6.761,2.906,6.761,7.774L36.5,36.5H30.5z M11.5,36.5v-18h6v18H11.5z M14.457,17.5c-1.713,0-2.957-1.262-2.957-3.001	c0-1.738,1.268-2.999,3.014-2.999c1.724,0,2.951,1.229,2.986,2.989c0,1.749-1.268,3.011-3.015,3.011H14.457z"
        opacity=".07"
      ></path>
      <path
        fill="#fff"
        d="M12,19h5v17h-5V19z M14.485,17h-0.028C12.965,17,12,15.888,12,14.499C12,13.08,12.995,12,14.514,12	c1.521,0,2.458,1.08,2.486,2.499C17,15.887,16.035,17,14.485,17z M36,36h-5v-9.099c0-2.198-1.225-3.698-3.192-3.698	c-1.501,0-2.313,1.012-2.707,1.99C24.957,25.543,25,26.511,25,27v9h-5V19h5v2.616C25.721,20.5,26.85,19,29.738,19	c3.578,0,6.261,2.25,6.261,7.274L36,36L36,36z"
      ></path>
    </svg>
  );
}
