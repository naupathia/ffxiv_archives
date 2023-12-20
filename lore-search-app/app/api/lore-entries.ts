import { fetchManyLoreEntries } from "@/app/lib/data";
import { NextApiRequest, NextApiResponse } from "next";

// EXPORT config to tell Next.js NOT to parse the body
export const config = {
  api: {
    bodyParser: false,
  },
};

// API handler function
export default function handler(
  req: NextApiRequest,
  res: NextApiResponse<any>
) {
  // const {id} = req.query;
  console.log(req.query);
  console.log(req);
  //   const ids = Array.isArray(req.query.id) ? req.query.id : [req.query.id];

  //   const data = await fetchManyLoreEntries(ids);

  //   res.send(data);
  return res.status(200);
}
