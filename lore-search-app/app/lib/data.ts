// import "server-only";

// import { MongoClient, ServerApiVersion } from "mongodb";
import axios from "axios";
import { SORT_TYPES } from "@/types/enums";
import { mapSynonymsToDict } from "./functions";

// if (!process.env.MONGODB_URI) {
//   throw new Error('Invalid/Missing environment variable: "MONGODB_URI"');
// }

const uri: string = process.env.MONGODB_URI ?? "";
const ITEMS_PER_PAGE = 100;
const API_KEY = process.env.API_KEY;

function createClient() {
  return axios.create({
    baseURL: "https://data.mongodb-api.com/app/data-lzrzo/endpoint/data/v1",
    headers: { apiKey: API_KEY, Accept: "application/json" },
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
  if (currentPage <= 1) {
    currentPage = 1;
  }

  const skip = (currentPage - 1) * ITEMS_PER_PAGE;
  console.log("skip num " + skip);

  let query: any = createWordSearchQuery(querystring);

  if (querystring.startsWith('"') && querystring.endsWith('"')) {
    query = createPhraseSearchQuery(querystring);
  }

  const agg: any[] = [
    query,
    {
      $skip: skip,
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

  return [];
}

function createPhraseSearchQuery(querystring: string) {
  return {
    $search: {
      index: "lore_text_search",
      phrase: {
        query: querystring,
        path: ["name", "text"],
      },
    },
  };
}

function createWordSearchQuery(querystring: string) {
  const wordQueries = querystring.split(" ").map((word) => ({
    text: {
      query: word,
      path: ["text", "name"],
      synonyms: "synonyms",
    },
  }));

  return {
    $search: {
      index: "lore_text_search",
      compound: {
        must: wordQueries,
      },
    },
  };
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
    const idParams = ids.map((i: string) => ({ $oid: i }));
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

export async function fetchSynonyms() {
  try {
    const client = createClient();
    const response = await client.post("/action/find", {
      dataSource: "Cluster0",
      database: "tea",
      collection: "synonyms",
      filter: {},
    });

    const items = response.data.documents;
    const dictItems = mapSynonymsToDict(items);
    return dictItems;
  } catch (error) {
    console.error("Data Error:", error);
  }

  return [];
}
