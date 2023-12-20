"use client";

import { ArrowUpIcon } from "@heroicons/react/24/solid";

export default function ScrollToTopButton() {
  return (
    <button className="fixed bottom-0 right-0 pb-4 pr-4" onClick={scrollToTop} title="to top">
      <ArrowUpIcon className="h-8 w-8" />
    </button>
  );
}

const isBrowser = () => typeof window !== "undefined"; //The approach recommended by Next.js

function scrollToTop() {
  if (!isBrowser()) return;
  window.scrollTo({ top: 0, behavior: "auto" });
}
