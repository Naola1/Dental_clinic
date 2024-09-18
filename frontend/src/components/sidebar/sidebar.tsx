import useAuthStore from "@/hooks/zustand/use-auth-store";
import { Button } from "../ui/button";

import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { SidebarItem } from "types/auth";

interface SidebarProps {
  items: SidebarItem[];
}

export function Sidebar({ items }: SidebarProps) {
  const navigate = useNavigate();
  const location = useLocation();
  const urlPath = location.pathname;
  const splitedPath = urlPath.split("/");

  const currentPath = splitedPath[splitedPath.length - 1];

  const authStore = useAuthStore();

  return (
    <div className="pb-12 flex w-screen">
      <div className="space-y-4 py-4 max-w-xs h-screen shadow-md">
        <div className="px-4 py-2 relative">
          <h2 className="mb-2 px-2 text-xl font-semibold">
            Lily Dental Clinic
          </h2>
          <div className="space-y-1 mt-6 h-screen">
            {items.map((item) => (
              <Button
                key={item.href}
                variant={
                  item.title.toLocaleLowerCase() !== currentPath
                    ? "ghost"
                    : "default"
                }
                className="w-full justify-start pl-2 font-light text-lg"
                size="lg"
                onClick={() => navigate(item.href)}
              >
                {item.title}
              </Button>
            ))}
            <Button
              className="absolute bottom-[20%] left-4"
              onClick={() => {
                authStore.logout();
                navigate("/login");
              }}
            >
              Logout
            </Button>
          </div>
        </div>
      </div>
      <div className="w-full">
        <Outlet />
      </div>
    </div>
  );
}
