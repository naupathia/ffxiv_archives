import BookmarksBar from "../ui/bookmarksBar";
import BookmarksProvider from "../ui/bookmarksContexts";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div>
      <main className="flex flex-col md:flex-row min-h-screen">
        <BookmarksProvider>
          <div className="flex flex-row min-w-full">
            <div className="p-8 basis-full">{children}</div>

            <BookmarksBar />
          </div>
        </BookmarksProvider>
      </main>
    </div>
  );
}
