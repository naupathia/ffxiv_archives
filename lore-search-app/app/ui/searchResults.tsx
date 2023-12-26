import { fetchSearchResults } from "../lib/data";
import ScrollToTopButton from "./scrollToTopButton";
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
  const results: LoreEntry[] = await fetchSearchResults(
    query,
    currentPage,
    sort
  );
  const options = [
    "Try harder next time.",
    "Maybe something less obscure?",
    "Check for typos!",
  ];

  return (
    <div className="flex flex-row flex-1">
      <LoreEntryList items={results} showBookmark={true} />
      {results && results.length > 0 ? <ScrollToTopButton /> : <></>}
    </div>
  );
}
