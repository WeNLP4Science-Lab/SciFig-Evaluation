const { ensureTables, annotationsTable } = require("../shared");

module.exports = async function (context, req) {
  await ensureTables();
  const table = annotationsTable();

  const progress = {};
  for await (const entity of table.listEntities()) {
    const fig = entity.partitionKey;
    if (!progress[fig]) progress[fig] = {};
    if (!progress[fig][entity.annotator]) progress[fig][entity.annotator] = 0;
    progress[fig][entity.annotator]++;
  }

  context.res = { body: progress, headers: { "Content-Type": "application/json" } };
};
