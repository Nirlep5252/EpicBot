import { useEffect } from "react";
import { useSearchParams } from "react-router-dom";

export default function Oauth2() {
  const [searchParams] = useSearchParams();

  useEffect(() => {
    const code = searchParams.get("code");
    if (!code) {
      window.location.href = "/";
      return;
    }
    fetch(`/api/token/${searchParams.get("code")}`)
      .then((res) => {
        if (res.status === 200) {
          res
            .json()
            .then((data) => {
              console.log(data);
              console.log(data.access_token);
              localStorage.setItem("token", data.access_token);
            })
            .finally(() => {
              window.location.href = "/";
            });
        } else {
          console.log(`ERROR: Non 200 status code: ${res.status}`);
          window.location.href = "/";
        }
      })
      .catch((err: Error) => {
        console.log(`ERROR: ${err}`);
        window.location.href = "/";
      });
  }, [searchParams]);

  return <>logging you in...</>;
}
