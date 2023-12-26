"use client";

import Link from "next/link";
import { useBookmarksDispatch } from "./bookmarksContexts";
import { XMarkIcon } from "@heroicons/react/24/solid";
import { useSearchParams } from "next/navigation";
import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import { Bars3Icon } from "@heroicons/react/24/solid";

export default function BookmarkListItem({ item }: { item: Bookmark }) {
  const bookmarksDispatch = useBookmarksDispatch();
  const searchParams = useSearchParams();
  const q = searchParams.get("q");
  const { attributes, listeners, setNodeRef, transform, transition } =
    useSortable({ id: item.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  function removeBookmark(e: any) {
    bookmarksDispatch({
      type: "delete",
      id: item.id,
    });
  }

  return (
    <div
      key={item.id}
      ref={setNodeRef}
      style={style}
      {...attributes}
      className="flex flex-row items-start p-1"
    >
      <Bars3Icon className="h-6 w-6 mr-2" {...listeners} />

      <Link
        href={`/search/entries?id=${item.id}` + (q ? `&q=${q}` : "")}
        className="flex-1 pr-4 hover:text-orange-300"
      >
        {item.name}
      </Link>
      
      <button title="remove" onClick={removeBookmark}>
        <XMarkIcon className="place-self-end text-white h-6 w-6" />
      </button>
    </div>
  );
}
