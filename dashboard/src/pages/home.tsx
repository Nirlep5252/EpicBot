import { Link } from "react-router-dom";
import { useUser } from "../lib/queries";

export default function Home() {
  const { data, isLoading, isError, error } = useUser();
  return (
    <div className="w-screen h-screen flex items-center justify-center">
      <div>
        {isLoading ? (
          "Loading..."
        ) : isError ? (
          error.message
        ) : data ? (
          <>
            Logged in as {data?.global_name} <Link to="/logout">Logout</Link>
          </>
        ) : (
          <Link to="/login">Login</Link>
        )}
      </div>
    </div>
  );
}
