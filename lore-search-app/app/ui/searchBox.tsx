"use client";

import { SORT_TYPES } from "@/types/enums";
import { useSearchParams, usePathname, useRouter } from "next/navigation";
import { MagnifyingGlassIcon } from "@heroicons/react/24/outline";

export default function SearchBox({ placeholder }: { placeholder: string }) {
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const { replace } = useRouter();


  function handleSearch(e: any) {
    e.preventDefault();

    
    const formData = new FormData(e.target);
    const asString = new URLSearchParams(formData as any).toString();

    console.log(asString);
    replace(`${pathname}?${asString}`);
  }

  return (
    <div className="relative flex flex-1 flex-shrink-0">
      <form onSubmit={handleSearch} className="peer block w-full">
        <label htmlFor="search" className="sr-only">
          Search
        </label>
        <MagnifyingGlassIcon className="absolute left-3 top-2 h-[18px] w-[18px] text-gray-500 peer-focus:text-gray-900" />
        <input
          id="search"
          name="q"
          className="peer block w-full text-black py-2 pl-10 text-sm outline-2 placeholder:text-gray-500"
          placeholder={placeholder}
          defaultValue={searchParams.get("q")?.toString()}
        />

        <fieldset>
          <div className="flex flex-row space-x-2 mt-2">
            <legend>sort by</legend>
            <input
              type="radio"
              id="sortRelevance"
              name="sort"
              value={SORT_TYPES.RELEVANCE}
              defaultChecked
            />
            <label htmlFor="sortRelevance">relevance</label>

            <input
              type="radio"
              id="sortCategory"
              name="sort"
              value={SORT_TYPES.CATEGORY}
            />
            <label htmlFor="sortCategory">category</label>
          </div>
        </fieldset>

        <input type="submit" className="sr-only" name="submit" />
      </form>
    </div>
  );
}
