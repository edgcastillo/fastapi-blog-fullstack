import { ReactComponent as Logo } from "../assets/photo-svgrepo-com.svg";
import { ReactComponent as SearchIcon } from "../assets/magnifying-glass-svgrepo-com.svg";

export default function Navigation() {
  return (
    <nav>
      <div className="logo-container w-25 flex flex-col items-center">
        <Logo />
        <h5>My Blog</h5>
      </div>
      <div className="search-container self-center">
        <SearchIcon />
        <input type="search" placeholder="Search..." />
      </div>
      <div className="buttons-container w-[30%] h-[50%] self-center flex gap-4">
        <button className="ml-auto w-[35%] h-[75%] bg-blue-500 text-white">Login</button>
        <button className="w-[35%] h-[75%] border border-gray-500">Sign Up</button>
      </div>
    </nav>
  );
}
