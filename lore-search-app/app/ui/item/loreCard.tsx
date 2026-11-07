"use client";

import { useState } from "react";
import LoreBody from "./loreBody";
import { convertToTitleCase } from "@/app/lib/functions";

export default function LoreCard({
  lore,
  toggleable,
}: {
  lore: LoreEntry;
  toggleable: boolean;
}) {
  const [collapsed, setCollapsed] = useState(false);
  const headerText = lore.title
    ? lore.title
    : convertToTitleCase(lore.datatype.name);
  const typeText = lore.title ? lore.datatype.name.toUpperCase() : "";
  const [showJP, setShowJP] = useState(false);

  const hasJpText = lore.text_jp != null && lore.text_jp != '';

  return (
    <article className="lore-card">
      <header className="lore-card-header">
        <div className="lore-card-heading">
          <h2 className="lore-card-title">
            {toggleable ? (
              <a href={`/item/${lore._id}`} target="_blank" rel="noreferrer">
                {headerText}
              </a>
            ) : (
              headerText
            )}
          </h2>
          {typeText && <span className="lore-card-type">{typeText}</span>}
        </div>
        <div className="lore-card-actions">
          <button
            className="language-toggle"
            type="button"
            aria-pressed={showJP}
            disabled={!hasJpText}
            onClick={() => setShowJP((current) => !current)}
          >
            {showJP ? "JP" : "EN"}
          </button>
          {toggleable && (
            <button
              className="collapse-toggle"
              type="button"
              aria-expanded={!collapsed}
              aria-label={collapsed ? "Expand entry" : "Collapse entry"}
              onClick={() => setCollapsed((current) => !current)}
            >
              <span aria-hidden="true">{collapsed ? "+" : "−"}</span>
            </button>
          )}
        </div>
      </header>
      {!collapsed && (
        <div className="lore-card-content">
          <LoreBody lore={lore} showJP={showJP} />
        </div>
      )}
    </article>
  );
}
