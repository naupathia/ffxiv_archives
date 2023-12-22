"use client";

import LoreItemCard from "./loreItemCard";
import { useSearchNavigation } from "./searchNavigationContexts";

export default function SearchResultsList({
  items,
  query,
}: {
  items: LoreEntry[];
  query?: string;
}) {
  const { setNavItems } = useSearchNavigation();
  const options = [
    "Try harder next time.",
    "Maybe something less obscure?",
    "Check for typos!",
  ];
  const hasResults = items && items.length > 0;

  if (items) {
    setNavItems(items.map((i) => ({ id: i._id, name: i.name })));
  }

  return (
    <div className="flex flex-col flex-1 space-y-12">
      {hasResults ? (
        items.map((item: LoreEntry) => (
          <div key={item._id}>
            <a id={item._id} />
            <LoreItemCard
              lore={item}
              searchText={query}
              isDetailView={false}
            ></LoreItemCard>
          </div>
        ))
      ) : query ? (
        <p className="text-white">
          No lore found. {_.sampleSize(options, 1)[0]}
        </p>
      ) : (
        <p></p>
      )}
    </div>
  );
}
