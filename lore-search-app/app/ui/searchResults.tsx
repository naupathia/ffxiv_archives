import { fetchSearchResults } from "../lib/data";
import ScrollToTopButton from "./scrollToTopButton";
import SearchResultsList from "./searchResultsList";

export default async function SearchResults({
  query,
  currentPage,
  sort = "",
}: {
  query: string;
  currentPage: number;
  sort?: string;
}) {
  const results: LoreEntry[] = await fetchSearchResults(
    query,
    currentPage,
    sort
  );

  return (
    <div className="flex flex-row flex-1">
      <SearchResultsList items={results} query={query} />
      {results && results.length > 0 ? <ScrollToTopButton /> : <></>}
    </div>
  );
}
