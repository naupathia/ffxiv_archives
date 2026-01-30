import { fetchSearchResults } from "@/app/lib/data";
import { NextRequest } from "next/server";

// API handler function
export async function GET(req: NextRequest) {
  const searchParams = req.nextUrl.searchParams;
  const q = searchParams.get("q");
  const page = parseInt(searchParams.get("page") || "1");
  const sort = searchParams.get("sort");
  const categories = searchParams.getAll("category") || [];
  const types = searchParams.getAll("type") || [];
  const expansions = searchParams.getAll("expansion") || [];

  const filters = [];

  if (categories && categories.length > 0) {
    filters.push({ name: "category", values: categories });
  }
  if (types && types.length > 0) {
    filters.push({ name: "datatype", values: types });
  }
  if (expansions && expansions.length > 0) {
    filters.push({ name: "expansion", values: expansions });
  }

  const data: any = await fetchSearchResults(
    q || "",
    page,
    sort || "",
    filters,
  );

  return Response.json(data);
}
