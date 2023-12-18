import clsx from "clsx";
import { fetchSearchResults } from "../lib/data";
import LoreItem from "./loreItem";
import { roboto_mono } from "./fonts";

export default async function SearchResults({
  query,
  currentPage,
}: {
  query: string;
  currentPage: number;
}) {
  const results = await fetchSearchResults(query, currentPage);

  return (
    <div className={clsx("mt-6 grid divide-y-2", roboto_mono.className)}>
          {results?.map((item: any) => <LoreItem key={item._id} lore={item} searchText={query}></LoreItem>)}
    </div>
  );
}
