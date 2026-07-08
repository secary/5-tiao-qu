export const importStatuses = [
  "uploaded",
  "extracting",
  "chunking",
  "embedding",
  "ready",
  "failed"
] as const;

export type ImportStatus = (typeof importStatuses)[number];

export const answerTypes = [
  "direct_rule",
  "related_inference",
  "not_found",
  "conflict"
] as const;

export type AnswerType = (typeof answerTypes)[number];

export const sourceTypes = [
  "base_rulebook",
  "expansion_rulebook",
  "faq",
  "errata",
  "player_note"
] as const;

export type SourceType = (typeof sourceTypes)[number];

export type BoundingBox = {
  pageNumber: number;
  x: number;
  y: number;
  width: number;
  height: number;
};

export type Citation = {
  id: string;
  chunkId: string;
  pageNumber: number;
  chapterTitle?: string;
  chunkText: string;
  sourceFile: string;
  sourceType: SourceType;
  sourcePriority: number;
  boundingBox?: BoundingBox;
  similarityScore?: number;
};

export type RagAnswer = {
  id: string;
  answerType: AnswerType;
  conclusion: string;
  explanation?: string;
  confidence?: number;
  citations: Citation[];
};
