// import Link from "next/link";

// export default function Page({
//   searchParams,
// }: {
//   searchParams?: {
//     query?: string;
//     page?: string;
//   };
// }) {
//   const query = searchParams?.query || "";
//   const currentPage = Number(searchParams?.page) || 1;

//   return (
//     <main className="flex flex-row justify-center">
//       <Link className="p-4" href='/search'>Search For Lore</Link>
//     </main>
//   );
// }

import { redirect } from "next/navigation";

export default function Page() {
  return redirect("/search");
}
