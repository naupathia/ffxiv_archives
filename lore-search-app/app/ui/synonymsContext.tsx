"use client";

import { createContext, useContext, useEffect, useState } from "react";

const SynonymsContext = createContext<any>(null);

export default function SynonymsProvider({
  children,
}: {
  children: any;
}) {
  const [synonyms, setSynonyms] = useState(null);

  useEffect(() => {
    if (!synonyms) {
      const fetchSynonyms = async () => {
        const response = await fetch("/api/synonyms");
        const result = await response.json();
        setSynonyms(result);
      };

      fetchSynonyms().catch((error) => console.log(error));
    }
  }, []);

  return (
    <SynonymsContext.Provider value={{ synonyms, setSynonyms }}>
      {children}
    </SynonymsContext.Provider>
  );
}

export function useSynonyms() {
  return useContext(SynonymsContext);
}
