// "use client";

// import { useEffect } from "react";
import LoreItemCard from "./loreItemCard";
// import { useSearchNavigation } from "./searchNavigationContexts";

export default function LoreEntryList({
  items,
  showBookmark = false,
}: {
  items: LoreEntry[];
  showBookmark?: boolean;
}) {
  // const { setNavItems } = useSearchNavigation();
  const hasResults = items && items.length > 0;

  // useEffect(() => {
  //   if (items) {
  //     setNavItems(items.map((i) => ({ id: i._id, name: i.name })));
  //   } else {
  //     setNavItems([]);
  //   }
  // }, []);

  return (
    <div className="flex-1">
      <div className="flex flex-col space-y-12">
        {hasResults &&
          items.map((item: LoreEntry) => (
            <div key={item._id}>
              <a id={item._id} />
              <LoreItemCard lore={item} showBookmark={showBookmark}></LoreItemCard>
            </div>
          ))}
      </div>
    </div>
  );
}
