import { fetchManyLoreEntries } from "@/app/lib/data";
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

      <div className="flex flex-col space-y-8 mt-6">
        <LoreEntryList items={items} />
      </div>
    </div>
  );
}
