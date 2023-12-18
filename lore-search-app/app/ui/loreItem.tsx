"use client";
import React from "react";
import clsx from "clsx";
import { roboto_mono } from "./fonts";

export default function LoreItem({ lore, searchText } : {lore: any, searchText?: string}) {
  const [isHidden, setHidden] = React.useState(false);
  const words = new RegExp('\\b(' + searchText?.split(' ').join('|') + ')\\b', 'gmi');

  function hideMe(e: any) {
    setHidden(!isHidden);
  }

  function translateType(type: string) {
    switch (type) {
      case "TRIPLETRIADCARD":
        return "TRIPLE TRIAD CARD";
      default:
        return type;
    }
  }

  function highlightSearchText(text: string) {
    const result= text.replace(words, "<mark>$&</mark>");
    return result
  }

  return (
    <div className="lore-item border-2 border-orange-300">
      
      <div className="flex items-baseline">
        <button onClick={hideMe}>
          {isHidden ? (
            <div className="plus"></div>
          ) : (
            <div className="cross"></div>
          )}
        </button>
        <h1 className="flex-1 text-xl font-bold ml-2">{lore.name}</h1>
        <span className="text-sm font-normal">{translateType(lore.datatype)}</span>
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

        <div className={clsx("whitespace-pre-wrap mt-4", roboto_mono.className)} dangerouslySetInnerHTML={{__html: highlightSearchText(lore.text)}}></div>
      </div>
    </div>
  );
}
