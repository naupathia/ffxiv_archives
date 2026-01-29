"use client";

import { PrimeReactProvider } from "primereact/api";
import LoreCard from "../item/loreCard";

export default function LoreEntryList({
  items,
  searchText,
}: {
  items: LoreEntry[];
  searchText: string;
}) {
  const options = {
    cssTransition: false,
  };

  const hasResults = items && items.length > 0;

  return (
    <PrimeReactProvider value={options}>
      <div className="flex-1">
        <div className="flex flex-col gap-6">
          {hasResults &&
            items.map((item: LoreEntry) => (
              <div key={item._id}>
                <a id={item._id} />
                <LoreCard
                  text={item.text_html}
                  lore={item}
                  toggleable={true}
                ></LoreCard>
              </div>
            ))}
        </div>
      </div>
    </PrimeReactProvider>
  );
}
