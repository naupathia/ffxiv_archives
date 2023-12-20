"use client";
import { useState } from "react";
import clsx from "clsx";
import { roboto_mono } from "../../types/fonts";
import { useBookmarksDispatch } from "./bookmarksContexts";
import { BookmarkIcon, PlusIcon, MinusIcon } from "@heroicons/react/24/solid";

export default function LoreItemCard({
  lore,
  searchText,
  isDetailView=true
}: {
  lore: LoreEntry;
  searchText?: string;
  isDetailView?: boolean
}) {
  const [isHidden, setHidden] = useState(false);
  const dispatch = useBookmarksDispatch();

  function toggleVisibility(e: any) {
    setHidden(!isHidden);
  }

  function updateBookmarkStatus(e: any) {
    console.log("button pushed");
    dispatch({
      type: "add",
      id: lore._id,
      name: lore.name,
      datatype: lore.datatype,
    });
  }

  function translateType(type: string) {
    switch (type) {
      case "TRIPLETRIADCARD":
        return "TRIPLE TRIAD CARD";
      default:
        return type;
    }
  }

  function highlightSearchText(text?: string) {
    if (searchText) {
      const words = new RegExp(
        "\\b(" + searchText?.split(" ").join("|") + ")\\b",
        "gmi"
      );
      return text?.replace(words, "<mark>$&</mark>") ?? "";
    }
    return text;
  }

  return (
    <div className="lore-item border-2 border-orange-300">
      <div className="flex items-baseline">
        <button onClick={toggleVisibility} title={isHidden ? "show" : "hide"}>
          {isHidden ? (
            <PlusIcon className="h-4 w-4" />
          ) : (
            <MinusIcon className="h-4 w-4" />
          )}
        </button>
        <h1 className="flex-1 text-xl font-bold ml-2">{lore.name}</h1>
        <span className="text-sm font-normal">
          {translateType(lore.datatype)}
        </span>
        <button
          className={clsx("pl-4", isDetailView && "hidden")}
          onClick={updateBookmarkStatus}
          title="bookmark"
        >
          <BookmarkIcon className="text-white h-6 w-6" />
        </button>
      </div>

      <div className={clsx("mt-4 ml-12 mr-12", isHidden && "hidden")}>
        <div className="flex">
          {lore.issuer ? (
            <div className="bg-gray-200/20 p-2 mt-2">
              <p>
                {lore.issuer} ({lore.place_name})
              </p>
              <p>
                {lore.journal_genre} ({lore.expansion})
              </p>
            </div>
          ) : (
            <></>
          )}
        </div>

        <div
          className={clsx("whitespace-pre-wrap mt-4")}
          dangerouslySetInnerHTML={{ __html: highlightSearchText(lore.text) || '' }}
        ></div>
      </div>
    </div>
  );
}
