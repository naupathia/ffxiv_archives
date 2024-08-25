"use client";

import LoreEntryCard from "./loreEntryCard";

export default function LoreEntryList({
  items,
  searchText
}: {
  items: LoreEntry[];
  searchText?: string;
}) {
  const hasResults = items && items.length > 0; 

  return (
    <div className="flex-1">
      <div className="flex flex-col space-y-8">
        {hasResults &&
          items.map((item: LoreEntry) => (
            <div key={item._id}>
              <a id={item._id} />
              <LoreEntryCard
                lore={item}
                searchText={searchText}
              ></LoreEntryCard>
            </div>
          ))}
      </div>
    </div>
  );
}
