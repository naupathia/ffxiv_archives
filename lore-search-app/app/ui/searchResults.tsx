import { fetchSearchResults, fetchSynonyms } from "../lib/data";
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

  const options = [
    "Try harder next time.",
    "Maybe something less obscure?",
    "Check for typos!",
  ];

  return (
    <LoreEntryList items={results} showBookmark={true} />
  );
}
