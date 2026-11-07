"use client";

import { FocusEvent, FormEvent, PointerEvent, useMemo, useState } from "react";
import { useFilters } from "@/app/ui/context/FiltersContext";
import { convertToTitleCase } from "@/app/lib/functions";

export default function SearchBox({
  setSearchParams,
  isSearching,
}: {
  setSearchParams: (params: SearchParams) => void;
  isSearching: boolean;
}) {
  const { filters, isLoading } = useFilters();
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
  const [selectedTypes, setSelectedTypes] = useState<string[]>([]);
  const [selectedExpansions, setSelectedExpansions] = useState<string[]>([]);
  const [sort, setSort] = useState("");
  const [q, setQ] = useState("");
  const [categoryQuery, setCategoryQuery] = useState("");

  const categories = useMemo(() => {
    const groups = new Map<string, string[]>();

    for (const { category, name } of filters?.categories ?? []) {
      if (!category || !name) continue;
      const names = groups.get(category) ?? [];
      if (!names.includes(name)) names.push(name);
      groups.set(category, names);
    }

    return [...groups.entries()].sort(([a], [b]) => a.localeCompare(b));
  }, [filters?.categories]);

  const visibleCategories = categories.filter(([category, types]) =>
    `${category} ${types.join(" ")}`
      .toLowerCase()
      .includes(categoryQuery.trim().toLowerCase()),
  );
  const selectedFilterCount =
    selectedCategories.length +
    selectedTypes.filter(
      (type) =>
        !categories.some(
          ([category, types]) =>
            selectedCategories.includes(category) && types.includes(type),
        ),
    ).length;
  const hasSelections =
    selectedCategories.length > 0 ||
    selectedTypes.length > 0 ||
    selectedExpansions.length > 0 ||
    sort !== "";

  function toggleCategory(category: string, types: string[], checked: boolean) {
    setSelectedCategories((current) =>
      checked
        ? [...new Set([...current, category])]
        : current.filter((value) => value !== category),
    );
    setSelectedTypes((current) =>
      checked
        ? [...new Set([...current, ...types])]
        : current.filter((value) => !types.includes(value)),
    );
  }

  function toggleType(category: string, type: string, types: string[], checked: boolean) {
    const next = checked
      ? [...new Set([...selectedTypes, type])]
      : selectedTypes.filter((value) => value !== type);
    setSelectedTypes(next);
    const allSelected = types.every((value) => next.includes(value));
    setSelectedCategories((selected) =>
      allSelected
        ? [...new Set([...selected, category])]
        : selected.filter((value) => value !== category),
    );
  }

  function toggleExpansion(expansion: string, checked: boolean) {
    setSelectedExpansions((current) =>
      checked
        ? [...new Set([...current, expansion])]
        : current.filter((value) => value !== expansion),
    );
  }

  function clearSelections() {
    setSelectedCategories([]);
    setSelectedTypes([]);
    setSelectedExpansions([]);
    setSort("");
  }

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSearchParams({
      q,
      category: selectedCategories,
      expansion: selectedExpansions,
      type: selectedTypes,
      sort,
    });
  }

  function closeFilterOnBlur(event: FocusEvent<HTMLDetailsElement>) {
    const nextTarget = event.relatedTarget;
    if (nextTarget instanceof Node && !event.currentTarget.contains(nextTarget)) {
      event.currentTarget.open = false;
    }
  }

  function closeOtherFiltersOnPointerDown(event: PointerEvent<HTMLFormElement>) {
    const target = event.target;
    if (!(target instanceof Node)) return;

    event.currentTarget
      .querySelectorAll<HTMLDetailsElement>(".filter-picker[open]")
      .forEach((filter) => {
        if (!filter.contains(target)) filter.open = false;
      });
  }

  return (
    <form
      className="search-box"
      onSubmit={submit}
      onPointerDownCapture={closeOtherFiltersOnPointerDown}
    >
      <div className="search-row">
        <input
          className="search-input"
          id="search"
          name="q"
          type="search"
          value={q}
          onChange={(event) => setQ(event.target.value)}
          autoFocus
          placeholder="enter search text"
        />
        <button className="primary-button search-submit" type="submit" disabled={isSearching}>
          {isSearching ? "searching..." : "search"}
        </button>
      </div>

      <div className="search-filters">
        <details className="filter-picker" onBlur={closeFilterOnBlur}>
          <summary>
            {isLoading
              ? "loading..."
              : selectedExpansions.length
                ? `Expansions (${selectedExpansions.length})`
                : "Expansions"}
          </summary>
          <div className="filter-options">
            <p className="filter-help">
              Applies to quest and cutscene data types.
            </p>
            {(filters?.expansions ?? []).map((expansion) => (
              <label className="filter-option" key={expansion}>
                <input
                  type="checkbox"
                  checked={selectedExpansions.includes(expansion)}
                  onChange={(event) => toggleExpansion(expansion, event.target.checked)}
                />
                <span>{convertToTitleCase(expansion)}</span>
              </label>
            ))}
            {!isLoading && !filters?.expansions?.length && (
              <p className="filter-help">No expansions available.</p>
            )}
          </div>
        </details>

        <details
          className="filter-picker categories-picker"
          onBlur={closeFilterOnBlur}
        >
          <summary>
            {isLoading
              ? "loading..."
              : selectedFilterCount
                ? `Categories (${selectedFilterCount})`
                : "Categories"}
          </summary>
          <div className="filter-options category-options">
            <input
              className="category-filter-input"
              type="search"
              aria-label="Filter categories"
              placeholder="Filter categories"
              value={categoryQuery}
              onChange={(event) => setCategoryQuery(event.target.value)}
            />
            {visibleCategories.map(([category, types]) => (
              <fieldset className="category-group" key={category}>
                <legend>
                  <label className="filter-option category-label">
                    <input
                      type="checkbox"
                      checked={selectedCategories.includes(category)}
                      onChange={(event) =>
                        toggleCategory(category, types, event.target.checked)
                      }
                    />
                    <span>{convertToTitleCase(category)}</span>
                  </label>
                </legend>
                {types.map((type) => (
                  <label className="filter-option category-child" key={type}>
                    <input
                      type="checkbox"
                      checked={selectedTypes.includes(type)}
                      onChange={(event) =>
                        toggleType(category, type, types, event.target.checked)
                      }
                    />
                    <span>{convertToTitleCase(type)}</span>
                  </label>
                ))}
              </fieldset>
            ))}
            {!isLoading && visibleCategories.length === 0 && (
              <p className="filter-help">No matching categories.</p>
            )}
          </div>
        </details>

        <label className="sort-label" htmlFor="sort">sort by</label>
        <select
          className="sort-select"
          id="sort"
          name="sort"
          value={sort}
          onChange={(event) => setSort(event.target.value)}
          title="How the results should be sorted. Default is relevance based on term matching."
        >
          <option value="">Relevance</option>
          <option value="category">Category</option>
          <option value="name">Name</option>
          <option value="row_id">Chronological</option>
        </select>
        {hasSelections && (
          <button
            className="clear-filters-button"
            type="button"
            onClick={clearSelections}
          >
            Clear all
          </button>
        )}
      </div>
    </form>
  );
}
