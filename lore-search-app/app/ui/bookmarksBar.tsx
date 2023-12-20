"use client";

import { useBookmarks } from "./bookmarksContexts";
import BookmarkListItem from "./bookmarkListItem";
import { FolderArrowDownIcon } from "@heroicons/react/24/solid";


export default function BookmarksBar() {
  const bookmarks = useBookmarks();

  return (
    <div className="flex flex-col border-l-2 border-orange-300 p-4 min-w-fit basis-1/6">
      <div className="flex flex-row mb-4">
        <h2 className="flex-1 text-xl text-orange-300 pr-4">BOOKMARKS</h2>
        <button title="download"><FolderArrowDownIcon className="text-white h-6 w-6"/></button>
      </div>
      {bookmarks.map((item: Bookmark) => (
        <BookmarkListItem key={item.id} item={item} />
      ))}
    </div>
  );
}
