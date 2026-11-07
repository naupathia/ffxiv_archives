"use client";

import LoreCard from "../item/loreCard";

export default function LoreEntryList({
  items,
}: {
  items: LoreEntry[];
}) {
  const hasResults = items && items.length > 0;

  return (
    <div className="results-list">
      {hasResults &&
        items.map((item: LoreEntry) => (
          <div key={item._id} id={item._id}>
            <LoreCard lore={item} toggleable={true} />
          </div>
        ))}
    </div>
  );
}
