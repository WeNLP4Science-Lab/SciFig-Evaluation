const { ensureTables, reviewsTable, passwordsTable, isKnownAlias, toReal, toAlias } = require("../shared");

module.exports = async function (context, req) {
  await ensureTables();

  if (req.method === "GET") {
    const figureId = req.query.figure_id;
    if (!figureId) {
      context.res = { status: 400, body: { error: "figure_id required" }, headers: { "Content-Type": "application/json" } };
      return;
    }

    const table = reviewsTable();
    const results = [];
    const filter = `PartitionKey eq '${figureId}'`;

    for await (const entity of table.listEntities({ queryOptions: { filter } })) {
      results.push({
        figure_id: entity.partitionKey,
        review_type: entity.reviewType,
        annotator: toAlias(entity.annotator),
        // Metadata reviews
        pdf_page: entity.pdfPage || null,
        figure_number: entity.figureNumber || null,
        caption: entity.captionEdit || null,
        // Adversarial reviews
        probe_type: entity.probeType || null,
        status: entity.status || null,
        new_blur_target: entity.newBlurTarget || null,
        new_question: entity.newQuestion || null,
        notes: entity.notes || null,
        timestamp: entity.timestamp,
      });
    }

    context.res = { body: results, headers: { "Content-Type": "application/json" } };
    return;
  }

  // POST
  const { figure_id, annotator, password, review_type, ...fields } = req.body || {};

  if (!figure_id || !annotator || !password || !review_type) {
    context.res = { status: 400, body: { error: "figure_id, annotator, password, and review_type required" }, headers: { "Content-Type": "application/json" } };
    return;
  }

  if (!isKnownAlias(annotator)) {
    context.res = { status: 403, body: { error: "unknown annotator" }, headers: { "Content-Type": "application/json" } };
    return;
  }

  const realName = toReal(annotator);

  // Verify password
  const pw = passwordsTable();
  try {
    const entity = await pw.getEntity("auth", realName);
    if (entity.password !== password) {
      context.res = { status: 401, body: { error: "wrong password" }, headers: { "Content-Type": "application/json" } };
      return;
    }
  } catch {
    context.res = { status: 401, body: { error: "not registered" }, headers: { "Content-Type": "application/json" } };
    return;
  }

  const table = reviewsTable();
  const rowKey = `${review_type}_${realName}`;

  const entity = {
    partitionKey: figure_id,
    rowKey,
    reviewType: review_type,
    annotator: realName,
    pdfPage: fields.pdf_page || "",
    figureNumber: fields.figure_number || "",
    captionEdit: fields.caption || "",
    probeType: fields.probe_type || "",
    status: fields.status || "",
    newBlurTarget: fields.new_blur_target || "",
    newQuestion: fields.new_question || "",
    notes: fields.notes || "",
  };

  await table.upsertEntity(entity);

  context.res = {
    body: { ok: true, figure_id, review_type, annotator },
    headers: { "Content-Type": "application/json" },
  };
};
