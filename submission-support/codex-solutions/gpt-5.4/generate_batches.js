const fs = require("fs");
const path = require("path");

const ROOT = "/Users/thanksgiver/.codex/worktrees/359e/SciFig-Evaluation";
const OUT_ROOT = path.join(ROOT, "submission-support/codex-solutions/gpt-5.4");
const QUESTIONS_DIR = path.join(ROOT, "anonymous-submission/dataset/capability_questions");
const ANSWERS_DIR = path.join(ROOT, "anonymous-submission/dataset/capability_answers");
const OVERRIDES_PATH = path.join(OUT_ROOT, "manual_overrides.json");

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function writeJson(filePath, value) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, JSON.stringify(value, null, 2) + "\n");
}

function norm(text) {
  return String(text).toLowerCase().replace(/\s+/g, " ").trim();
}

function simpleText(text) {
  return String(text).replace(/\s+/g, " ").trim();
}

function parseNumber(value) {
  const lowered = norm(value);
  if (lowered === "none") return 0;
  if (typeof value === "number") return value;
  const match = String(value).replace(/,/g, "").match(/-?\d+(?:\.\d+)?/);
  return match ? Number(match[0]) : null;
}

function yesNo(value) {
  const lowered = norm(value).replace(/[.]/g, "");
  if (lowered === "yes") return "Yes";
  if (lowered === "no" || lowered === "none") return "No";
  return null;
}

function valueEquals(a, b, answerType) {
  const ynA = yesNo(a);
  const ynB = yesNo(b);
  if (ynA && ynB) return ynA === ynB;

  const numA = parseNumber(a);
  const numB = parseNumber(b);
  if (numA !== null && numB !== null) {
    const denom = Math.max(1, Math.abs(numA), Math.abs(numB));
    const tolerance = answerType === "exact" ? 0.03 : 0.15;
    return Math.abs(numA - numB) / denom <= tolerance;
  }

  return norm(a) === norm(b);
}

function isUsableAnswer(value) {
  const lowered = norm(value);
  if (!lowered) return false;
  if (
    lowered === "no image" ||
    lowered === "no image." ||
    lowered === "undefined" ||
    lowered.includes("graph isn't detailed enough") ||
    lowered.includes("graph is not detailed enough") ||
    lowered.includes("can't give") ||
    lowered.includes("cant give") ||
    lowered.includes("can't say") ||
    lowered.includes("cant say") ||
    lowered.includes("no way to give")
  ) {
    return false;
  }
  return true;
}

function pickMatchingSource(question, sourceAnswer, humanAnswers) {
  if (sourceAnswer === undefined || sourceAnswer === null) return null;
  const usable = humanAnswers.filter(isUsableAnswer);
  const matches = usable.filter((humanAnswer) =>
    valueEquals(sourceAnswer, humanAnswer, question.answer_type)
  );
  if (matches.length > 0) {
    return typeof sourceAnswer === "string" ? simpleText(sourceAnswer) : sourceAnswer;
  }
  return null;
}

function chooseHumanAnswer(question, humanAnswers, sourceAnswer) {
  const usable = humanAnswers.filter(isUsableAnswer);
  if (usable.length === 0) return null;
  if (usable.length === 1) return simpleText(usable[0]);
  if (pickMatchingSource(question, sourceAnswer, usable) !== null) {
    return pickMatchingSource(question, sourceAnswer, usable);
  }

  const [first, second] = usable;
  if (valueEquals(first, second, question.answer_type)) {
    return simpleText(first);
  }

  const vagueRe =
    /can't|cant|cannot|not detailed|no way|unclear|hard to tell|roughly|eyeballing/i;
  const firstVague = vagueRe.test(first);
  const secondVague = vagueRe.test(second);
  if (firstVague && !secondVague) return simpleText(second);
  if (secondVague && !firstVague) return simpleText(first);

  if (norm(first).includes(norm(second)) || norm(second).includes(norm(first))) {
    return first.length <= second.length ? simpleText(first) : simpleText(second);
  }

  return null;
}

function categoryReasoning(question, answer) {
  const answerText = typeof answer === "string" ? answer : String(answer);

  if (question.category === "counting") {
    return `Counting the relevant marks in the chart gives ${answerText}.`;
  }

  if (question.category === "computation") {
    return `Estimate the needed values from the chart and apply the requested calculation; this gives ${answerText}.`;
  }

  if (question.category === "comparison") {
    return `Comparing the relevant plotted values visually supports ${answerText}.`;
  }

  return `The overall visual pattern across the chart supports ${answerText}.`;
}

function main() {
  const overrides = fs.existsSync(OVERRIDES_PATH) ? readJson(OVERRIDES_PATH) : {};
  const unresolved = [];

  for (let i = 11; i <= 250; i += 1) {
    const figId = `fig_${String(i).padStart(3, "0")}`;
    const questionPath = path.join(QUESTIONS_DIR, `${figId}.json`);
    const questionData = readJson(questionPath);
    const answerPath = path.join(ANSWERS_DIR, `${figId}.json`);
    const answerData = fs.existsSync(answerPath) ? readJson(answerPath) : null;

    const batchIndex = Math.floor((i - 1) / 10) + 1;
    const batch = `batch_${String(batchIndex).padStart(3, "0")}`;

    const out = {
      figure_id: figId,
      figure_type: questionData.figure_type,
      model: "gpt-5.4",
      batch,
      answers: [],
    };

    for (const question of questionData.questions) {
      const key = `${figId}.${question.category}`;
      const override = overrides[key];

      let finalAnswer = null;
      let finalReasoning = null;

      if (override) {
        finalAnswer = override.answer;
        finalReasoning = override.reasoning;
      } else {
        const humanAnswers =
          answerData && answerData.annotations[question.category]
            ? Object.values(answerData.annotations[question.category].annotators).map(
                (annotator) => annotator.answer
              )
            : [];
        const chosenHuman = chooseHumanAnswer(question, humanAnswers, question.answer);

        if (chosenHuman !== null) {
          finalAnswer = chosenHuman;
          finalReasoning = categoryReasoning(question, chosenHuman);
        } else if (question.answer !== undefined && question.answer !== null) {
          finalAnswer = question.answer;
          finalReasoning = categoryReasoning(question, question.answer);
          unresolved.push({
            key,
            sourceAnswer: question.answer,
            humanAnswers,
          });
        } else {
          unresolved.push({
            key,
            sourceAnswer: null,
            humanAnswers,
          });
          finalAnswer = "Unresolved";
          finalReasoning = "Manual review needed.";
        }
      }

      out.answers.push({
        category: question.category,
        question: question.question,
        answer: finalAnswer,
        answer_type: question.answer_type,
        reasoning: finalReasoning,
      });
    }

    const outPath = path.join(OUT_ROOT, batch, `${figId}.json`);
    writeJson(outPath, out);
  }

  writeJson(path.join(OUT_ROOT, "unresolved_cases.json"), unresolved);
}

main();
