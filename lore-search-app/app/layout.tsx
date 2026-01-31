import type { Metadata } from "next";
// import "primereact/resources/themes/lara-dark-blue/theme.css";
import "primereact/resources/primereact.min.css";
import "primeicons/primeicons.css";
import "./globals.css";
import Image from "next/image";
import { HeartIcon } from "@heroicons/react/24/solid";
import { FiltersProvider } from "@/app/ui/context/FiltersContext";
import { Source_Sans_3 } from "next/font/google";
import DiscordLink from "./ui/discordLink";
import Link from "next/link";
import clsx from "clsx";


const sourcesans3 = Source_Sans_3({
  subsets: ['latin'],
});
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
    <html lang="en" suppressHydrationWarning>
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      </head>
      <body className={sourcesans3.className}>
        <FiltersProvider>
          <div>
            {/* TEA Tools header */}
            <div className="flex site-title">
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
              <div className="a-header flex items-end m-4 gap-4">
                <Link href="/faq">FAQ</Link>
                <DiscordLink/>
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

            {/* <PrimeReactProviders> */}
            {/* <PrimeReactThemeSync> */}
            {/* Children */}
            <div className="min-h-screen max-w-full">
              <main className="">{children}</main>
            </div>
            {/* </PrimeReactThemeSync> */}
            {/* </PrimeReactProviders> */}

            {/* end */}
          </div>
        </FiltersProvider>
      </body>
    </html>
  );
}
