import type { Metadata } from "next";
import "./globals.css";
import { roboto } from "../types/fonts";
import Image from "next/image";
import ScrollToTopButton from "./ui/scrollToTopButton";

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
            <Image
              src="/appname.png"
              height={600}
              width={600}
              className="object-scale-down"
              alt="TEA Logo"
              priority={true}
            ></Image>
          </div>

          <div>{children}</div>

          <ScrollToTopButton />
        </div>
      </body>
    </html>
  );
}
