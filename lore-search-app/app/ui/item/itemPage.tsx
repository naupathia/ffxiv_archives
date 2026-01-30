"use client";

import LoreCard from "./loreCard";
import { useEffect } from "react";

export default function ItemPage({ lore }: { lore: LoreEntry }) {
  useEffect(() => {
    document.title = `TEA Tools | ${lore.title}`;
  }, []);
  return <LoreCard lore={lore} toggleable={false} />;
}
