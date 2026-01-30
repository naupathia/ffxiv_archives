"use client";
import { MultiSelect } from "primereact/multiselect";
import { useState } from "react";
import { InputText } from "primereact/inputtext";
import { useFilters } from "@/app/ui/context/FiltersContext";
import { convertToTitleCase } from "@/app/lib/functions";
import { Card } from "primereact/card";
import { TreeNode } from "primereact/treenode";
import { TreeSelect } from "primereact/treeselect";
import { Button } from "primereact/button";
import { Dropdown } from "primereact/dropdown";

export default function SearchBox({
  setSearchParams,
  isSearching,
}: {
  setSearchParams: any;
  isSearching: boolean;
}) {
  const { filters, isLoading } = useFilters();
  const [selectedCategories, setSelectedCategories] = useState(null);
  const [selectedExpansions, setSelectedExpansions] = useState(null);
  const [sort, setSort] = useState("");
  const [q, setQ] = useState("");

  const sortOptions = [
    { label: "Relevance", value: "" },
    { label: "Category", value: "category" },
    { label: "Name", value: "name" },
  ];

  const categoryKey = "datatype.category:";
  const typeKey = "datatype.name:";

  function createOptions(values: string[]) {
    if (!values || values.length == 0) {
      return [];
    }
    return values
      .filter((v: string) => v != null)
      .map((v: string) => {
        return {
          label: convertToTitleCase(v),
          value: v,
        };
      });
  }

  function createTreeNodes(values: { category: string; name: string }[]) {
    let nodes = new Map<string, TreeNode[]>();

    values.forEach((element) => {
      const id = `${typeKey}${element.name}`;
      const childNode = {
        id: id,
        key: id,
        label: convertToTitleCase(element.name),
      } as TreeNode;

      if (nodes.has(element.category)) {
        nodes.get(element.category)?.push(childNode);
      } else {
        nodes.set(element.category, [childNode]);
      }
    });

    return nodes
      .entries()
      .map((value, key) => {
        const id = `${categoryKey}${value[0]}`;
        return {
          children: value[1],
          id: id,
          key: id,
          label: convertToTitleCase(value[0]),
        } as TreeNode;
      })
      .toArray();
  }

  function submit(e: any) {
    e.preventDefault();
    handleSearch();
  }

  function getSelectedCategories() {
    if (selectedCategories == null) {
      return [];
    }

    const results: string[] = [];
    Object.keys(selectedCategories).forEach((key) => {
      if (selectedCategories[key] && key.startsWith(categoryKey)) {
        results.push(key.replace(categoryKey, ""));
      }
    });

    return results;
  }

  function getSelectedTypes() {
    if (selectedCategories == null) {
      return [];
    }

    const results: string[] = [];
    Object.keys(selectedCategories).forEach((key) => {
      if (selectedCategories[key] && key.startsWith(typeKey)) {
        results.push(key.replace(typeKey, ""));
      }
    });

    return results;
  }

  function handleSearch() {
    console.log(selectedCategories);
    const params = {
      q: q,
      category: getSelectedCategories(),
      expansion: selectedExpansions ?? [],
      type: getSelectedTypes(),
      sort: sort,
    } as SearchParams;

    console.log(params);

    setSearchParams(params);
  }

  return (
    <Card>
      <form onSubmit={submit}>
        <input type="submit" className="sr-only" name="submit" />

        <div className="flex flex-col gap-2">
          <div className="flex flex-row gap-2">
            <div className="grow">
              <InputText
                className="input-search p-inputtext-lg min-w-full h-12 p-2"
                id="search"
                name="q"
                value={q}
                onChange={(e) => setQ(e.target.value)}
                autoFocus
                placeholder="enter search text"
              />
            </div>
            <Button
              label="search"
              onClick={handleSearch}
              raised={true}
              loading={isSearching}
              className="basis-32"
            />
          </div>

          <div className="flex flex-row gap-2 items-center">
            <MultiSelect
              options={
                isLoading ? [] : createOptions(filters?.expansions ?? [])
              }
              value={selectedExpansions}
              onChange={(e) => setSelectedExpansions(e.value)}
              placeholder={isLoading ? "loading..." : "Expansions"}
              showClear
              maxSelectedLabels={2}
              className="basis-64"
            />
            <TreeSelect
              options={
                isLoading ? [] : createTreeNodes(filters?.categories ?? [])
              }
              value={selectedCategories}
              selectionMode="multiple"
              // @ts-ignore
              onChange={(e) => setSelectedCategories(e.value)}
              placeholder={isLoading ? "loading..." : "Categories"}
              filter
              metaKeySelection={false}
              showClear
              className="grow"
            />

            <label htmlFor="sort">sort by</label>
            <Dropdown
              options={sortOptions}
              id="sort"
              name="sort"
              value={sort}
              optionValue="value"
              onChange={(e) => setSort(e.value)}
              placeholder="Sort by"
              className="basis-60"
            />
          </div>
        </div>
      </form>
    </Card>
  );
}
