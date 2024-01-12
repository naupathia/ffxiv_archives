import type { Metadata } from "next";
import "./globals.css";
import Image from "next/image";
import Link from "next/link";
import BookmarksProvider from "./ui/bookmarksContexts";
import SynonymsProvider from "./ui/synonymsContext";
import { HeartIcon } from "@heroicons/react/24/solid";

export const metadata: Metadata = {
  title: "TEA Tools",
  description: "Search for FFXIV lore",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <div>
          <div className="flex">
            <div className="flex-1">
              <Image
                src="/appname.png"
                height={600}
                width={600}
                className="object-scale-down p-2"
                alt="TEA Logo"
                priority={true}
              ></Image>
            </div>

            <div className="flex items-end m-4">
              <a
                className="flex flex-row text-nowrap"
                href="https://patreon.com/eorzeanarchives?utm_medium=clipboard_copy&utm_source=copyLink&utm_campaign=creatorshare_creator&utm_content=join_link"
                target="blank"
              >
                Support
                <HeartIcon className="w-6 pr-1 pl-1" />
                Us
              </a>
            </div>
          </div>

          <div className="tab-header bg-blue-500/10">
            <Link className="tab basis-1" href={`/search`}>
              SEARCH
            </Link>
            <Link className="tab basis-1" href={`/bookmarks`}>
              BOOKMARKS
            </Link>
          </div>
          <BookmarksProvider>
            <SynonymsProvider>{children}</SynonymsProvider>
          </BookmarksProvider>
        </div>
      </body>
    </html>
  );
}
