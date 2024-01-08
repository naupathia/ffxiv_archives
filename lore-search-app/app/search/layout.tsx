import Link from "next/link";
import BookmarksProvider from "../ui/bookmarksContexts";
import SynonymsProvider from "../ui/synonymsContext";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div>
      <main className="min-h-screen min-w-full">
        <div className="p-2 flex flex-row justify-center gap-x-4 border-b-2 border-orange-300">
          <Link
            className="p-2 basis-1 grow text-center hover:bg-orange-300 hover:text-black"
            href={`/search`}
          >
            SEARCH
          </Link>
          <Link
            className="p-2 basis-1 grow text-center hover:bg-orange-300 hover:text-black"
            href={`/search/bookmarks`}
          >
            BOOKMARKS
          </Link>
        </div>
        <BookmarksProvider>
          <SynonymsProvider>{children}</SynonymsProvider>
        </BookmarksProvider>
      </main>
    </div>
  );
}
