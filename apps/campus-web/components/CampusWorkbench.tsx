"use client";

import { useMemo, useState } from "react";
import type { ReactNode } from "react";
import {
  AlertTriangle,
  BookOpenCheck,
  CalendarCheck2,
  ClipboardList,
  FileEdit,
  GraduationCap,
  Library,
  MessageSquareText,
  Plus,
  ShieldCheck,
  Sparkles,
  UserRoundCog,
} from "lucide-react";
import { initialTasks, knowledgeSources } from "@/lib/campus/fixtures";
import { hermesBridge } from "@/lib/hermes/bridge";
import { taskFromAnswer, taskFromDraft } from "@/lib/campus/tasks";
import type {
  CampusAnswer,
  CampusDraft,
  CampusRole,
  CampusTask,
  DraftKind,
} from "@/lib/campus/types";

const roleCopy: Record<
  CampusRole,
  { label: string; description: string; icon: ReactNode; prompts: string[] }
> = {
  "teaching-admin": {
    label: "教学管理副职",
    description: "制度问答、材料起草、会议纪要、任务跟踪",
    icon: <UserRoundCog aria-hidden="true" />,
    prompts: [
      "调课获批后需要通知哪些内容？",
      "期末考试材料要提前多久提交？",
      "教学检查汇总报告应包含哪些材料？",
    ],
  },
  teacher: {
    label: "教师",
    description: "备课、作业、量规、学生沟通草稿",
    icon: <GraduationCap aria-hidden="true" />,
    prompts: [
      "帮我设计下周课程教学计划结构",
      "作业评分量规应该包含哪些维度？",
      "考试材料提交有什么要求？",
    ],
  },
};

const statusLabels: Record<CampusTask["status"], string> = {
  draft: "草稿",
  reviewing: "审核中",
  confirmed: "已确认",
  done: "已完成",
};

const draftKindOptions: { value: DraftKind; label: string }[] = [
  { value: "notice", label: "通知" },
  { value: "meeting-brief", label: "会议材料" },
  { value: "lesson-plan", label: "教案" },
  { value: "assignment", label: "作业" },
  { value: "rubric", label: "量规" },
];

export function CampusWorkbench() {
  const [role, setRole] = useState<CampusRole>("teaching-admin");
  const [question, setQuestion] = useState(roleCopy["teaching-admin"].prompts[0]);
  const [answer, setAnswer] = useState<CampusAnswer | null>(null);
  const [draft, setDraft] = useState<CampusDraft | null>(null);
  const [tasks, setTasks] = useState<CampusTask[]>(initialTasks);
  const [draftKind, setDraftKind] = useState<DraftKind>("notice");
  const [isThinking, setIsThinking] = useState(false);

  const roleSources = useMemo(
    () => knowledgeSources.filter((source) => source.audience.includes(role)),
    [role],
  );

  const roleTasks = useMemo(
    () => tasks.filter((task) => task.role === role),
    [role, tasks],
  );

  async function askQuestion(nextQuestion = question) {
    setIsThinking(true);
    setQuestion(nextQuestion);
    const result = await hermesBridge.ask({ role, question: nextQuestion });
    setAnswer(result);
    setDraft(null);
    setIsThinking(false);
  }

  async function generateDraft() {
    const result = await hermesBridge.draft({
      role,
      kind: draftKind,
      prompt: question,
      citations: answer?.citations ?? [],
    });
    setDraft(result);
  }

  function saveAnswerTask() {
    if (!answer) return;
    setTasks((current) => [taskFromAnswer(answer), ...current]);
  }

  function saveDraftTask() {
    if (!draft) return;
    setTasks((current) => [taskFromDraft(draft), ...current]);
  }

  function switchRole(nextRole: CampusRole) {
    setRole(nextRole);
    setQuestion(roleCopy[nextRole].prompts[0]);
    setAnswer(null);
    setDraft(null);
  }

  return (
    <main className="campus-shell">
      <aside className="rail" aria-label="角色与功能导航">
        <div className="brand-block">
          <div className="brand-mark">
            <Sparkles aria-hidden="true" />
          </div>
          <div>
            <strong>Hermes Campus</strong>
            <span>一期工作台</span>
          </div>
        </div>

        <section className="role-switcher" aria-label="角色切换">
          {(Object.keys(roleCopy) as CampusRole[]).map((item) => (
            <button
              className={item === role ? "role-card active" : "role-card"}
              key={item}
              onClick={() => switchRole(item)}
              type="button"
            >
              <span className="role-icon">{roleCopy[item].icon}</span>
              <span>
                <strong>{roleCopy[item].label}</strong>
                <small>{roleCopy[item].description}</small>
              </span>
            </button>
          ))}
        </section>

        <nav className="nav-list" aria-label="一期能力">
          <a className="nav-item active" href="#qa">
            <MessageSquareText aria-hidden="true" />
            来源问答
          </a>
          <a className="nav-item" href="#draft">
            <FileEdit aria-hidden="true" />
            草稿审核
          </a>
          <a className="nav-item" href="#tasks">
            <ClipboardList aria-hidden="true" />
            任务台账
          </a>
          <a className="nav-item" href="#sources">
            <Library aria-hidden="true" />
            知识来源
          </a>
        </nav>

        <div className="guardrail">
          <ShieldCheck aria-hidden="true" />
          <p>当前版本只使用本地 fixture，不连接真实学校系统，不自动发布或审批。</p>
        </div>
      </aside>

      <section className="workspace">
        <header className="topbar">
          <div>
            <p className="eyebrow">Web + 企业微信入口的第一期核心工作面</p>
            <h1>{roleCopy[role].label}工作台</h1>
          </div>
          <div className="metrics" aria-label="当前状态">
            <div>
              <strong>{roleSources.length}</strong>
              <span>可用来源</span>
            </div>
            <div>
              <strong>{roleTasks.length}</strong>
              <span>角色任务</span>
            </div>
            <div>
              <strong>0</strong>
              <span>外部写入</span>
            </div>
          </div>
        </header>

        <div className="content-grid">
          <section className="main-panel" id="qa">
            <div className="section-heading">
              <div>
                <p className="eyebrow">Knowledge Q&A</p>
                <h2>来源引用型问答</h2>
              </div>
              <span className={answer?.confidence === "insufficient" ? "badge warn" : "badge"}>
                {answer ? confidenceLabel(answer.confidence) : "等待提问"}
              </span>
            </div>

            <div className="prompt-row">
              <textarea
                aria-label="输入校园工作问题"
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
                rows={4}
              />
              <button
                className="primary-button"
                disabled={isThinking}
                onClick={() => askQuestion()}
                type="button"
              >
                <BookOpenCheck aria-hidden="true" />
                {isThinking ? "检索中" : "带来源回答"}
              </button>
            </div>

            <div className="quick-prompts" aria-label="常用问题">
              {roleCopy[role].prompts.map((prompt) => (
                <button key={prompt} onClick={() => askQuestion(prompt)} type="button">
                  {prompt}
                </button>
              ))}
            </div>

            <article className="answer-box">
              {answer ? (
                <>
                  <div className="answer-meta">
                    <span>{new Date(answer.createdAt).toLocaleString("zh-CN")}</span>
                    <span>{roleCopy[answer.role].label}</span>
                  </div>
                  <pre>{answer.answer}</pre>
                  <div className="action-row">
                    <button onClick={generateDraft} type="button">
                      <FileEdit aria-hidden="true" />
                      生成草稿
                    </button>
                    <button onClick={saveAnswerTask} type="button">
                      <Plus aria-hidden="true" />
                      保存为任务
                    </button>
                  </div>
                </>
              ) : (
                <div className="empty-state">
                  <MessageSquareText aria-hidden="true" />
                  <p>选择一个常用问题，或输入教学管理/教师工作问题。回答必须带来源，没有依据时会明确拒答。</p>
                </div>
              )}
            </article>
          </section>

          <aside className="side-panel" id="sources">
            <div className="section-heading compact">
              <div>
                <p className="eyebrow">Sources</p>
                <h2>来源依据</h2>
              </div>
            </div>

            {answer?.citations.length ? (
              <div className="source-list">
                {answer.citations.map((citation) => (
                  <article className="source-card" key={citation.excerptId}>
                    <div className="source-title">
                      <strong>{citation.title}</strong>
                      <span>{citation.department}</span>
                    </div>
                    <p>{citation.excerpt}</p>
                    <footer>
                      <span>{citation.version}</span>
                      <span>{citation.effectiveDate}</span>
                    </footer>
                  </article>
                ))}
              </div>
            ) : (
              <div className="source-list">
                {roleSources.map((source) => (
                  <article className="source-card muted" key={source.id}>
                    <div className="source-title">
                      <strong>{source.title}</strong>
                      <span>{source.department}</span>
                    </div>
                    <p>{source.summary}</p>
                    <footer>
                      <span>{source.version}</span>
                      <span>{source.sensitivity}</span>
                    </footer>
                  </article>
                ))}
              </div>
            )}
          </aside>

          <section className="draft-panel" id="draft">
            <div className="section-heading">
              <div>
                <p className="eyebrow">Draft Workspace</p>
                <h2>可审核草稿</h2>
              </div>
              <select
                aria-label="草稿类型"
                value={draftKind}
                onChange={(event) => setDraftKind(event.target.value as DraftKind)}
              >
                {draftKindOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>

            {draft ? (
              <article className="draft-document">
                <div className="draft-alert">
                  <AlertTriangle aria-hidden="true" />
                  <span>待人工审核，不得直接作为正式通知或决定。</span>
                </div>
                <h3>{draft.title}</h3>
                <pre>{draft.body}</pre>
                <div className="assumptions">
                  {draft.assumptions.map((item) => (
                    <span key={item}>{item}</span>
                  ))}
                </div>
                <button onClick={saveDraftTask} type="button">
                  <CalendarCheck2 aria-hidden="true" />
                  加入任务台账
                </button>
              </article>
            ) : (
              <div className="empty-state horizontal">
                <FileEdit aria-hidden="true" />
                <p>先完成一次来源问答，再生成通知、会议材料、教案、作业或量规草稿。</p>
              </div>
            )}
          </section>

          <section className="task-panel" id="tasks">
            <div className="section-heading">
              <div>
                <p className="eyebrow">Task Ledger</p>
                <h2>教学任务台账</h2>
              </div>
              <span className="badge">{roleTasks.length} 项</span>
            </div>

            <div className="task-list">
              {roleTasks.map((task) => (
                <article className="task-card" key={task.id}>
                  <div>
                    <span className={`status ${task.status}`}>{statusLabels[task.status]}</span>
                    <strong>{task.title}</strong>
                  </div>
                  <p>{task.detail}</p>
                  <footer>
                    <span>{task.createdFrom}</span>
                    {task.dueAt ? <span>截止 {task.dueAt}</span> : <span>待定截止时间</span>}
                    <span>{task.sourceIds.length} 个来源</span>
                  </footer>
                </article>
              ))}
            </div>
          </section>
        </div>
      </section>
    </main>
  );
}

function confidenceLabel(confidence: CampusAnswer["confidence"]) {
  if (confidence === "grounded") return "来源充分";
  if (confidence === "partial") return "部分依据";
  return "依据不足";
}
