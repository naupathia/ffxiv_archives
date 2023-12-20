import { Suspense } from "react";
import SearchBox from "../ui/searchBox";
import SearchResults from "../ui/searchResults";

export default function Page({
  searchParams,
}: {
  searchParams?: {
    q?: string;
    page?: string;
  };
}) {

  const query = searchParams?.q || "";
  const currentPage = Number(searchParams?.page) || 1;

  return (
    <div>
      <div className="flex items-center justify-between gap-2 min-w-full">
        <SearchBox placeholder="Search..." />
      </div>

      <Suspense fallback={<Loading />}>
        <SearchResults query={query} currentPage={currentPage} />
      </Suspense>
    </div>
  );
}

function Loading() {
  return <p className="mt-6">searching...</p>;
}
