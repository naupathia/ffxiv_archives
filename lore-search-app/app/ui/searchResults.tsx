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
    <div className="flex flex-col mt-6">
          {results?.map((item: any) => <LoreItem key={item._id} lore={item} searchText={query}></LoreItem>)}
    </div>
  );
}
