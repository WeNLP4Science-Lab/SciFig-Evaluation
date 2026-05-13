const { ensureTables, annotationsTable, passwordsTable, ANNOTATORS } = require("../shared");

module.exports = async function (context, req) {
  await ensureTables();

  if (req.method === "GET") {
    const figureId = req.query.figure_id;
    if (!figureId) {
      context.res = { status: 400, body: { error: "figure_id required" }, headers: { "Content-Type": "application/json" } };
      return;
    }

    const table = annotationsTable();
    const results = [];
    const filter = `PartitionKey eq '${figureId}'`;

    for await (const entity of table.listEntities({ queryOptions: { filter } })) {
      results.push({
        figure_id: entity.partitionKey,
        category: entity.category,
        annotator: entity.annotator,
        answer: entity.answer,
        edited_question: entity.editedQuestion || null,
        change_requested: entity.changeRequested === true,
        notes: entity.notes || null,
        timestamp: entity.timestamp,
      });
    }

    context.res = { body: results, headers: { "Content-Type": "application/json" } };
    return;
  }

  // POST
  const { figure_id, category, annotator, password, answer, edited_question, notes } = req.body || {};

  if (!figure_id || !category || !annotator || !password || answer === undefined) {
    context.res = { status: 400, body: { error: "figure_id, category, annotator, password, and answer required" }, headers: { "Content-Type": "application/json" } };
    return;
  }

  if (!ANNOTATORS.includes(annotator)) {
    context.res = { status: 403, body: { error: "unknown annotator" }, headers: { "Content-Type": "application/json" } };
    return;
  }

  // Verify password
  const pw = passwordsTable();
  try {
    const entity = await pw.getEntity("auth", annotator);
    if (entity.password !== password) {
      context.res = { status: 401, body: { error: "wrong password" }, headers: { "Content-Type": "application/json" } };
      return;
    }
  } catch {
    context.res = { status: 401, body: { error: "not registered" }, headers: { "Content-Type": "application/json" } };
    return;
  }

  const table = annotationsTable();
  const rowKey = `${category}_${annotator}`;

  await table.upsertEntity({
    partitionKey: figure_id,
    rowKey,
    category,
    annotator,
    answer: String(answer),
    editedQuestion: edited_question || "",
    changeRequested: !!edited_question,
    notes: notes || "",
  });

  context.res = {
    body: { ok: true, figure_id, category, annotator, change_requested: !!edited_question },
    headers: { "Content-Type": "application/json" },
  };
};
