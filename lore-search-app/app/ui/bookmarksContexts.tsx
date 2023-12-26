"use client";

import {
  Dispatch,
  createContext,
  useContext,
  useEffect,
  useReducer,
} from "react";
import { fetchManyLoreEntries } from "../lib/data";

const BookmarksContext = createContext<Bookmark[]>([]);
const BookmarksDispatchContext = createContext<Dispatch<any>>(
  (() => undefined) as Dispatch<any>
);

export default function BookmarksProvider({ children }: { children: any }) {
  const [bookmarks, dispatch] = useReducer(bookmarksReducer, []);

  useEffect(() => {
    const savedBookmarks = JSON.parse(localStorage.bookmarks ?? "[]");
    dispatch({
      type: "set",
      value: savedBookmarks,
    });
  }, []);

  return (
    <BookmarksContext.Provider value={bookmarks}>
      <BookmarksDispatchContext.Provider value={dispatch}>
        {children}
      </BookmarksDispatchContext.Provider>
    </BookmarksContext.Provider>
  );
}

export function useBookmarks() {
  return useContext(BookmarksContext);
}

export function useBookmarksDispatch() {
  return useContext(BookmarksDispatchContext);
}

export function bookmarksReducer(bookmarks: Bookmark[], action: any) {
  // console.log(action);
  switch (action.type) {
    case "add": {
      if (!containsLoreEntry(bookmarks, action.id)) {
        const results = [
          ...bookmarks,
          {
            id: action.id,
            name: action.name,
            datatype: action.datatype,
          },
        ];
        localStorage.setItem("bookmarks", JSON.stringify(results));
        return results;
      }
      return bookmarks;
    }
    case "delete": {
      const results = bookmarks.filter((t: Bookmark) => t.id !== action.id);
      localStorage.setItem("bookmarks", JSON.stringify(results));
      return results;
    }
    case "set": {
      localStorage.setItem("bookmarks", JSON.stringify(action.value));
      return action.value;
    }
    case "clear": {
      localStorage.removeItem("bookmarks");
      return [];
    }
    default: {
      throw Error("Unknown action: " + action.type);
    }
  }
}

export function containsLoreEntry(bookmarks: Bookmark[], id: string) {
  return bookmarks.some((x) => x.id === id);
}
