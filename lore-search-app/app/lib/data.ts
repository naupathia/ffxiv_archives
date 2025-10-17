// import "server-only";

import { MongoClient, ServerApiVersion, ObjectId } from "mongodb";
import axios from "axios";
import { SORT_TYPES } from "@/types/enums";
import { mapSynonymsToDict } from "./functions";

if (!process.env.MONGODB_URI) {
  throw new Error('Invalid/Missing environment variable: "MONGODB_URI"');
}

const uri: string = process.env.MONGODB_URI ?? "";

const ITEMS_PER_PAGE = 100;
const API_KEY = process.env.API_KEY;
const DATASOURCE = "Cluster0";
const DATABASE = "tea";
const COLLECTION = "lore";
const INDEX_NAME = "default";
const SYNONYMS = "synonym_mapping";

async function createClient(col: string = COLLECTION) {
  const client = new MongoClient(uri, {
    serverApi: {
      version: ServerApiVersion.v1,
      strict: false,
      deprecationErrors: true,
    },
  });
  await client.connect();
  const database = client.db(DATABASE);
  return database.collection(col);
}

export async function fetchSearchResults(
  querystring: string = "",
  currentPage: number = 1,
  sort: string = "",
  expansion: string[] = [],
  category: string[] = []
) {
  if (!querystring) {
    return [];
  }
  if (currentPage <= 1) {
    currentPage = 1;
  }

  const skip = (currentPage - 1) * ITEMS_PER_PAGE;

  let query: any = createWordSearchQuery(querystring);

  if (querystring.startsWith('"') && querystring.endsWith('"')) {
    query = createPhraseSearchQuery(querystring);
  }

  const agg: any[] = [];

  agg.push(query);

  if (expansion) {
    let e: any = [...expansion];
    if (expansion.length > 0 && expansion[0] != "") {
      e = [...expansion, null];
    }
    agg.push({
      $match: { expansion: { $in: e } },
    });
  }

  if (category) {
    agg.push({
      $match: { datatype: { $in: category } },
    });
  }

  if (sort && sort == SORT_TYPES.CATEGORY) {
    agg.push({
      $sort: { datatype: -1, rank: 1, name: 1 },
    });
  }

  agg.push({
    $skip: skip,
  });

  agg.push({
    $limit: ITEMS_PER_PAGE,
  });

  try {
    const collection = await createClient();

    const response = await collection.aggregate<LoreEntry>(agg).toArray();

    return response;
  } catch (error) {
    console.error("Data Error:", error);
  }

  return [];
}

function createPhraseSearchQuery(querystring: string) {
  return {
    $search: {
      index: INDEX_NAME,
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
      synonyms: SYNONYMS,
    },
  }));

  return {
    $search: {
      index: INDEX_NAME,
      compound: {
        must: wordQueries,
      },
    },
  };
}

export async function fetchLoreEntry(id: string) {
  try {
    const collection = await createClient();

    const response = await collection.findOne<LoreEntry>({ _id: new ObjectId(id) });

    return response;
  } catch (error) {
    console.error("Data Error:", error);
  }

  return null;
}

export async function fetchManyLoreEntries(ids: any) {
  try {
    const idParams = ids.map((i: string) => ({ $oid: i }));
    const collection = await createClient();
    const response = await collection.find<LoreEntry>({
      _id: { $in: idParams },
    }).toArray();

    return response;
    // const sortedItems: LoreEntry[] = [];

    // ids.forEach((id: string) => {
    //   const foundItem = items.find((x: any) => x._id == id);
    //   if (foundItem) {
    //     sortedItems.push(foundItem);
    //   }
    // });

    // return sortedItems;
  } catch (error) {
    console.error("Data Error:", error);
  }

  return [];
}

export async function fetchSynonyms() {
  try {
    const collection = await createClient("synonyms");
    const items = await collection.find({}).toArray();

    const dictItems = mapSynonymsToDict(items);
    return dictItems;
  } catch (error) {
    console.error("Data Error:", error);
  }

  return [];
}
