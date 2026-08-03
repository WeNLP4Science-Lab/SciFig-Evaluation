const fs = require("fs");
const path = require("path");
const {
  AlignmentType,
  Document,
  HeadingLevel,
  LevelFormat,
  Packer,
  PageBreak,
  Paragraph,
  TextRun,
  ShadingType,
} = require("docx");

const repo = path.resolve(__dirname, "../..");
const dataPath = path.join(repo, "tmp", "docx_template", "reviews.json");
const outputDir = path.join(repo, "output", "docx");
const outputPath = path.join(outputDir, "scifig_eval_reviewer_responses.docx");
const reviews = JSON.parse(fs.readFileSync(dataPath, "utf8"));
fs.mkdirSync(outputDir, { recursive: true });

const RED = "8C1B13";
const DARK = "333333";
const GREY = "666666";

function title(text, pageBreakBefore = false) {
  return new Paragraph({
    pageBreakBefore,
    keepNext: true,
    spacing: { before: 0, after: 60 },
    children: [new TextRun({ text, bold: true, color: "374151", size: 24, font: "Arial" })],
  });
}

function officialLine(review) {
  return new Paragraph({
    keepNext: true,
    spacing: { after: 100 },
    children: [
      new TextRun({ text: `Official Review by Reviewer ${review.id}`, color: GREY, size: 21, font: "Arial" }),
      new TextRun({ text: `${review.date}`, color: GREY, size: 21, font: "Arial" }),
      new TextRun({ text: " Program Chairs, Senior Area Chairs, Area Chairs, Reviewers Submitted, Reviewer ", color: GREY, size: 21, font: "Arial" }),
      new TextRun({ text: `${review.id}, Authors`, color: GREY, size: 21, font: "Arial" }),
    ],
  });
}

function sectionHeading(text) {
  return new Paragraph({
    keepNext: true,
    spacing: { before: 100, after: 40 },
    children: [new TextRun({ text: `${text}:`, bold: true, color: RED, size: 22, font: "Arial" })],
  });
}

function body(text, options = {}) {
  return new Paragraph({
    spacing: { after: 80, line: 276, lineRule: "auto" },
    indent: options.indent ? { left: options.indent } : undefined,
    numbering: options.numbering,
    children: [new TextRun({ text, color: DARK, size: 21, font: "Arial" })],
  });
}

function response(text) {
  const parts = text.split("\n\n");
  return parts.map((part, i) => new Paragraph({
    spacing: { before: i ? 40 : 20, after: i === parts.length - 1 ? 100 : 30, line: 276, lineRule: "auto" },
    indent: { left: 900, right: 180 },
    children: [new TextRun({
      text: `${i === 0 ? "A: " : ""}${part}`,
      color: DARK,
      size: 21,
      font: "Arial",
      shading: { fill: "B6D7A8", type: ShadingType.CLEAR },
    })],
  }));
}

function meta(label, value, keepNext = false) {
  return new Paragraph({
    keepNext,
    spacing: { after: 35, line: 276, lineRule: "auto" },
    children: [
      new TextRun({ text: `${label}:`, bold: true, color: RED, size: 21, font: "Arial" }),
      new TextRun({ text: ` ${value}`, color: DARK, size: 21, font: "Arial" }),
    ],
  });
}

const children = [];
reviews.forEach((review, reviewIndex) => {
  children.push(title(`Official Review of Submission14568 by Reviewer ${review.id}`, reviewIndex > 0));
  children.push(officialLine(review));
  children.push(sectionHeading("Paper Summary"));
  children.push(body(review.summary));
  children.push(sectionHeading("Summary Of Strengths"));
  review.strengths.forEach((strength) => children.push(body(strength, {
    numbering: { reference: `strengths-${reviewIndex}`, level: 0 },
  })));

  let currentSection = null;
  let weaknessNumber = 0;
  let commentNumber = 0;
  review.items.forEach(([section, concern, answer]) => {
    if (section && section !== currentSection) {
      currentSection = section;
      children.push(sectionHeading(section));
    }
    const isComment = currentSection === "Comments Suggestions And Typos";
    const ref = isComment ? `comments-${reviewIndex}` : `weaknesses-${reviewIndex}`;
    if (isComment) commentNumber += 1; else weaknessNumber += 1;
    children.push(body(concern, { numbering: { reference: ref, level: 0 } }));
    if (answer) children.push(...response(answer));
  });

  review.meta.forEach(([label, value], metaIndex) => children.push(meta(label, value, metaIndex < review.meta.length - 1)));
});

const numberingConfigs = [];
reviews.forEach((_, i) => {
  for (const name of ["strengths", "weaknesses", "comments"]) {
    numberingConfigs.push({
      reference: `${name}-${i}`,
      levels: [{
        level: 0,
        format: LevelFormat.DECIMAL,
        text: "%1.",
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } },
      }],
    });
  }
});

const doc = new Document({
  creator: "SciFig-Eval Authors",
  title: "SciFig-Eval Reviewer Responses",
  styles: {
    default: { document: { run: { font: "Arial", size: 21, color: DARK }, paragraph: { spacing: { line: 276, lineRule: "auto" } } } },
    paragraphStyles: [
      { id: "Normal", name: "Normal", quickFormat: true, run: { font: "Arial", size: 21, color: DARK } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: "Arial", size: 24, bold: true, color: RED },
        paragraph: { spacing: { before: 100, after: 40 }, outlineLevel: 0 } },
    ],
  },
  numbering: { config: numberingConfigs },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440, header: 720, footer: 720 },
      },
    },
    children,
  }],
});

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync(outputPath, buffer);
  process.stdout.write(`${outputPath}\n`);
});
