
import clientPromise from "../lib/mongodb";

export default function Search({ results }) {
  return (
    <div className="container">
      <h1>Search Results</h1>

      {results ? (
        <table className="hidden min-w-full text-gray-900 md:table align-text-top">
          <tbody className="bg-white">
            {results.map((item) => (
              <tr
                key={item._id}
                className="w-full border-b py-3 text-sm align-text-top"
              >
                <td className="whitespace-nowrap px-3 py-3 align-text-top">{item.datatype}</td>
                <td className="whitespace-nowrap px-3 py-3 align-text-top">{item.name}</td>
                <td className="whitespace-nowrap px-3 py-3 align-text-top">
                  <pre>{item.text}</pre>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No results found.</p>
      )}
    </div>
  );
}

export async function getServerSideProps({ query }) {
  const searchText = query.q;
  let results = [];

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
      $limit: 20,
    },
  ];

  if (searchText) {
    try {
      console.log(searchText);
      const client = await clientPromise;
      const db = client.db("tea");

      results = await db.collection("lore").aggregate(agg).toArray();
    } catch (e) {
      console.error(e);
    }
  }

  return {
    props: { results: JSON.parse(JSON.stringify(results)) },
  };
}
