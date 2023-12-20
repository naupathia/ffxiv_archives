"use client";

import { useSearchParams, usePathname, useRouter } from 'next/navigation';
import { useState } from "react";
// import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';

export default function SearchBox({ placeholder }: { placeholder: string }) {
  const [text, setText] = useState("");
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const { replace } = useRouter();

  function onChange(e: any) {
    setText(e.target.value)
  }

  function handleSearch(e: any) {
    e.preventDefault();
    console.log(text);
    const params = new URLSearchParams(searchParams);
    if (text) {
      params.set("query", text);
    } else {
      params.delete("query");
    }
    replace(`${pathname}?${params.toString()}`);
  }

  return (
    <div className="relative flex flex-1 flex-shrink-0">
      <form onSubmit={handleSearch} className='peer block w-full'>
        <label htmlFor="search" className="sr-only">
          Search
        </label>
        <input
          id="search"
          name="search"
          className="peer block w-full text-black py-[9px] pl-10 text-sm outline-2 placeholder:text-gray-500"
          placeholder={placeholder}
          onChange={onChange}
          defaultValue={searchParams.get('query')?.toString()}
        />
        <input type="submit" className='sr-only' name="submit"/>
        {/* <MagnifyingGlassIcon className="absolute left-3 top-1/2 h-[18px] w-[18px] -translate-y-1/2 text-gray-500 peer-focus:text-gray-900" /> */}
      </form>
    </div>
  );
}
