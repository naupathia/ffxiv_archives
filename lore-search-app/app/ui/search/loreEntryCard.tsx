"use client";
import { useEffect, useState } from "react";
import { PlusIcon, MinusIcon } from "@heroicons/react/24/solid";
import { highlightSearchText, translateType } from "@/app/lib/functions";
import LoreItemBody from "../item/loreItemBody";
import Link from "next/link";

export default function LoreEntryCard({
  lore,
  searchText,
}: {
  lore: LoreEntry;
  searchText?: string;
}) {
  const [isHidden, setHidden] = useState(false);
  const [synonyms, setSynonyms] = useState(null);

  useEffect(() => {
    if (!synonyms) {
      const fetchSynonyms = async () => {
        const response = await fetch("/api/synonyms");
        const result = await response.json();
        setSynonyms(result);
      };

      fetchSynonyms().catch((error) => console.log(error));
    }
  }, []);

  function toggleVisibility(e: any) {
    setHidden(!isHidden);
  }

  const innerText = highlightSearchText(lore.text, searchText, synonyms) || "";

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
        <h2 className="flex-1 text-xl ml-2">
          <Link href={`/item/${lore._id}`} target="_blank">{lore.name}</Link>
        </h2>
        <span className="text-sm font-normal">
          {translateType(lore.datatype)}
        </span>
      </div>

      <div className={isHidden ? "hidden" : ""}>
        <LoreItemBody text={innerText} lore={lore} />
      </div>
    </div>
  );
}
