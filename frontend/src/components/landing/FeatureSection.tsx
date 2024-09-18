import { useState } from "react";
import { motion } from "framer-motion";
import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Calendar,
  Clipboard,
  Users,
  UserCog,
  CalendarClock,
  ListTodo,
} from "lucide-react";

const features = [
  {
    title: "Patient Account Management",
    description: "Easily manage your personal information and preferences.",
    icon: UserCog,
  },
  {
    title: "Appointment Booking",
    description: "Book and view your dental appointments with ease.",
    icon: Calendar,
  },
  {
    title: "Treatment History",
    description: "Access your complete dental treatment history anytime.",
    icon: Clipboard,
  },
  {
    title: "Doctor Patient Management",
    description: "Efficiently manage patient records and treatment plans.",
    icon: Users,
  },
  {
    title: "Receptionist Appointment Management",
    description: "Streamline appointment scheduling and management.",
    icon: CalendarClock,
  },
  {
    title: "Doctor Work Schedule",
    description: "View and manage doctor availability and work hours.",
    icon: ListTodo,
  },
];

export default function AnimatedFeatures() {
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);

  return (
    <section className="py-12 bg-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
            Comprehensive Dental Clinic Management
          </h2>
          <p className="mt-4 text-xl text-gray-500">
            Explore our feature-rich platform designed for patients, doctors,
            and staff.
          </p>
        </div>
        <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              whileHover={{ scale: 1.05 }}
              onHoverStart={() => setHoveredIndex(index)}
              onHoverEnd={() => setHoveredIndex(null)}
            >
              <Card className="h-full">
                <CardHeader>
                  <motion.div
                    initial={false}
                    animate={{
                      scale: hoveredIndex === index ? 1.04 : 1,
                    }}
                    transition={{ duration: 0.3 }}
                    className="mb-2"
                  >
                    <feature.icon className="h-8 w-8 text-blue-500" />
                  </motion.div>
                  <CardTitle>{feature.title}</CardTitle>
                  <CardDescription>{feature.description}</CardDescription>
                </CardHeader>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
