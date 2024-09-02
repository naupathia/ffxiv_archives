import type { Metadata } from "next";
import "./globals.css";
import Image from "next/image";
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
          {/* TEA Tools header */}
          <div className="flex bg-blue-500/10 border-b-2 border-orange-300">
            {/* Image as title */}
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

            {/* Patreon support link */}
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

          {/* Children */}
          <div>
            <main className="min-h-screen min-w-full p-8">{children}</main>
          </div>

          {/* end */}
        </div>
      </body>
    </html>
  );
}
