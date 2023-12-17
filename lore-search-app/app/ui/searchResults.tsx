import { fetchSearchResults } from "../lib/data";
import LoreItem from "./loreItem";

export default async function SearchResults({
  query,
  currentPage,
}: {
  query: string;
  currentPage: number;
}) {
  const results = await fetchSearchResults(query, currentPage);

  return (
    <div className="mt-6 flow-root">
          {results?.map((item) => <LoreItem lore={item}></LoreItem>)}
    </div>
  );
}
