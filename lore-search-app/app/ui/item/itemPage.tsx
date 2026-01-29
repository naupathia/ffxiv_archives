"use client";

import { translateType } from "@/app/lib/functions";
import LoreCard from "./loreCard";
import { useEffect } from "react";

export default async function ItemPage({ lore }: { lore: LoreEntry }) {
  useEffect(() => {
    document.title = `TEA Tools | ${lore.title}`;
  }, []);
  return (
    <div className="lore-item">
      <div className="flex items-baseline">
        <h2 className="flex-1 text-xl ml-2">{lore.title}</h2>
        <span className="text-sm font-normal">
          {translateType(lore.datatype)}
        </span>
      </div>

      <LoreCard text={lore.text_html} lore={lore} toggleable={false}/>
    </div>
  );
}
