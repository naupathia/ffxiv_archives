"use client";

import { createContext, useContext, useState } from "react";

const SearchNavigationContext = createContext<any>(null);

export default function SearchNavigationProvider({ children }: { children: any }) {
  const [navItems, setNavItems] = useState([] as any[]);

  return (
    <SearchNavigationContext.Provider value={{ navItems, setNavItems }}>
      {children}
    </SearchNavigationContext.Provider>
  );
}

export function useSearchNavigation() {
  return useContext(SearchNavigationContext);
}