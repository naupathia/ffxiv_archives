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
    page: 1,
  } as SearchParams);
  const PAGE_SIZE = 100;

  const shouldFetch = searchParams.q != null && searchParams.q != "";
  const categoryList = !isEmptyArray(searchParams.category)
    ? "&category=" + searchParams.category.join("&category=")
    : "";
  const expansionList = !isEmptyArray(searchParams.expansion)
    ? "&expansion=" + searchParams.expansion.join("&expansion=")
    : "";
  const searchUri = encodeURI(
    `/api/search?q=${searchParams.q}&sort=${searchParams.sort}${categoryList}${expansionList}`
  );
  // if (shouldFetch) {
  //   console.log(searchParams);
  // }

  const { data, mutate, size, setSize, isValidating, isLoading } =
    useSWRInfinite(
      (page) => shouldFetch && searchUri + `&page=${page + 1}`,
      fetcher
    );

  const results = data ? [].concat(...data) : [];
  const isLoadingMore =
    isLoading || (size > 0 && data && typeof data[size - 1] === "undefined");
  const isEmpty = data?.[0]?.length === 0;
  const isReachingEnd =
    isEmpty || (data && data[data.length - 1]?.length < PAGE_SIZE);
  const isRefreshing = isValidating && data && data.length === size;

  return (
    <div className="flex flex-col">
      <div className="flex-1 ">
        <div className="flex items-center justify-between gap-2 min-w-full">
          <SearchBox
            placeholder="search..."
            setSearchParams={setSearchParams}
          />
        </div>

        <div className="mt-6">
          {isLoading ? (
            Loading()
          ) : (
            <LoreEntryList items={results} searchText={searchParams.q} />
          )}
        </div>
      </div>

      <div className="flex flex-col items-center justify-between pb-20">
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

function Loading() {
  return <p className="mt-6">searching...</p>;
}
