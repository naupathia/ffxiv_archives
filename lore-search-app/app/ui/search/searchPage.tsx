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
  // if (shouldFetch) {
  //   console.log(searchParams);
  // }
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
  const isLoadingMore =
    isLoading || (size > 0 && data && typeof data[size - 1] === "undefined");
  const isEmpty = data?.[0]?.length === 0;
  const isReachingEnd =
    isEmpty || (data && data[data.length - 1]?.length < PAGE_SIZE);
  const isRefreshing = isValidating && data && data.length === size;
  const totalResults = data?.at(-1).count ?? 0;

  return (
    <div className="flex flex-col">
      <div className="flex-1">
        <SearchBox setSearchParams={setSearchParams} isSearching={isLoading}/>

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
          className={clsx(data && data.length > 0 ? "" : "hidden")}
          disabled={isLoadingMore || isReachingEnd}
          onClick={() => setSize(size + 1)}
        >
          {isLoadingMore
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
