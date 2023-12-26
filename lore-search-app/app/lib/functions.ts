export function mapSynonymsToDict(synonyms: any) {
  const synonymMapper: any = {};

  synonyms.forEach((s: any) => {
    if (s.mappingType == "equivalent") {
      s.synonyms.forEach((i: string) => {
        synonymMapper[i] = s.synonyms;
      });
    }
    else{
        synonymMapper[s.input] = s.synonyms;
    }
  });

  return synonymMapper;
}
