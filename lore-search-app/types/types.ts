type LoreEntry = {
    _id: string;
    datatype: string;
    name?: string;
    text?: string;
    sortorder?: number;
    place_name?: string;
    patch?: string;
    issuer?: string;
    journal_genre?: string;
    expansion?: string
};

type Bookmark = {
    id: string;
    name: string;
    datatype: string
}

type Project = {
    id: string; 
    name: string
}