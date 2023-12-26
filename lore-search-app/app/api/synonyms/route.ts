import { fetchSynonyms } from "@/app/lib/data";
import { NextRequest } from "next/server";

// API handler function
export async function GET(req: NextRequest) {
  //   const searchParams = req.nextUrl.searchParams;
  //   const ids = searchParams.getAll("id");
  //   console.log(ids);

  const data: any[] = await fetchSynonyms();

  return Response.json(data);
}
