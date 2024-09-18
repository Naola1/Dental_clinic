import { create } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";

interface AuthStore {
  token: string | null;
  login: (token: string) => void;
  logout: () => void;
}
const useAuthStore = create(
  persist<AuthStore>(
    (set) => ({
      token: "",
      login: (token) => {
        set({ token: token });
      },
      logout: () => {
        sessionStorage.clear();
      },
    }),
    {
      name: "token",
      storage: createJSONStorage(() => sessionStorage),
    }
  )
);

export default useAuthStore;
