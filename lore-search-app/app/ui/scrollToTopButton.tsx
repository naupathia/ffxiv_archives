"use client";

import { ArrowUpIcon } from "@heroicons/react/24/solid";
import { useEffect, useState } from "react";

export default function ScrollToTopButton() {
  const [isVisible, setIsVisible] = useState(false);

  const isBrowser = () => typeof window !== "undefined"; //The approach recommended by Next.js

  function scrollToTop() {
    if (!isBrowser()) return;
    window.scrollTo({ top: 0, behavior: "auto" });
  }
  
  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > window.innerHeight / 2) {
        setIsVisible(true);
      } else {
        setIsVisible(false);
      }
    };

    window.addEventListener("scroll", handleScroll);

    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  return (
    <div className="flex flex-col items-center justify-center p-2">
      <button
        className="scrollToTopBtn"
        onClick={scrollToTop}
        title="to top"
        style={{ display: isVisible ? "block" : "none" }}
      >
        <div className="flex flex-col items-center justify-center">
          <ArrowUpIcon className="h-8 w-8" />
        </div>
      </button>
    </div>
  );
}
