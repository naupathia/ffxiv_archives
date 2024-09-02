export function mapSynonymsToDict(synonyms: any) {
  const synonymMapper: any = {};

  synonyms.forEach((s: any) => {
    if (s.mappingType == "equivalent") {
      s.synonyms.forEach((i: string) => {
        synonymMapper[i] = s.synonyms;
      });
    } else {
      synonymMapper[s.input] = s.synonyms;
    }
  });

  return synonymMapper;
}

// @ts-ignore
export const fetcher = (...args) => fetch(...args).then((res) => res.json());

export function isEmptyArray(arr?: string[]) {
  return arr == null || arr.length == 0 || arr[0] == "";
}

export function highlightSearchText(
  text?: string,
  searchText?: string,
  synonyms?: any
) {
  if (searchText) {
    if (searchText.startsWith('"') && searchText.endsWith('"')) {
      const rwords = new RegExp(
        "\\b(" + searchText.slice(1, -1) + ")\\b",
        "gmi"
      );
      return text?.replace(rwords, "<mark>$&</mark>") ?? "";
    } else {
      let words = searchText?.split(" ");
      if (synonyms) {
        words.forEach((w: string) => {
          if (synonyms[w.toLowerCase()]) {
            words = [...words, ...synonyms[w.toLowerCase()]];
          }
        });
      }
      const rwords = new RegExp("\\b(" + words.join("|") + ")\\b", "gmi");
      return text?.replace(rwords, "<mark>$&</mark>") ?? "";
    }
  }
  return text;
}

export function translateType(type: string) {
  switch (type) {
    case "card":
      return "TRIPLE TRIAD CARD";
    default:
      return type;
  }
}
