"use client";
import { useState } from "react";
import clsx from "clsx";
import { useBookmarksDispatch } from "./bookmarksContexts";
import { BookmarkIcon, PlusIcon, MinusIcon } from "@heroicons/react/24/solid";
import { useSynonyms } from "./synonymsContext";
import { useSearchParams } from "next/navigation";

export default function LoreEntryCard({
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
      if (searchText.startsWith('"') && searchText.endsWith('"')) {
        const rwords = new RegExp(
          "\\b(" + searchText.slice(1, -1) + ")\\b",
          "gmi"
        );
        return text?.replace(rwords, "<mark>$&</mark>") ?? "";
      } else {
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
    }
    return text;
  }

  return (
    <div className="lore-item">
      <div className="flex items-baseline">
        <button onClick={toggleVisibility} title={isHidden ? "show" : "hide"}>
          {isHidden ? (
            <PlusIcon className="h-4 w-4" />
          ) : (
            <MinusIcon className="h-4 w-4" />
          )}
        </button>
        <h2 className="flex-1 text-xl ml-2">{lore.name}</h2>
        <span className="text-sm font-normal">
          {translateType(lore.datatype)}
        </span>
      </div>

      <div className={clsx("lore-item-body", isHidden && "hidden")}>
        {lore.issuer ? (
          <div className="flex mb-4">
            <div className="bg-gray-200/20 p-2">
              <p>
                {lore.issuer} ({lore.place_name})
              </p>
              <p>
                {lore.journal_genre} ({lore.expansion})
              </p>
            </div>
          </div>
        ) : (
          <></>
        )}

        <p
          className="whitespace-pre-wrap"
          dangerouslySetInnerHTML={{
            __html: highlightSearchText(lore.text) || "",
          }}
        >
        </p>
      </div>
    </div>
  );
}
