"use client";

import { translateType } from "@/app/lib/functions";
import LoreItemBody from "./loreItemBody";

export default async function ItemPage({ lore }: { lore: LoreEntry }) {
  return (
    <div className="lore-item">
      <div className="flex items-baseline">
        <h2 className="flex-1 text-xl ml-2">{lore.name}</h2>
        <span className="text-sm font-normal">
          {translateType(lore.datatype)}
        </span>
      </div>

      <LoreItemBody text={lore.text} lore={lore} />
    </div>
  );
}
