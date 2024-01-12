import { fetchManyLoreEntries } from "@/app/lib/data";
import { NextRequest } from "next/server";

// API handler function
export async function GET(req: NextRequest) {
  const searchParams = req.nextUrl.searchParams;
  const ids = searchParams.getAll("id");

  const data: any[] = await fetchManyLoreEntries(ids);

  const stringResults = data.map((doc: any) => getEntryAsString(doc));
  const headers = new Headers();
  headers.append("Content-Type", "text/plain; charset-UTF-8");
  return new Response(stringResults.join("\n\r"), { headers });
}

function getEntryAsString(doc: any) {
  const details = doc.issuer
    ? `
${doc.issuer ? `${doc.issuer} (${doc.place_name})` : ""}
${doc.journal_genre ? `${doc.journal_genre} (${doc.expansion})` : ""}`
    : "";

  return `[${doc.datatype}]

${doc.name} ${details}

${doc.text}

--------------------------------------------------------------------------------------------------`;
}
