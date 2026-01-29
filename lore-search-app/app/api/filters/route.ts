import { fetchFilters } from "@/app/lib/data";
import { NextRequest } from "next/server";

// API handler function
export async function GET(req: NextRequest) {

  const data = await fetchFilters();

  return Response.json(data);
}
