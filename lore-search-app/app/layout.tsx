import type { Metadata } from "next";
import "./globals.css";
import { roboto } from "./ui/fonts";
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
      <body className={roboto.className}>
        <div className="flex bg-blue-500/10 border-b-2 border-orange-300">
          <Image
            src="/appname.png"
            height={800}
            width={800}
            className="object-scale-down mr-10"
            alt="TEA Logo"
            priority={true}
          ></Image>
        </div>

        <div>{children}</div>
      </body>
    </html>
  );
}
