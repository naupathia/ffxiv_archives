"use client";
import SynonymsProvider from "./ui/synonymsContext";
import SearchTab from "./ui/searchTab";

export default function Page() {
  return (
    <div>
      <SynonymsProvider>
        <SearchTab />
      </SynonymsProvider>
    </div>
  );
}
