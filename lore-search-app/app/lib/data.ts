import { MongoClient, ServerApiVersion } from 'mongodb'

if (!process.env.MONGODB_URI) {
  throw new Error('Invalid/Missing environment variable: "MONGODB_URI"')
}

const uri: string = process.env.MONGODB_URI ?? "";
const ITEMS_PER_PAGE = 1000;

export async function fetchSearchResults(
  querystring: string,
  currentPage: number = 1
) {
  if (!querystring) {
    return [];
  }

  const agg = [
    {
      $search: {
        index: "lore_text_search",
        text: {
          query: querystring,
          path: { wildcard: "*" }
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

  
  // Create a MongoClient with a MongoClientOptions object to set the Stable API version
  const client = new MongoClient(uri, {
    serverApi: {
      version: ServerApiVersion.v1,
      deprecationErrors: true,
    }
  });

  client.connect()

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
