import { fetchLoreEntry } from "@/app/lib/data";
import ItemPage from "../../ui/item/itemPage";

export default async function Page({ params }: { params: { id: string } }) {
  const { id } = await params;
  let data = await fetchLoreEntry(id);

  return <div>{data ? <ItemPage lore={data} /> : "Not Found"}</div>;
}
