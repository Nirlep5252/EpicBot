import { createQuery } from "react-query-kit";

export const useUser = createQuery({
  primaryKey: "user",
  queryFn: async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      console.log("NO TOKEN");
      return null;
    }
    const res = await fetch(`/api/user/${token}`);
    if (res.status !== 200) {
      // localStorage.removeItem("token");
      return null;
    }
    return res.json();
  },
});
