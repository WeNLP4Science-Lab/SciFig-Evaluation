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

// Server-only mapping. Browser bundle only ever sees the aliases.
// Azure tables are keyed by real names (historical), so we translate at the API boundary.
const ALIAS_TO_REAL = {
  "Admin":  "Admin",
  "User 1": "Wei",
  "User 2": "Bana",
  "User 3": "Ananya",
  "User 4": "Paul",
  "User 5": "John",
  "User 6": "Benedict",
  "User 7": "Anthony",
  "User 8": "Dan",
};

const REAL_TO_ALIAS = Object.fromEntries(
  Object.entries(ALIAS_TO_REAL).map(([alias, real]) => [real, alias])
);

const ALIASES = Object.keys(ALIAS_TO_REAL);

function toReal(alias) {
  return ALIAS_TO_REAL[alias] || null;
}

function toAlias(real) {
  return REAL_TO_ALIAS[real] || real;
}

function isKnownAlias(alias) {
  return ALIAS_TO_REAL.hasOwnProperty(alias);
}

module.exports = {
  ensureTables,
  passwordsTable: () => getTableClient("passwords"),
  annotationsTable: () => getTableClient("annotations"),
  reviewsTable: () => getTableClient("reviews"),
  ALIASES,
  toReal,
  toAlias,
  isKnownAlias,
};
