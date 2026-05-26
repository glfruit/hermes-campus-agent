import type { CampusAnswer, CampusDraft, CampusRole, CampusTask } from "./types";

export function taskFromAnswer(answer: CampusAnswer): CampusTask {
  return {
    id: `task-answer-${Date.now()}`,
    title: `复核问答：${answer.question.slice(0, 22)}`,
    role: answer.role,
    status: answer.confidence === "insufficient" ? "draft" : "reviewing",
    sourceIds: answer.citations.map((citation) => citation.sourceId),
    createdFrom: "qa",
    detail:
      answer.confidence === "insufficient"
        ? "当前依据不足，需补充材料后再处理。"
        : "根据来源引用生成的问答，需要人工确认后进入正式工作。",
  };
}

export function taskFromDraft(draft: CampusDraft): CampusTask {
  return {
    id: `task-draft-${Date.now()}`,
    title: `审核草稿：${draft.title}`,
    role: draft.role,
    status: "reviewing",
    sourceIds: draft.sourceIds,
    createdFrom: "draft",
    detail: "检查草稿依据、措辞、对象和发布边界。确认前不得作为正式通知。",
  };
}

export function roleTaskCount(tasks: CampusTask[], role: CampusRole): number {
  return tasks.filter((task) => task.role === role).length;
}
