import { useQuery } from "@tanstack/react-query";

export default function Home() {
  const { data, isLoading } = useQuery({
    queryKey: ["ping"],
    queryFn: () => fetch("http://localhost:8000/ping").then((res) => res.json()),
  });

  const text = isLoading ? "Loading..." : data?.status;
  return (
    <div>
      <h1>Home Page</h1>
      <p>{text}</p>
    </div>
  );
}
