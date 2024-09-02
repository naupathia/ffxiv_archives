export default function QuestItemMetadata({
  data,
}: {
  data: {
    issuer: string;
    placeName: string;
    journalGenre: string;
    expansion: string;
  };
}) {
  return (
    <div className="flex mb-4">
      <div className="bg-gray-200/20 p-2">
        <p>
          {data.issuer} ({data.placeName})
        </p>
        <p>
          {data.journalGenre} ({data.expansion})
        </p>
      </div>
    </div>
  );
}
