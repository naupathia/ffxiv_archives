import { fetchSearchResults } from "@/app/lib/data";
import { NextRequest } from "next/server";

// API handler function
export async function GET(req: NextRequest) {
  const searchParams = req.nextUrl.searchParams;
  const q = searchParams.get("q");
  const page = parseInt(searchParams.get("page") || "1");
  const sort = searchParams.get("sort");
  const categories = searchParams.getAll("category") || [];
  const expansions = searchParams.getAll("expansion") || [];

  const data: any[] = await fetchSearchResults(q || '', page, sort || '', expansions, categories);

  return Response.json(data);
}
