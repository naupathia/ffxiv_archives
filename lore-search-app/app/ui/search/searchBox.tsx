"use client";

import { SORT_TYPES } from "@/types/enums";
import { MagnifyingGlassIcon } from "@heroicons/react/24/outline";
import CheckboxGroup from "../checkboxgroup";
import RadioGroup from "../radiogroup";

export default function SearchBox({
  placeholder,
  setSearchParams,
}: {
  placeholder: string;
  setSearchParams: any;
}) {
  const expansions: CheckBoxItem[] = [
    { value: "a realm reborn", label: "A Realm Reborn", isChecked: true },
    { value: "heavensward", label: "Heavensward", isChecked: true },
    { value: "stormblood", label: "Stormblood", isChecked: true },
    { value: "shadowbringers", label: "Shadowbringers", isChecked: true },
    { value: "endwalker", label: "Endwalker", isChecked: true },
    { value: "dawntrail", label: "Dawntrail", isChecked: true },
  ];
  const categories: CheckBoxItem[] = [
    { value: "quest", label: "quest", isChecked: true },
    { value: "cutscene", label: "cutscene", isChecked: true },
    { value: "custom", label: "dialogue", isChecked: true },
    { value: "fate", label: "fate", isChecked: true },
    { value: "item", label: "item", isChecked: true },
    { value: "fish", label: "fish", isChecked: true },
    { value: "card", label: "triple triad card", isChecked: true },
    { value: "mount", label: "mount", isChecked: true },
  ];
  const sortValues: CheckBoxItem[] = [
    { value: SORT_TYPES.RELEVANCE, label: "relevance", isChecked: true },
    { value: SORT_TYPES.CATEGORY, label: "category", isChecked: false },
  ];

  function handleSearch(e: any) {
    e.preventDefault();

    const formData = new FormData(e.target);
    // console.log(formData)
    const params = {
      q: formData.get("q"),
      sort: formData.get("sort"),
      category: formData.getAll("category"),
      expansion: formData.getAll("expansion"),
    };

    setSearchParams(params);
  }

  return (
    <div className="relative flex flex-1 flex-shrink-0">
      <form onSubmit={handleSearch} className="peer block w-full">
        <input type="submit" className="sr-only" name="submit" />
        <label htmlFor="search" className="sr-only">
          Search
        </label>
        <MagnifyingGlassIcon className="absolute left-3 top-2 h-[18px] w-[18px] text-gray-500 peer-focus:text-gray-900" />
        <input
          id="search"
          name="q"
          className="peer block w-full text-black py-2 pl-10 text-sm outline-2 placeholder:text-gray-500"
          placeholder={placeholder}
        />

        <RadioGroup group="sort" items={sortValues} />

        <CheckboxGroup items={categories} group="category" />

        <CheckboxGroup items={expansions} group="expansion" />
      </form>
    </div>
  );
}
