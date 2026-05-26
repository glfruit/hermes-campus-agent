import { answerCampusQuestion } from "@/lib/campus/knowledge";
import { createDraft } from "@/lib/campus/drafts";
import type {
  CampusAgentInput,
  CampusAgentOutput,
  CampusDraftInput,
  CampusDraftOutput,
} from "@/lib/campus/types";

export interface HermesBridge {
  ask(input: CampusAgentInput): Promise<CampusAgentOutput>;
  draft(input: CampusDraftInput): Promise<CampusDraftOutput>;
}

export class LocalHermesBridge implements HermesBridge {
  async ask(input: CampusAgentInput): Promise<CampusAgentOutput> {
    return answerCampusQuestion(input.question, input.role);
  }

  async draft(input: CampusDraftInput): Promise<CampusDraftOutput> {
    return createDraft(input);
  }
}

export const hermesBridge = new LocalHermesBridge();
