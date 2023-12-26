"use client";

import { useBookmarks, useBookmarksDispatch } from "./bookmarksContexts";
import BookmarkListItem from "./bookmarkListItem";
import { FolderArrowDownIcon, XCircleIcon } from "@heroicons/react/24/solid";
import useDownloader from "react-use-downloader";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import clsx from "clsx";
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
} from "@dnd-kit/core";
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
} from "@dnd-kit/sortable";

export default function BookmarksList() {
  const bookmarks = useBookmarks();
  const dispatch = useBookmarksDispatch();
  const searchParams = useSearchParams();
  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

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

  function handleDragEnd(event: any) {
    console.log("sorting!");
    const { active, over } = event;

    if (active.id !== over.id) {
      const oldIndex = bookmarks.findIndex((i) => i.id == active.id);
      const newIndex = bookmarks.findIndex((i) => i.id == over.id);
      console.log(`move ${oldIndex} to ${newIndex}`);

      const newlist = arrayMove(bookmarks, oldIndex, newIndex);
      dispatch({
        type: "set",
        value: newlist,
      });
    }
  }

  return (
    <div className="flex flex-col">
      {/* Bookmark list title area with buttons */}
      <div className="flex flex-row mb-4">
        <h2 className="flex-1 text-xl text-orange-300 pr-4">BOOKMARKS</h2>
        <button title="download" onClick={downloadBookmarks}>
          <FolderArrowDownIcon className="text-white h-6 w-6" />
        </button>
        <button title="clear all" onClick={clearBookmarks} className="pl-2">
          <XCircleIcon className="text-white h-6 w-6" />
        </button>
      </div>

      {/* the link to open all the bookmarks */}
      <Link
        className={clsx(
          "pb-2 hover:text-orange-300",
          bookmarks.length == 0 && "hidden"
        )}
        href={linkUrl}
      >
        (open all)
      </Link>

      {/* list of bookmarks */}
      <DndContext
        sensors={sensors}
        collisionDetection={closestCenter}
        onDragEnd={handleDragEnd}
      >
        <SortableContext
          items={bookmarks}
          strategy={verticalListSortingStrategy}
        >
          <div className="flex flex-col space-y-1">
          {bookmarks.map((item: Bookmark) => (
            <BookmarkListItem item={item} key={item.id} />
          ))}
          </div>
        </SortableContext>
      </DndContext>
    </div>
  );
}
