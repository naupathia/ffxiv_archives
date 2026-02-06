"use client";

import { useState } from "react";
import useSWRInfinite from "swr/infinite";
import { fetcher, isEmptyArray } from "@/app/lib/functions";
import SearchBox from "./searchBox";
import LoreEntryList from "./loreEntryList";
import { Button } from "primereact/button";
import { ScrollTop } from "primereact/scrolltop";

export default function SearchPage() {
  const [searchParams, setSearchParams] = useState({
    category: [],
    expansion: [],
    type: [],
    q: "",
    sort: "",
  } as SearchParams);

  const PAGE_SIZE = 500;
  const shouldFetch =
    (searchParams.q != null && searchParams.q != "") ||
    searchParams.category.length > 0 ||
    searchParams.expansion.length > 0 ||
    searchParams.type.length > 0;
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
    if (previousPageData && !previousPageData.documents.length) return null;

    if (!shouldFetch) {
      return null;
    }

    return searchUri + `&page=${pageIndex}`;
  };

  const { data, mutate, size, setSize, isValidating, isLoading } =
    useSWRInfinite(getKey, fetcher);

  const results = data?.flatMap((page) => page.documents) ?? [];
  const currentResults = data?.at(-1)?.documents ?? [];
  const isEmpty = results.length == 0;
  const isReachingEnd = isEmpty || currentResults.length < PAGE_SIZE;
  const isLoadingMore =
    isValidating && data && typeof data[size - 1] === "undefined";
  const totalResults = data?.at(-1).count ?? 0;

  return (
    <div className="flex flex-col gap-2">
      <div className="flex-1">
        <SearchBox setSearchParams={setSearchParams} isSearching={isLoading} />
      </div>

      <p className="p-search-info">
        {isLoading
          ? "searching..."
          : data == null
            ? ""
            : `found ${totalResults} results`}
      </p>

      {isLoading ? <></> : <LoreEntryList items={results} />}

      <div className="flex justify-center">
        <Button
          className="p-2"
          label={
            isReachingEnd
              ? "end of results"
              : isLoadingMore
                ? "loading..."
                : "load more"
          }
          loading={isLoadingMore}
          onClick={() => setSize(size + 1)}
          disabled={isReachingEnd || isLoadingMore}
          visible={!isEmpty}
        />
        <ScrollTop/>
      </div>

    </div>
  );
}
