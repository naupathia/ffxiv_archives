"use client";
import { useState } from "react";
import BookmarksProvider from "./ui/bookmarksContexts";
import SynonymsProvider from "./ui/synonymsContext";
import Link from "next/link";
import SearchTab from "./ui/searchTab";
import BookmarksTab from "./ui/bookmarksTab";
import clsx from "clsx";

export default function Page() {
  const [tab, setTab] = useState("SEARCH");

  return (
    <div>
      <BookmarksProvider>
        <div className="tab-header bg-blue-500/10">
          <button
            className="tab basis-1"
            onClick={() => setTab("SEARCH")}
          >
            SEARCH
          </button>
          <button
            className="tab basis-1"
            onClick={() => setTab("BOOKMARKS")}
          >
            BOOKMARKS
          </button>
        </div>

        <div className="tab-container">
          {/* search tab */}
          <div className={clsx(tab == "SEARCH" ? "" : "hidden")}>
            <SynonymsProvider>
              <SearchTab />
            </SynonymsProvider>
          </div>
          {/* bookmarks tab */}
          <div className={clsx(tab == "BOOKMARKS" ? "" : "hidden")}>
            <BookmarksTab />
          </div>
        </div>
      </BookmarksProvider>
    </div>
  );
}
