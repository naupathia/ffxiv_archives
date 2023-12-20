
import SearchBox from "./ui/searchBox";
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
  // const bookmarks = [];

  const query = searchParams?.query || "";
  const currentPage = Number(searchParams?.page) || 1;

  return (
    <main className="flex flex-row min-h-screen">
      Search ----
    </main>
  );
}

function Loading() {
  return <p className="mt-6">searching...</p>;
}
