"use client";
import { useState } from "react";
import clsx from "clsx";
import { useBookmarksDispatch } from "./bookmarksContexts";
import { BookmarkIcon, PlusIcon, MinusIcon } from "@heroicons/react/24/solid";
import { useSynonyms } from "./synonymsContext";
import { useSearchParams } from "next/navigation";

export default function LoreItemCard({
  lore,
  showBookmark = false,
}: {
  lore: LoreEntry;
  showBookmark?: boolean;
}) {
  const [isHidden, setHidden] = useState(false);
  const dispatch = useBookmarksDispatch();
  const { synonyms } = useSynonyms();
  const searchParams = useSearchParams();
  const searchText = searchParams.get("q");

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
      let words = searchText?.split(" ");
      if (synonyms) {
        words.forEach((w: string) => {
          if (synonyms[w.toLowerCase()]) {
            words = [...words, ...synonyms[w.toLowerCase()]];
          }
        });
      }
      const rwords = new RegExp("\\b(" + words.join("|") + ")\\b", "gmi");
      return text?.replace(rwords, "<mark>$&</mark>") ?? "";
    }
    return text;
  }

  return (
    <div className="lore-item p-6 border-2 border-orange-300">
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
        {/* <button
          className={clsx("pl-4", !showBookmark && "hidden")}
          onClick={updateBookmarkStatus}
          title="bookmark"
        >
          <BookmarkIcon className="text-white h-6 w-6" />
        </button> */}
      </div>

      <div className={clsx("mt-4", isHidden && "hidden")}>
        <div className="flex mb-4">
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
          className="whitespace-pre-wrap"
          dangerouslySetInnerHTML={{
            __html: highlightSearchText(lore.text) || "",
          }}
        >
          {/* {lore.text} */}
        </div>
      </div>
    </div>
  );
}
