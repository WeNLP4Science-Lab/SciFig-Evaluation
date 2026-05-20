const { TableClient, AzureNamedKeyCredential } = require("@azure/data-tables");

const account = process.env.STORAGE_ACCOUNT_NAME;
const key = process.env.STORAGE_ACCOUNT_KEY;

function getTableClient(tableName) {
  const credential = new AzureNamedKeyCredential(account, key);
  const url = `https://${account}.table.core.windows.net`;
  return new TableClient(url, tableName, credential);
}

let initialized = false;
async function ensureTables() {
  if (initialized) return;
  try { await getTableClient("passwords").createTable(); } catch (e) { if (e.statusCode !== 409) throw e; }
  try { await getTableClient("annotations").createTable(); } catch (e) { if (e.statusCode !== 409) throw e; }
  try { await getTableClient("reviews").createTable(); } catch (e) { if (e.statusCode !== 409) throw e; }
  initialized = true;
}

const ANNOTATORS = ["Admin", "Wei", "Bana", "Ananya", "Paul", "John", "Benedict", "Anthony", "Dan"];

module.exports = {
  ensureTables,
  passwordsTable: () => getTableClient("passwords"),
  annotationsTable: () => getTableClient("annotations"),
  reviewsTable: () => getTableClient("reviews"),
  ANNOTATORS,
};
