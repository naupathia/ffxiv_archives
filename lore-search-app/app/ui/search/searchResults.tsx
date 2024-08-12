import { fetchSearchResults } from "../../lib/data";
import LoreEntryList from "./loreEntryList";

export default async function SearchResults({
  query,
  currentPage,
  sort = "",
}: {
  query: string;
  currentPage: number;
  sort?: string;
}) {
  const results = await fetchSearchResults(query, currentPage, sort);

  return (
    <LoreEntryList items={results} />
  );
}
