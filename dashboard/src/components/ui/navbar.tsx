import { useUser } from "@/lib/queries";
import { Loader2Icon } from "lucide-react";
import { Button } from "./button";
import config from "@/config";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "./dropdown-menu";
import { Avatar, AvatarFallback, AvatarImage } from "./avatar";
import { Link } from "react-router-dom";

export default function Navbar() {
  const { data: user, isLoading: isUserLoading } = useUser();

  return (
    <div className="w-screen h-24 fixed p-4">
      <div className="w-full h-full m-auto border border-border rounded-full flex items-center justify-between px-8">
        <div className="left">left</div>
        <div className="middle">middle</div>
        <div className="right">
          {isUserLoading ? (
            <Loader2Icon className="animate-spin h-8 w-8" />
          ) : user ? (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Avatar>
                  <AvatarImage
                    src={`https://cdn.discordapp.com/avatars/${user.id}/${user.avatar}.png`}
                  />
                  <AvatarFallback>
                    {(user.username as string).charAt(0).toUpperCase()}
                  </AvatarFallback>
                </Avatar>
              </DropdownMenuTrigger>
              <DropdownMenuContent>
                <DropdownMenuLabel>{user.global_name}</DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem>
                  <Link to="/logout">logout</Link>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          ) : (
            <Button asChild>
              <Link to={config.LOGIN_URL}>Sign In</Link>
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
