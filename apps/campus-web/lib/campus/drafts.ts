import type {
  CampusDraft,
  CampusDraftInput,
  DraftKind,
} from "./types";

const kindLabels: Record<DraftKind, string> = {
  notice: "通知草稿",
  "meeting-brief": "会议材料草稿",
  "lesson-plan": "教案框架",
  assignment: "作业说明",
  rubric: "评分量规",
};

export function createDraft(input: CampusDraftInput): CampusDraft {
  const sourceTitles = input.citations.map((citation) => `《${citation.title}》`);
  const basis =
    sourceTitles.length > 0
      ? `依据 ${Array.from(new Set(sourceTitles)).join("、")} 的相关片段。`
      : "当前没有明确来源依据，仅可作为结构草稿。";

  return {
    id: `draft-${Date.now()}`,
    kind: input.kind,
    title: `${kindLabels[input.kind]}：${input.prompt.slice(0, 24) || "待补充主题"}`,
    role: input.role,
    status: "reviewing",
    sourceIds: Array.from(new Set(input.citations.map((citation) => citation.sourceId))),
    createdAt: new Date().toISOString(),
    assumptions: [
      "草稿需要人工审核后才能发布或提交。",
      "未连接真实业务系统，不会自动发送或审批。",
      basis,
    ],
    body: [
      "【待人工审核】",
      "",
      "一、背景",
      `${basis}本草稿用于协助整理表达，不代表正式决定。`,
      "",
      "二、拟处理事项",
      input.prompt || "请补充具体事项、对象、时间和责任人。",
      "",
      "三、工作要求",
      "1. 请相关人员核对事实、时间、对象和适用范围。",
      "2. 涉及正式通知、审批或高风险判断时，须由负责人确认。",
      "3. 如依据材料不足，应补充制度、会议纪要或上级通知后再发布。",
      "",
      "四、后续跟进",
      "建议将待办事项进入任务台账，保留来源和审核记录。",
    ].join("\n"),
  };
}
