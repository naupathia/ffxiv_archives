import { fetchSearchResults, fetchSynonyms } from "../lib/data";
import ScrollToTopButton from "./scrollToTopButton";
import LoreEntryList from "./loreEntryList";
import SynonymsProvider from "./synonymsContext";

export default async function SearchResults({
  query,
  currentPage,
  sort = "",
}: {
  query: string;
  currentPage: number;
  sort?: string;
}) {
  const searchPromise = fetchSearchResults(query, currentPage, sort);
  const synonymPromise = fetchSynonyms();
  let results: LoreEntry[] = [];
  let synonyms: any = [];
  await Promise.all([searchPromise, synonymPromise]).then((values: any) => {
    results = values[0];
    synonyms = values[1];
  });

  const options = [
    "Try harder next time.",
    "Maybe something less obscure?",
    "Check for typos!",
  ];

  return (
    <div className="flex flex-row flex-1">
        <LoreEntryList
          items={results}
          showBookmark={true}
          synonyms={synonyms}
        />
    </div>
  );
}
