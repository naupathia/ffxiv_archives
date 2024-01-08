import type { Metadata } from "next";
import "./globals.css";
import Image from "next/image";

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
          <div className="flex bg-blue-500/10 border-b-2 border-orange-300">
            <div className="flex-1">
              <Image
                src="/appname.png"
                height={600}
                width={600}
                className="object-scale-down"
                alt="TEA Logo"
                priority={true}
              ></Image>
            </div>

            <div className="flex items-end m-4">
              <a className="" href="https://patreon.com/eorzeanarchives?utm_medium=clipboard_copy&utm_source=copyLink&utm_campaign=creatorshare_creator&utm_content=join_link">
                Support Us
              </a>
            </div>
          </div>

          <div>{children}</div>
        </div>
      </body>
    </html>
  );
}
