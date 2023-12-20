"use client";

import { useBookmarks, useBookmarksDispatch } from "./bookmarksContexts";
import BookmarkListItem from "./bookmarkListItem";
import { FolderArrowDownIcon, XCircleIcon } from "@heroicons/react/24/solid";
import useDownloader from "react-use-downloader";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import clsx from "clsx";

export default function BookmarksBar() {
  const bookmarks = useBookmarks();
  const dispatch = useBookmarksDispatch();
  const searchParams = useSearchParams();

  const { download, isInProgress } = useDownloader();
  const filename = "TEA Tools Bookmarks.txt";

  const q = searchParams.get("q");
  const qParam = q ? `&q=${q}` : "";
  const linkUrl =
    "/search/entries?" + bookmarks.map((b) => `id=${b.id}`).join("&") + qParam;

  function downloadBookmarks(e: any) {
    const params = bookmarks.map((i) => `id=${i.id}`).join("&");
    const url = `/api/lore-entries?${params}`;

    download(url, filename);
  }

  function clearBookmarks(e: any) {
    dispatch({ type: "clear" });
  }

  return (
    <div className="flex flex-col border-l-2 border-orange-300 p-4 min-w-fit basis-1/6">
      <div className="flex flex-row mb-4">
        <h2 className="flex-1 text-xl text-orange-300 pr-4">BOOKMARKS</h2>
        <button title="download" onClick={downloadBookmarks}>
          <FolderArrowDownIcon className="text-white h-6 w-6" />
        </button>
        <button title="clear all" onClick={clearBookmarks} className="pl-2">
          <XCircleIcon className="text-white h-6 w-6" />
        </button>
      </div>
      <Link
        className={clsx(
          "pb-2 hover:text-orange-300",
          bookmarks.length == 0 && "hidden"
        )}
        href={linkUrl}
      >
        (open all)
      </Link>
      {bookmarks.map((item: Bookmark) => (
        <BookmarkListItem key={item.id} item={item} />
      ))}
    </div>
  );
}
