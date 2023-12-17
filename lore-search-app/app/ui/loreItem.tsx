"use client";
import React from "react";
import clsx from "clsx";

export default function LoreItem({ lore, searchText } : {lore: any, searchText: string}) {
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
    <div className="mb-8 p-4 border-2 border-white border-l-slate-200">
      <div className="flex items-baseline">
        <h1 className="flex-1 text-xl font-bold">{lore.name}</h1>
        <span className="text-sm font-normal">{translateType(lore.datatype)}</span>
        <button className="ml-2" onClick={hideMe}>
          {isHidden ? (
            <div className="plus"></div>
          ) : (
            <div className="cross"></div>
          )}
        </button>
      </div>

      <div className={clsx("mt-4", isHidden && "hidden")}>
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

        <div className="whitespace-pre-wrap mt-4" dangerouslySetInnerHTML={{__html: highlightSearchText(lore.text)}}></div>
      </div>
    </div>
  );
}
