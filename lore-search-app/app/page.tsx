
import Search from "./ui/search";
import { Suspense  } from "react";
import SearchResults from "./ui/searchResults";

export default function Page({
  searchParams,
}: {
  searchParams?: {
    query?: string;
    page?: string;
  };
}) {
  // const [bookmarks, setBookmarks] = useState([]);
  const bookmarks = [];

  const query = searchParams?.query || "";
  const currentPage = Number(searchParams?.page) || 1;

  return (
    <main className="flex flex-row min-h-screen">
      <div className="basis-1/4 pr-8 border-r-2 border-orange-300">
        <div className="flex flex-col p-4">
          <h1 className="font-center">BOOKMARKS</h1>
          {bookmarks?.map((bm: any) => (
            <p>{bm.name}</p>
          ))}
        </div>
      </div>

      <div className="basis-3/4 p-8">
        <div className="flex items-center justify-between gap-2">
          <Search placeholder="Search..." />
        </div>

        <Suspense fallback={<Loading />}>
          <SearchResults query={query} currentPage={currentPage} />
        </Suspense>
      </div>
    </main>
  );
}

function Loading() {
  return <p className="mt-6">searching...</p>;
}
