// import { MongoClient, ServerApiVersion } from "mongodb";
import axios from "axios";

// if (!process.env.MONGODB_URI) {
//   throw new Error('Invalid/Missing environment variable: "MONGODB_URI"');
// }

const uri: string = process.env.MONGODB_URI ?? "";
const ITEMS_PER_PAGE = 1000;

export async function fetchSearchResults(
  querystring: string = "",
  currentPage: number = 1
) {
  if (!querystring) {
    return [];
  }

  let agg: any = [
    {
      $search: {
        index: "lore_text_search",
        text: {
          query: querystring,
          path: { wildcard: "*" },
        },
      },
    },
    {
      $limit: ITEMS_PER_PAGE,
    },
    {
      $sort: { datatype: -1, sortorder: 1, name: 1 },
    },
  ];

  if (querystring.split(" ").length <= 1) {
    agg = [
      {
        $search: {
          index: "lore_text_search",
          text: {
            query: querystring,
            path: { wildcard: "*" },
            synonyms: "synonyms",
          },
        },
      },
      {
        $limit: ITEMS_PER_PAGE,
      },
      {
        $sort: { datatype: -1, sortorder: 1, name: 1 },
      },
    ];
  }

  try {
    const client = axios.create({
      baseURL: "https://data.mongodb-api.com/app/data-lzrzo/endpoint/data/v1",
      headers: { apiKey: process.env.API_KEY, Accept: "application/json" },
    });

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
