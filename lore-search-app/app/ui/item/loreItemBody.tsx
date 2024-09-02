import QuestItemMetadata from "./questItemMetadata";

export default function LoreItemBody({
  text,
  lore,
}: {
  text: string;
  lore: LoreEntry;
}) {
  const metadata =
    lore.datatype == "quest"
      ? {
          expansion: lore.expansion || "",
          placeName: lore.meta?.place_name || "",
          journalGenre: lore.meta?.journal_genre || "",
          issuer: lore.meta?.issuer || "",
        }
      : null;

  return (
    <div className="lore-item-body">
      {metadata ? <QuestItemMetadata data={metadata} /> : <></>}

      <p
        className="whitespace-pre-wrap"
        dangerouslySetInnerHTML={{
          __html: text,
        }}
      ></p>
    </div>
  );
}
