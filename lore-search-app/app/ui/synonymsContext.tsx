"use client";

import { createContext, useContext, useState } from "react";

const SynonymsContext = createContext<any>(null);

export default function SynonymsProvider({ children }: { children: any }) {
  const [synonyms, setSynonyms] = useState([] as any[]);

  return (
    <SynonymsContext.Provider value={{ synonyms, setSynonyms }}>
      {children}
    </SynonymsContext.Provider>
  );
}

export function useSynonyms() {
  return useContext(SynonymsContext);
}
