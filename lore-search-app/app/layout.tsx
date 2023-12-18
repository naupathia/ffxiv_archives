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
          <div className="flex ml-10">
            <Image
              src="/book.png"
              height={160}
              width={160}
              className="object-scale-down mr-10"
              alt="TEA Logo"
              priority={true}
            ></Image>

            <Image
              src="/title.png"
              height={200}
              width={800}
              className="object-scale-down"
              alt="TEA Tools"
              priority={true}
            ></Image>
          </div>
          {/* <div className="flex w-full items-center justify-between pl-4">
            <h1 className="text-2xl">TEA Tools</h1>
          </div> */}
        </div>

        <div>{children}</div>
      </body>
    </html>
  );
}
