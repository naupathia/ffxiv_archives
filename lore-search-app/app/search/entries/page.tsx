import LoreItemCard from "@/app/ui/loreItemCard";
import { fetchManyLoreEntries } from "@/app/lib/data";
import Link from "next/link";
import { ArrowLeftIcon } from "@heroicons/react/24/solid";
import LoreEntryList from "@/app/ui/loreEntryList";

export default async function Page({
  searchParams,
}: {
  searchParams: { id: string[]; q?: string };
}) {
  const ids = Array.isArray(searchParams.id)
    ? searchParams.id
    : [searchParams.id];
  const items = await fetchManyLoreEntries(ids);
  return (
    <div className="p-8">
      <Link
        href={searchParams.q ? `/search?q=${searchParams.q}` : `/search`}
        className="flex items-baseline"
      >
        <ArrowLeftIcon className="text-white w-3 h-3 mr-2" />
        back to search
      </Link>

      <div className="flex flex-col space-y-8 mt-6">
        <LoreEntryList items={items} />
      </div>
    </div>
  );
}
