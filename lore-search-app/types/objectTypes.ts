type Expansion = {
  num: number;
  name: string;
  abbr: string;
}

type TypeDefinition = {
  category: string;
  name: string
}

type LoreEntry = {
  _id: string;
  datatype: TypeDefinition;
  title: string;
  text_html: string;
  expansion?: Expansion;
  meta?: LoreEntryMetadata;  
  highlights: HighlightData[];
};

type LoreEntryMetadata = {
  place_name?: string;
  patch?: string;
  issuer?: string;
  journal_genre?: string;
};

type Project = {
  id: string;
  name: string;
};

type SearchParams = {
  q?: string;
  sort?: string;
  category: string[];
  type: string[];
  expansion: string[];
};

type HighlightTexts = {
  type: string;
  value: string;
}

type HighlightData = {
  path: string;
  texts: HighlightTexts[];
}

type Filter = {
  name: string,
  values: string[]
}