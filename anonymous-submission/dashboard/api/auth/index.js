const { ensureTables, passwordsTable, ANNOTATORS } = require("../shared");

module.exports = async function (context, req) {
  await ensureTables();
  const { name, password } = req.body || {};

  if (!name || !password) {
    context.res = { status: 400, body: { error: "name and password required" }, headers: { "Content-Type": "application/json" } };
    return;
  }

  if (!ANNOTATORS.includes(name)) {
    context.res = { status: 403, body: { error: "unknown annotator" }, headers: { "Content-Type": "application/json" } };
    return;
  }

  const table = passwordsTable();

  try {
    const entity = await table.getEntity("auth", name);
    if (entity.password === password) {
      context.res = { body: { ok: true, name }, headers: { "Content-Type": "application/json" } };
    } else {
      context.res = { status: 401, body: { error: "wrong password" }, headers: { "Content-Type": "application/json" } };
    }
  } catch (e) {
    if (e.statusCode === 404) {
      await table.createEntity({ partitionKey: "auth", rowKey: name, password });
      context.res = { body: { ok: true, name, created: true }, headers: { "Content-Type": "application/json" } };
    } else {
      context.res = { status: 500, body: { error: e.message }, headers: { "Content-Type": "application/json" } };
    }
  }
};
