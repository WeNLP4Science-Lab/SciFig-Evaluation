/**
 * Base URL for serving figure images.
 * In development, figures are served locally from public/figures/.
 * In production, figures are served from Azure Blob Storage.
 */
export const FIGURES_BASE_URL = import.meta.env.PROD
  ? 'https://scifigfigures.blob.core.windows.net/figures'
  : `${import.meta.env.BASE_URL}figures`

/**
 * Azure Blob Storage config for saving/loading capability questions.
 * In production, questions are read/written to blob storage.
 * In development, questions are read from local files and saved via Vite API.
 */
const BLOB_SAS_TOKEN = 'se=2027-04-15T00%3A00%3A00Z&sp=rwl&spr=https&sv=2026-02-06&sr=c&sig=xO4yY3qdzgxakEcoz4olYoiCBe9Cq7YN5HfkHtYNRCQ%3D'
export const QUESTIONS_BLOB_URL = `https://scifigfigures.blob.core.windows.net/data/capability_questions.json`
export const QUESTIONS_BLOB_WRITE_URL = `${QUESTIONS_BLOB_URL}?${BLOB_SAS_TOKEN}`

export const HALLUCINATION_BLOB_URL = `https://scifigfigures.blob.core.windows.net/data/hallucination_probes.json`
export const HALLUCINATION_BLOB_WRITE_URL = `${HALLUCINATION_BLOB_URL}?${BLOB_SAS_TOKEN}`
