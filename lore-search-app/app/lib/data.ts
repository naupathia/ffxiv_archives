// import "server-only";

// import { MongoClient, ServerApiVersion } from "mongodb";
import axios from "axios";
import { SORT_TYPES } from "@/types/enums";

// if (!process.env.MONGODB_URI) {
//   throw new Error('Invalid/Missing environment variable: "MONGODB_URI"');
// }

const uri: string = process.env.MONGODB_URI ?? "";
const ITEMS_PER_PAGE = 100;

function createClient() {
  return axios.create({
    baseURL: "https://data.mongodb-api.com/app/data-lzrzo/endpoint/data/v1",
    headers: { apiKey: process.env.API_KEY, Accept: "application/json" },
  });
}

export async function fetchSearchResults(
  querystring: string = "",
  currentPage: number = 1,
  sort: string = ""
) {
  if (!querystring) {
    return [];
  }

  // console.log(querystring);

  const wordQueries = querystring.split(" ").map((word) => ({
    text: {
      query: word,
      path: ['text', 'name'],
      synonyms: "synonyms",
    },
  }));

  const agg: any[] = [
    {
      $search: {
        index: "lore_text_search",
        compound: {
          must: wordQueries,
        }
      },
    },
    {
      $limit: ITEMS_PER_PAGE,
    },
  ];

  if (sort && sort == SORT_TYPES.CATEGORY) {
    agg.push({
      $sort: { datatype: -1, sortorder: 1, name: 1 },
    });
  }

  try {
    const client = createClient();

    const response = await client.post("/action/aggregate", {
      dataSource: "Cluster0",
      database: "tea",
      collection: "lore",
      pipeline: agg,
    });

    return response.data.documents;
  } catch (error) {
    console.error("Data Error:", error);
  }

  // Create a MongoClient with a MongoClientOptions object to set the Stable API version
  // const client = new MongoClient(uri, {
  //   serverApi: {
  //     version: ServerApiVersion.v1,
  //     deprecationErrors: true,
  //   }
  // });

  // client.connect()

  // try {
  //   // Connect the client to the server	(optional starting in v4.7)

  //   const coll = client.db("tea").collection("lore");
  //   const results = await coll.aggregate(agg).toArray();

  //   return JSON.parse(JSON.stringify(results));
  // } catch (error) {
  //   console.error("Database Error:", error);
  // } finally {
  //   await client.close();
  // }

  return [];
}

export async function fetchLoreEntry(id: string) {
  try {
    const client = createClient();

    const response = await client.post("/action/findOne", {
      dataSource: "Cluster0",
      database: "tea",
      collection: "lore",
      filter: { _id: { $oid: id } },
    });

    return response.data.document;
  } catch (error) {
    console.error("Data Error:", error);
  }

  return null;
}

export async function fetchManyLoreEntries(ids: any) {
  try {
    const idParams = ids.map((i: any) => ({ $oid: i }));
    const client = createClient();
    const response = await client.post("/action/find", {
      dataSource: "Cluster0",
      database: "tea",
      collection: "lore",
      filter: { _id: { $in: idParams } },
    });

    const items = response.data.documents;
    const sortedItems: LoreEntry[] = [];

    ids.forEach((id: string) => {
      const foundItem = items.find((x: any) => x._id == id);
      sortedItems.push(foundItem);
    });

    return sortedItems;
  } catch (error) {
    console.error("Data Error:", error);
  }

  return [];
}
