import { Suspense } from "react";
import SearchBox from "../ui/searchBox";
import SearchResults from "../ui/searchResults";
import BookmarksList from "../ui/bookmarksList";
import BookmarksProvider from "../ui/bookmarksContexts";
import SearchNavigationProvider from "../ui/searchNavigationContexts";
import SearchNavigationList from "../ui/searchNavigationList";
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
    <div>
      <BookmarksProvider>
        <SearchNavigationProvider>
          <div className="flex">
            <div className="hidden md:block flex-none w-1/4 border-r-2 border-orange-300 p-6 min-h-screen">
              <SearchNavigationList />
            </div>

            <div className="p-8">
              <div className="flex flex-1 items-center justify-between gap-2 min-w-full">
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

            <div className="hidden md:block flex-none w-1/4 border-l-2 border-orange-300 p-6 min-h-screen">
              <BookmarksList />
            </div>
          </div>
        </SearchNavigationProvider>
      </BookmarksProvider>
    </div>
  );
}

function Loading() {
  return <p className="mt-6">searching...</p>;
}
