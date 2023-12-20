import LoreItemCard from "@/app/ui/loreItemCard";
import Link from "next/link";
import { ArrowLeftIcon } from "@heroicons/react/24/solid";
import { fetchManyLoreEntries } from "@/app/lib/data";

export default async function Page({
  searchParams,
}: {
  searchParams: { id: string[], q?: string };
}) {
  const ids = Array.isArray(searchParams.id)
    ? searchParams.id
    : [searchParams.id];
  const items = await fetchManyLoreEntries(ids);

  return (
    <div>
      <Link href={searchParams.q ? `/search?q=${searchParams.q}` : `/search`} className="flex items-baseline">
        <ArrowLeftIcon className="text-white w-3 h-3 mr-2" />
        back to search
      </Link>
      {items.map((item: LoreEntry) => (
        <LoreItemCard lore={item} key={item._id} />
      ))}
    </div>
  );
}
