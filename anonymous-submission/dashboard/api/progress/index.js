const { ensureTables, annotationsTable, toAlias } = require("../shared");

module.exports = async function (context, req) {
  await ensureTables();
  const table = annotationsTable();

  const progress = {};
  for await (const entity of table.listEntities()) {
    const fig = entity.partitionKey;
    const alias = toAlias(entity.annotator);
    if (!progress[fig]) progress[fig] = {};
    if (!progress[fig][alias]) progress[fig][alias] = 0;
    progress[fig][alias]++;
  }

  context.res = { body: progress, headers: { "Content-Type": "application/json" } };
};
