import clientPromise from "../../lib/mongodb";

export default async (req, res) => {
  //   const searchText = req.query.q;
  const searchText = "Shiva";

  const agg = [
    {
      $search: {
        index: "lore_text_search",
        text: {
          query: searchText,
          path: { wildcard: "*" },
          synonyms: "synonyms"
        },
      },
    },
    {
      $limit: 5,
    }
  ];

  try {
    const client = await clientPromise;
    const db = client.db("tea");

    const results = await db.collection("lore").aggregate(agg).toArray();

    res.json({ query: searchText, results: results });
  } catch (e) {
    console.error(e);
  }
};
