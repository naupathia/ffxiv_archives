import { Suspense } from "react";
import SearchBox from "../ui/searchBox";
import SearchResults from "../ui/searchResults";
import ScrollToTopButton from "../ui/scrollToTopButton";

export default function Page({
  searchParams,
}: {
  searchParams?: {
    q?: string;
    page?: string;
    sort?: string;
  };
}) {
  const query = searchParams?.q || "";
  const currentPage = Number(searchParams?.page) || 1;

  return (
    <div className="flex flex-row">
      <div className="p-8 flex-1 ">
        <div className="flex items-center justify-between gap-2 min-w-full">
          <SearchBox placeholder="Search..." />
        </div>

        <div className="mt-6">
          <Suspense fallback={<Loading />}>
            <SearchResults
              query={query}
              currentPage={currentPage}
              sort={searchParams?.sort}
            />
          </Suspense>
        </div>

        <ScrollToTopButton />
      </div>

      {/* <div className="hidden md:block flex-none w-1/4 border-l-2 border-orange-300 p-6 min-h-screen">
              <BookmarksList />
            </div> */}
    </div>
  );
}

function Loading() {
  return <p className="mt-6">searching...</p>;
}
