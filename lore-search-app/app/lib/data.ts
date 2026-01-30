// import "server-only";

import { MongoClient, ServerApiVersion, ObjectId } from "mongodb";
import { SORT_TYPES } from "@/types/enums";
import { mapSynonymsToDict } from "./functions";

if (!process.env.MONGODB_URI) {
  throw new Error('Invalid/Missing environment variable: "MONGODB_URI"');
}

const uri: string = process.env.MONGODB_URI ?? "";

const ITEMS_PER_PAGE = 500;
const DATABASE = "tea";
const COLLECTION = "lore";
const INDEX_NAME = "default";
const SYNONYMS = "synonym_mapping";
const SEARCH_FIELDS = ["title", "text"];

async function connect(col: string = COLLECTION) {
  const client = new MongoClient(uri, {
    serverApi: {
      version: ServerApiVersion.v1,
      strict: false,
      deprecationErrors: true,
    },
    maxPoolSize: 100,
  });
  await client.connect();
  return client;
}

function collection(client: MongoClient) {
  return client.db(DATABASE).collection(COLLECTION);
}

export async function fetchSearchResults(
  querystring: string = "",
  currentPage: number = 1,
  sort: string = "",
  filters: Filter[] = [],
) {
  if (!querystring) {
    return [];
  }
  if (currentPage <= 1) {
    currentPage = 1;
  }

  const skip = (currentPage - 1) * ITEMS_PER_PAGE;

  let query: any = createQuery(querystring, filters);

  const agg: any[] = [];

  agg.push({
    $search: query,
  });

  agg.push({
    $addFields: {
      highlights: { $meta: "searchHighlights" },
    },
  });

  if (sort?.toLowerCase() == SORT_TYPES.CATEGORY) {
    agg.push({
      $sort: {
        "datatype.category": 1,
        "datatype.name": 1,
        "expansion.num": 1,
        searchScore: { $meta: "searchScore" },
        _id: 1,
      },
    });
  } else if (sort?.toLowerCase() == SORT_TYPES.NAME) {
    agg.push({
      $sort: {
        "datatype.name": 1,
        searchScore: { $meta: "searchScore" },
        _id: 1,
      },
    });
  } else {
    agg.push({
      $sort: { searchScore: { $meta: "searchScore" }, _id: 1 },
    });
  }

  agg.push({
    $facet: {
      documents: [{ $skip: skip }, { $limit: ITEMS_PER_PAGE }],
      count: [{ $count: "total" }],
    },
  });

  agg.push({
    $project: {
      documents: 1,
      count: { $first: "$count.total" },
    },
  });

  console.log(JSON.stringify(agg));

  const client = await connect();
  const col = await collection(client);
  try {
    const response = await col.aggregate(agg).toArray();

    return {
      query: agg,
      documents: response[0].documents,
      count: response[0].count,
    };
  } catch (error) {
    console.error("Data Error:", error);
  } finally {
    client.close();
  }

  return { items: [], query: agg };
}

function createQuery(querystring: string, filters: Filter[]) {
  let mustFilters: any = [];
  let shouldFilters: any = [];
  let minShould = 0;

  if (querystring.startsWith('"') && querystring.endsWith('"')) {
    const searchString = querystring.slice(1, -1);
    console.log(searchString);
    mustFilters.push({
      phrase: {
        query: searchString,
        path: SEARCH_FIELDS,
      },
    });
  } else {
    minShould = 1;
    shouldFilters = [
      {
        phrase: {
          query: querystring,
          path: SEARCH_FIELDS,
        },
      },
      {
        text: {
          query: querystring,
          path: SEARCH_FIELDS,
          matchCriteria: "all",
          synonyms: SYNONYMS,
        },
      },
    ];
  }

  if (filters && filters.length > 0) {
    console.log(JSON.stringify(filters));
    const innerShouldFilter: any[] = [];
    const innerMustFilter: any[] = [];
    filters.forEach((element) => {
      if (element.name == "category") {
        innerShouldFilter.push({
          in: {
            path: "datatype.category",
            value: element.values,
          },
        });
      } else if (element.name == "datatype") {
        innerShouldFilter.push({
          in: {
            path: "datatype.name",
            value: element.values,
          },
        });
      } else {
        const filterName = "expansion.name";
        innerMustFilter.push({
          in: {
            path: filterName,
            value: element.values,
          },
        });
      }
    });

    mustFilters.push({
      compound: {
        must: innerMustFilter,
        should: innerShouldFilter,
        minimumShouldMatch: innerShouldFilter.length > 0 ? 1 : 0,
      },
    });
  }

  return {
    index: INDEX_NAME,
    compound: {
      should: shouldFilters,
      must: mustFilters,
      minimumShouldMatch: minShould,
    },
    highlight: {
      path: "text",
      maxNumPassages: 50,
    },
  };
}

export async function fetchFilters() {
  const client = await connect();
  const col = await collection(client);
  try {
    const response = await col.aggregate([
      {
        $facet: {
          categories: [
            { $group: { _id: "$datatype" } },
            { $sort: { "_id.category": 1, "_id.name": 1 } },
          ],
          expansions: [
            { $group: { _id: "$expansion" } },
            { $sort: { "_id.num": 1 } },
          ],
        },
      },
      {
        $project: {
          categories: "$categories._id",
          expansions: "$expansions._id.name",
        },
      },
    ]);

    return await response.next();
  } finally {
    await client.close();
  }
}

export async function fetchLoreEntry(id: string) {
  const client = await connect();
  const col = await collection(client);
  try {
    const document = await col.findOne<LoreEntry>({
      _id: new ObjectId(id),
    });

    if (document) {
      document._id = document._id.toString();
    }

    return await document;
  } catch (error) {
    console.error("Data Error:", error);
  } finally {
    await client.close();
  }

  return null;
}

export async function fetchManyLoreEntries(ids: any) {
  const client = await connect();
  const col = await collection(client);
  try {
    const idParams = ids.map((i: string) => ({ $oid: i }));

    const response = await col
      .find<LoreEntry>({
        _id: { $in: idParams },
      })
      .toArray();

    return await response;
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
  } finally {
    await client.close();
  }

  return [];
}

export async function fetchSynonyms() {
  const client = await connect();
  const col = await collection(client);

  try {
    const items = await col.find({}).toArray();

    const dictItems = await mapSynonymsToDict(items);
    return dictItems;
  } catch (error) {
    console.error("Data Error:", error);
  } finally {
    await client.close();
  }

  return [];
}
