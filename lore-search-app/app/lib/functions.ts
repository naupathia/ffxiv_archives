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
export const fetcher = (...args) => fetch(...args).then((res) => {
  console.log('api call finished');
  return res.json();
});

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

export function convertToTitleCase(e: string) {
  if (!e) {
    return "";
  }

  return e
    .toLowerCase()
    .split(" ")
    .map(function (word: string) {
      return word.charAt(0).toUpperCase().concat(word.substring(1));
    })
    .join(" ");
}

export function formatHighlightToHtml(highlightData: any) {
  let htmlString = '';
  highlightData.texts.forEach((textSnippet: any) => {
    if (textSnippet.type === 'hit') {
      // Wrap the 'hit' type text with the <mark> tag
      htmlString += `<mark>${textSnippet.value}</mark>`;
    } else {
      // Add 'text' type content as plain text
      htmlString += textSnippet.value;
    }
  });
  return htmlString;
}

export function highlightText(text: string, highlightData: HighlightData[]) {
  let formattedText = text;
  highlightData.forEach(h => {
    const originalText = h.texts.map(t=>t.value).join('');
    const highlightText = formatHighlightToHtml(h);
    formattedText = formattedText.replace(originalText, highlightText);
  })
  return formattedText;
}