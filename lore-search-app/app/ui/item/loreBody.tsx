"use client";

import { convertToTitleCase, highlightText } from "@/app/lib/functions";
var showdown = require("showdown");

export default function LoreBody({
  lore,
}: {
  lore: LoreEntry;
}) {
  const isQuest = lore.datatype.name == "quest";
  const hasPlace = lore.meta?.place_name != null;

  const bodyText = highlightText(lore.text, lore.highlights)

  const converter = new showdown.Converter();
  const html = converter.makeHtml(bodyText);

  return (
    <div className="flex flex-col items-start">
      {isQuest ? (
        <blockquote>
          {lore.meta?.issuer} ({lore.meta?.place_name ?? ""})<br />
          {lore.meta?.journal_genre ?? ""} (
          {convertToTitleCase(lore.expansion?.name ?? "")})
        </blockquote>
      ) : hasPlace ? (
        <blockquote>{lore.meta?.place_name ?? ""}</blockquote>
      ) : (
        <></>
      )}

      <div
        className="lore-panel flex flex-col"
        dangerouslySetInnerHTML={{
          __html: html,
        }}
      ></div>
    </div>
  );
}
