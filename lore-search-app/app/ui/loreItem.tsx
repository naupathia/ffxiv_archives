"use client";
import React from "react";
import clsx from "clsx";

export default function LoreItem({ lore }) {
  const [isHidden, setHidden] = React.useState(false);

  function hideMe(e) {
    setHidden(!isHidden);
  }

  return (
    <div className="mb-8 p-4 paper rounded shadow-md">
      <div className="flex align-top">
        <h1 className="flex-1 text-xl font-bold">{lore.name}</h1>
        <span className="text-sm font-normal">{lore.datatype}</span>
        <button className="ml-2" onClick={hideMe}>
          {isHidden ? "+" : "x"}
        </button>
      </div>
      <div className={clsx("mt-4", isHidden && "hidden")}>

        <div className="flex">
          {lore.issuer ? (
            <div className="bg-gray-500/30 p-2 mt-2">
              <p>
                {lore.issuer} ({lore.place_name}) 
              <p>
                {lore.journal_genre} ({lore.expansion})
              </p>
            </div>
          ) : (
            <></>
          )}
        </div>

        <p className="whitespace-pre-wrap mt-4">{lore.text}</p>
      </div>
    </div>
  );
}
