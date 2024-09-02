type LoreEntry = {
  _id: string;
  datatype: string;
  name: string;
  text: string;
  expansion?: string;
  rank?: number;
  meta?: LoreEntryMetadata;  
};

type LoreEntryMetadata = {
  place_name?: string;
  patch?: string;
  issuer?: string;
  journal_genre?: string;
};

type Bookmark = {
  id: string;
  name: string;
  datatype: string;
};

type Project = {
  id: string;
  name: string;
};

type CheckBoxItem = {
  value: string;
  label: string;
  isChecked: boolean;
};

type SearchParams = {
  q?: string;
  sort?: string;
  category: string[];
  expansion: string[];
  page: number;
};
