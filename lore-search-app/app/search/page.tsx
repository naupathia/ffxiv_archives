"use client";

import { useEffect, useState } from "react";
import useSWRInfinite from "swr/infinite";
import clsx from "clsx";
import { useSearchParams } from "next/navigation";
import SearchBox from "../ui/search/searchBox";
import LoreEntryList from "../ui/search/loreEntryList";
import ScrollToTopButton from "../ui/scrollToTopButton";
import { fetcher } from "../lib/functions";

export default function Page() {
  const urlParams = useSearchParams();
  const [searchParams, setSearchParams] = useState({
    category: [],
    expansion: [],
    page: 1,
  } as SearchParams);
  const PAGE_SIZE = 100;

  useEffect(() => {
    if (urlParams && urlParams.get("q")) {
      setSearchParams({
        q: urlParams.get("q")?.toString(),
        category: [],
        expansion: [],
        page: 1,
      });
    }
  }, [urlParams]);

  const shouldFetch = searchParams.q != null && searchParams.q != "";
  const categoryList =
    searchParams.category.length > 0
      ? "&category=" + searchParams.category.join("&category=")
      : "";
  const expansionList =
    searchParams.expansion.length > 0
      ? "&expansion=" + searchParams.expansion.join("&expansion=")
      : "";
  const searchUri = encodeURI(
    `/api/search?q=${searchParams.q}&sort=${searchParams.sort}${categoryList}${expansionList}`
  );
  // console.log(shouldFetch);

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
      <div className="p-8 flex-1 ">
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
