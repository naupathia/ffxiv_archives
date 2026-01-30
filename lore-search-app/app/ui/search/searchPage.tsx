"use client";

import { useState } from "react";
import useSWRInfinite from "swr/infinite";
import clsx from "clsx";
import { fetcher, isEmptyArray } from "@/app/lib/functions";
import SearchBox from "./searchBox";
import LoreEntryList from "./loreEntryList";
import ScrollToTopButton from "../scrollToTopButton";

export default function SearchPage() {
  const [searchParams, setSearchParams] = useState({
    category: [],
    expansion: [],
    type: [],
    q: "",
    sort: "",
  } as SearchParams);
  const PAGE_SIZE = 500;
  const shouldFetch = searchParams.q != null && searchParams.q != "";
  const categoryList = !isEmptyArray(searchParams.category)
    ? "&category=" + searchParams.category.join("&category=")
    : "";
  const expansionList = !isEmptyArray(searchParams.expansion)
    ? "&expansion=" + searchParams.expansion.join("&expansion=")
    : "";
  const typeList = !isEmptyArray(searchParams.type)
    ? "&type=" + searchParams.type.join("&type=")
    : "";
  const searchUri = encodeURI(
    `/api/search?q=${searchParams.q}&sort=${searchParams.sort}${categoryList}${expansionList}${typeList}`,
  );
  console.log(searchUri);

  const getKey = (pageIndex: number, previousPageData: any) => {
    // If no previous page data or no items in the previous page, it's the last page
    if (previousPageData && !previousPageData.items.length) return null;

    if (!shouldFetch) {
      return null;
    }

    return searchUri + `&page=${pageIndex + 1}`;
  };

  const { data, mutate, size, setSize, isValidating, isLoading } =
    useSWRInfinite(getKey, fetcher);

  const results = data?.flatMap((page) => page.documents) ?? [];
  const currentResults = data?.at(-1)?.documents ?? [];
  const isEmpty = results.length == 0;
  const isReachingEnd = isEmpty || currentResults.length < PAGE_SIZE;
  const totalResults = data?.at(-1).count ?? 0;

  return (
    <div className="flex flex-col">
      <div className="flex-1">
        <SearchBox setSearchParams={setSearchParams} isSearching={isLoading} />

        <p className="p-search-info">
          {isLoading
            ? "searching..."
            : data == null
              ? ""
              : `found ${totalResults} results`}
        </p>
      </div>

      {isLoading ? <></> : <LoreEntryList items={results} />}

      <div className="flex flex-col mt-8">
        <button
          className={clsx(isEmpty ? "hidden" : "")}
          disabled={isLoading || isReachingEnd}
          onClick={() => setSize(size + 1)}
        >
          {isLoading
            ? "loading..."
            : isReachingEnd
              ? "end of results"
              : "load more"}
        </button>
      </div>

      <ScrollToTopButton />
    </div>
  );
}
