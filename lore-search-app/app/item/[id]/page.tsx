import { fetchLoreEntry } from "@/app/lib/data";
import { notFound } from "next/navigation";
import ItemPage from "../../ui/item/itemPage";

export default async function Page({ params }: { params: { id: string } }) {
  const { id } = await params;
  const data = await fetchLoreEntry(id);

  if (!data) {
    notFound();
  }

  return <ItemPage lore={data} />;
}
