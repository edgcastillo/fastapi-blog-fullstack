import { ReactComponent as Logo } from "../assets/photo-svgrepo-com.svg";
import { ReactComponent as SearchIcon } from "../assets/magnifying-glass-svgrepo-com.svg";

export default function Navigation() {
  return (
    <nav>
      <div className="logo-container w-25 flex flex-col items-center">
        <Logo />
        <h5>My Blog</h5>
      </div>
      <div className="search-container self-center mt-[10px]">
        <SearchIcon />
        <input className="w-[20rem]" type="search" placeholder="Search..." />
      </div>
      <div className="buttons-container w-[20%] h-[50%] self-center flex gap-4">
        <button className="ml-auto w-[10rem] h-[3rem] rounded-[50px] bg-blue-500 text-white">Login</button>
        <button className="w-[7rem] h-[3rem] rounded-[50px] border border-gray-500">Join</button>
      </div>
    </nav>
  );
}
