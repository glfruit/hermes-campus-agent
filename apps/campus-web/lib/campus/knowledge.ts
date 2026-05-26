import { knowledgeSources } from "./fixtures";
import type { CampusAnswer, CampusRole, Citation, KnowledgeExcerpt } from "./types";

type ScoredExcerpt = {
  excerpt: KnowledgeExcerpt;
  score: number;
};

const roleLabels: Record<CampusRole, string> = {
  "teaching-admin": "教学管理副职",
  teacher: "教师",
};

function tokenize(input: string): string[] {
  const normalized = input.toLowerCase();
  const asciiTokens = normalized.match(/[a-z0-9]+/g) ?? [];
  const chineseTokens = Array.from(
    new Set(
      normalized
        .replace(/[a-z0-9\s,.;:!?()[\]{}'"`~@#$%^&*_+=|\\/<>-]/g, "")
        .split("")
        .filter(Boolean),
    ),
  );
  return [...asciiTokens, ...chineseTokens];
}

function scoreExcerpt(question: string, excerpt: KnowledgeExcerpt): number {
  const questionTokens = tokenize(question);
  let score = 0;

  for (const keyword of excerpt.keywords) {
    if (question.includes(keyword)) score += 4;
  }

  for (const token of questionTokens) {
    if (excerpt.text.toLowerCase().includes(token)) score += 1;
    if (excerpt.heading.toLowerCase().includes(token)) score += 2;
  }

  return score;
}

function toCitation(excerpt: KnowledgeExcerpt): Citation {
  const source = knowledgeSources.find((item) => item.id === excerpt.sourceId);
  if (!source) {
    throw new Error(`Unknown source: ${excerpt.sourceId}`);
  }

  return {
    sourceId: source.id,
    excerptId: excerpt.id,
    title: source.title,
    department: source.department,
    version: source.version,
    effectiveDate: source.effectiveDate,
    excerpt: excerpt.text,
  };
}

export function searchKnowledge(question: string, role: CampusRole): Citation[] {
  const scored: ScoredExcerpt[] = knowledgeSources
    .filter((source) => source.audience.includes(role))
    .flatMap((source) => source.excerpts)
    .map((excerpt) => ({ excerpt, score: scoreExcerpt(question, excerpt) }))
    .filter((item) => item.score > 1)
    .sort((a, b) => b.score - a.score);

  return scored.slice(0, 3).map((item) => toCitation(item.excerpt));
}

export function answerCampusQuestion(
  question: string,
  role: CampusRole,
): CampusAnswer {
  const citations = searchKnowledge(question, role);
  const now = new Date().toISOString();

  if (citations.length === 0) {
    return {
      id: `answer-${Date.now()}`,
      question,
      role,
      confidence: "insufficient",
      citations: [],
      createdAt: now,
      answer:
        "当前本地知识库没有足够依据回答这个问题。建议补充对应制度、通知或会议材料后再生成结论；在没有来源前，不应把 AI 输出作为正式解释。",
      nextActions: ["补充来源材料", "改问更具体的问题", "转人工确认"],
    };
  }

  const lead = citations[0];
  const bullets = citations
    .map((citation) => `- ${citation.excerpt}`)
    .join("\n");

  return {
    id: `answer-${Date.now()}`,
    question,
    role,
    confidence: citations.length > 1 ? "grounded" : "partial",
    citations,
    createdAt: now,
    answer: `${roleLabels[role]}视角下，可以先依据《${lead.title}》处理。当前来源支持以下要点：\n${bullets}\n\n以上内容只能作为工作辅助和草稿依据，涉及审批、处分、成绩、人事或正式发布时仍需走学校规定程序。`,
    nextActions: ["生成草稿", "保存为任务", "补充材料后复核"],
  };
}
