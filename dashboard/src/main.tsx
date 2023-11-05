import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./index.css";
import Home from "./pages/home";
import Redirect from "./components/redirect";
import config from "./config";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import Oauth2 from "./pages/oauth2";
import Logout from "./components/logout";
import Navbar from "./components/ui/navbar";

const queryClient = new QueryClient();

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Redirect to={config.LOGIN_URL} />} />
          <Route path="/oauth2/redirect" element={<Oauth2 />} />
          <Route path="/logout" element={<Logout />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>
);
