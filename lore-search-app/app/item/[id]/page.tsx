import { fetchLoreEntry } from "@/app/lib/data";
import ItemPage from "../../ui/item/itemPage";

export default async function Page({ params }: { params: { id: string } }) {
  let data = await fetchLoreEntry(params.id);

  return (
    <div>{data ? <ItemPage lore={data} /> : "Not Found"}</div>
  );
}
