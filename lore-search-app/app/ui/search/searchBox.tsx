"use client";
import { MultiSelect } from "primereact/multiselect";
import { useRef, useState } from "react";
import { InputText } from "primereact/inputtext";
import { FloatLabel } from "primereact/floatlabel";
import { useFilters } from "@/app/context/FiltersContext";
import { convertToTitleCase } from "@/app/lib/functions";
import { Card } from "primereact/card";
import { SORT_TYPES } from "@/types/enums";
import { Checkbox } from "primereact/checkbox";
import { TreeNode } from "primereact/treenode";
import { TreeSelect, TreeSelectSelectionKeysType } from "primereact/treeselect";
import { TreeCheckboxSelectionKeys } from "primereact/tree";

export default function SearchBox({
  setSearchParams,
}: {
  setSearchParams: any;
}) {
  const { filters, isLoading } = useFilters();
  const [selectedCategories, setSelectedCategories] = useState(null);
  const [selectedExpansions, setSelectedExpansions] = useState(null);
  const [q, setQ] = useState("");
  const [useCatgorySort, setUseCategorySort] = useState(false);

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

  function handleSortChange(e: any) {
    const checked = e.target.checked;
    setUseCategorySort(checked);
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
      sort: useCatgorySort ? SORT_TYPES.CATEGORY : "",
    } as SearchParams;

    console.log(params);

    setSearchParams(params);
  }

  return (
    <Card>
      <form onSubmit={submit}>
        <input type="submit" className="sr-only" name="submit" />

        <div className="flex flex-col gap-2">
          <FloatLabel>
            <InputText
              className="p-inputtext-lg h-12 min-w-full p-2"
              id="search"
              name="q"
              value={q}
              onChange={(e) => setQ(e.target.value)}
            />
            <label htmlFor="search">search</label>
          </FloatLabel>

          <div className="flex flex-row gap-2">
            <MultiSelect
              options={
                isLoading ? [] : createOptions(filters?.expansions ?? [])
              }
              value={selectedExpansions}
              onChange={(e) => setSelectedExpansions(e.value)}
              placeholder={isLoading ? "loading..." : "Expansions"}
              display="chip"
              showClear
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
            />

            <div>
              <Checkbox
                name="sort"
                checked={useCatgorySort}
                onChange={handleSortChange}
              />
              <label htmlFor="sort" className="ml-2">
                sort by category
              </label>
            </div>
          </div>
        </div>
      </form>
    </Card>
  );
}
