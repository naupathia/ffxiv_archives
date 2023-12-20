import LoreItemCard from "@/app/ui/loreItemCard";
import Link from "next/link";
import { fetchLoreEntry } from "@/app/lib/data";
import { ArrowLeftIcon } from "@heroicons/react/24/solid";

export default async function Page({ params }: { params: { id: string } }) {
  const item = await fetchLoreEntry(params.id);

  return (
    <div>
      <Link href="/search" className="flex items-baseline"><ArrowLeftIcon className="text-white w-3 h-3 mr-2"/>back to search</Link>
      {item ? <LoreItemCard lore={item} isDetailView={true} /> : <></>}
    </div>
  );
}
