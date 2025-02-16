import Navigation from "./Navigation";
import { Outlet } from "react-router";

export default function Layout() {
  return (
    <div>
      <Navigation />
      <main className="mt-[2rem]">
        <Outlet />
      </main>
    </div>
  );
} 