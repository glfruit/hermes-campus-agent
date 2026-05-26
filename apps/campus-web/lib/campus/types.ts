export type CampusRole = "teaching-admin" | "teacher";

export type SourceType = "policy" | "notice" | "template" | "meeting" | "guide";

export type Sensitivity = "public" | "internal" | "restricted";

export type ReviewStatus = "draft" | "reviewing" | "confirmed" | "done";

export type TaskOrigin = "manual" | "qa" | "draft";

export type KnowledgeSource = {
  id: string;
  title: string;
  department: string;
  version: string;
  effectiveDate: string;
  sourceType: SourceType;
  sensitivity: Sensitivity;
  audience: CampusRole[];
  summary: string;
  excerpts: KnowledgeExcerpt[];
};

export type KnowledgeExcerpt = {
  id: string;
  sourceId: string;
  heading: string;
  text: string;
  keywords: string[];
};

export type Citation = {
  sourceId: string;
  excerptId: string;
  title: string;
  department: string;
  version: string;
  effectiveDate: string;
  excerpt: string;
};

export type CampusAnswer = {
  id: string;
  question: string;
  role: CampusRole;
  answer: string;
  confidence: "grounded" | "partial" | "insufficient";
  citations: Citation[];
  nextActions: string[];
  createdAt: string;
};

export type DraftKind =
  | "notice"
  | "meeting-brief"
  | "lesson-plan"
  | "assignment"
  | "rubric";

export type CampusDraft = {
  id: string;
  kind: DraftKind;
  title: string;
  body: string;
  role: CampusRole;
  status: ReviewStatus;
  sourceIds: string[];
  assumptions: string[];
  createdAt: string;
};

export type CampusTask = {
  id: string;
  title: string;
  role: CampusRole;
  status: ReviewStatus;
  sourceIds: string[];
  dueAt?: string;
  createdFrom: TaskOrigin;
  detail: string;
};

export type CampusAgentInput = {
  role: CampusRole;
  question: string;
};

export type CampusAgentOutput = CampusAnswer;

export type CampusDraftInput = {
  role: CampusRole;
  kind: DraftKind;
  prompt: string;
  citations: Citation[];
};

export type CampusDraftOutput = CampusDraft;
