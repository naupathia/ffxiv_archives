"use client";

import Link from "next/link";
import { useBookmarksDispatch } from "./bookmarksContexts";
import { XMarkIcon } from "@heroicons/react/24/solid";
import { useSearchParams } from "next/navigation";


export default function BookmarkListItem({ item }: { item: Bookmark }) {
  const bookmarksDispatch = useBookmarksDispatch();
  const searchParams = useSearchParams();
  const q = searchParams.get("q");

  function removeBookmark(e: any) {
    bookmarksDispatch(
        {
            'type': 'delete',
            'id': item.id,
        }
    )
  }

  return (
    <div key={item.id} className="flex flex-row items-start mb-2 border-b-2 border-white/20 p-1">
      <Link href={`/search/entries?id=${item.id}` + (q ? `&q=${q}` : '')} className="min-w-fit grow pr-4 hover:text-orange-300">{item.name}</Link>
      <button title="remove" onClick={removeBookmark}><XMarkIcon className="place-self-end text-white h-6 w-6"/></button>
    </div>
  );
}
