"use client";

import { createContext, useContext, ReactNode } from "react";
import useSWR from "swr";
import { fetcher } from "@/app/lib/functions";

interface DataType {
  category: string;
  name: string
}

// Define the shape of filter data
interface FiltersData {
  categories: DataType[];
  expansions: string[];
}

// Define the context value shape
interface FiltersContextValue {
  filters: FiltersData | undefined;
  isLoading: boolean;
  error: Error | undefined;
}

// Create the context with a default value
const FiltersContext = createContext<FiltersContextValue | undefined>(undefined);

// Provider component that fetches filters once and provides them to children
export function FiltersProvider({ children }: { children: ReactNode }) {
  const { data, error, isLoading } = useSWR<FiltersData>("/api/filters", fetcher, {
    revalidateOnFocus: false,
    revalidateOnReconnect: false,
    dedupingInterval: 60000,
  });

  return (
    <FiltersContext.Provider
      value={{
        filters: data,
        isLoading,
        error,
      }}
    >
      {children}
    </FiltersContext.Provider>
  );
}

// Custom hook for consuming the filters context
export function useFilters(): FiltersContextValue {
  const context = useContext(FiltersContext);

  if (context === undefined) {
    throw new Error("useFilters must be used within a FiltersProvider");
  }

  return context;
}
