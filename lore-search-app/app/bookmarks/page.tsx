'use client'
import LoreEntryList from "@/app/ui/loreEntryList";
import { useBookmarks } from "../ui/bookmarksContexts";

export default async function Page() {
  const bookmarks = useBookmarks();

  return (
    <div className="p-8">

      <div className="flex flex-col space-y-8 mt-6">
        
      </div>
    </div>
  );
}
