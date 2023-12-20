
import { fetchSearchResults } from "../lib/data";
import LoreItemCard from "./loreItemCard";
var _ = require('lodash');

export default async function SearchResults({
  query,
  currentPage,
}: {
  query: string;
  currentPage: number;
}) {
  const results = await fetchSearchResults(query, currentPage);
  const options = [
    "Try harder next time.",
    "Maybe something less obscure?",
    "Check for typos!"
  ]

  return (
    <div className="flex flex-col mt-6">
      {results && results.length > 0 ? (
        results.map((item: any) => (
          <LoreItemCard key={item._id} lore={item} searchText={query} isDetailView={false}></LoreItemCard>
        ))
      ) : query ? (
        <p className="text-white">No lore found. {_.sampleSize(options, 1)[0]}</p>
      ) : (
        <p></p>
      )}
    </div>
  );
}
