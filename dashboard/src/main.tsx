import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "./index.css";
import Home from "./pages/Home";
import Redirect from "./components/Redirect";
import config from "./config";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import Oauth2 from "./pages/Oauth2";
import Logout from "./components/Logout";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
  },
  {
    path: "/login",
    element: <Redirect to={config.LOGIN_URL} />,
  },
  {
    path: "/oauth2/redirect",
    element: <Oauth2 />,
  },
  {
    path: "/logout",
    element: <Logout />,
  },
]);
const queryClient = new QueryClient();

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  </React.StrictMode>
);
