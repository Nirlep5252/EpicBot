import { useEffect } from "react";

export default function Redirect(props: { to: string }) {
  console.log(props.to);
  useEffect(() => {
    window.location.href = props.to;
  }, [props.to]);
  return <></>;
}
