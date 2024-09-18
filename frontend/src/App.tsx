import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { RouterProvider } from "react-router-dom";
import { router } from "./routes";
import { AuthProvider } from "./components/AuthContext";
import { Toaster } from "./components/ui/toaster";

const queryClient = new QueryClient();

const App = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <RouterProvider router={router} />
        {/* TODO: change to false after deployment */}
        <ReactQueryDevtools initialIsOpen={true} />
        <Toaster />
      </AuthProvider>
    </QueryClientProvider>
  );
};

export default App;
