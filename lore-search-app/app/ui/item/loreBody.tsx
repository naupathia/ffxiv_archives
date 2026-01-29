import { convertToTitleCase } from "@/app/lib/functions";

export default function LoreBody({
  text,
  lore,
}: {
  text: string;
  lore: LoreEntry;
}) {
  const metadata =
    lore.datatype == "quest"
      ? {
          expansion: lore.expansion?.name || "",
          placeName: lore.meta?.place_name || "",
          journalGenre: lore.meta?.journal_genre || "",
          issuer: lore.meta?.issuer || "",
        }
      : null;

  return (
    <div className="flex flex-col items-start gap-y-2">
      {metadata ? (
        <blockquote>
            {metadata.issuer} ({metadata.placeName})<br/>
            {metadata.journalGenre} ({convertToTitleCase(metadata.expansion)})
        </blockquote>
      ) : (
        <></>
      )}

      <div
        dangerouslySetInnerHTML={{
          __html: text,
        }}
      ></div>
    </div>
  );
}
