import Search from "./ui/search";
import { Suspense } from "react";
import SearchResults from "./ui/searchResults";

export default async function Page({
  searchParams,
}: {
  searchParams?: {
    query?: string;
    page?: string;
  };
}) {
  const query = searchParams?.query || '';
  const currentPage = Number(searchParams?.page) || 1;
 
  return (
    <main className="flex min-h-screen flex-col justify-between p-24">
      <div>
        <div className="w-full">
          <div className="flex w-full items-center justify-between">
            <h1 className="text-2xl">TEA Tools</h1>
          </div>
          <div className="mt-4 flex items-center justify-between gap-2 md:mt-8">
            <Search placeholder="Search..." />
          </div>
          <Suspense>
            <SearchResults query={query} currentPage={currentPage} />
          </Suspense>
          <div className="mt-5 flex w-full justify-center">
            {/* <Pagination totalPages={totalPages} /> */}
          </div>
        </div>
      </div>
    </main>
  );
}
