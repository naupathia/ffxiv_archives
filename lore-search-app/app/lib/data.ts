import clientPromise from "./mongodb";

const ITEMS_PER_PAGE = 1000;

export async function fetchSearchResults(
  querystring: string,
  currentPage: number = 1
) {
  if (!querystring) {
    return [];
  }

  console.log(querystring)

  const agg = [
    {
      $search: {
        index: "lore_text_search",
        text: {
          query: querystring,
          path: { wildcard: "*" },
          synonyms: "synonyms"
        },
      },
    },
    {
      $limit: ITEMS_PER_PAGE,
    },
    {
      $sort: {datatype: -1}
    }
  ];

  const client = await clientPromise;

  try {
    // Connect the client to the server	(optional starting in v4.7)
    
    const coll = client.db("tea").collection("lore");
    const results = await coll.aggregate(agg).toArray();

    return JSON.parse(JSON.stringify(results));
  } catch (error) {
    console.error("Database Error:", error);
  } finally {
    await client.close();
  }

  return [];
}
