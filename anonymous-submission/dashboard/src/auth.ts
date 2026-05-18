export const ANNOTATORS = ["Admin", "Wei", "Bana", "Ananya", "Paul", "John", "Benedict", "Anthony", "Dan"] as const

// Figure assignments per annotator. null = see all (Admin).
const ANNOTATOR_FIGURES: Record<string, string[] | null> = {
  Admin: null,
  Ananya: ["fig_001","fig_002","fig_003","fig_004","fig_005","fig_006","fig_007","fig_008","fig_100","fig_101","fig_102","fig_103","fig_104","fig_105","fig_106","fig_107","fig_199","fig_200","fig_201","fig_202"],
  Bana: ["fig_009","fig_010","fig_011","fig_012","fig_013","fig_014","fig_015","fig_016","fig_017","fig_018","fig_019","fig_020","fig_092","fig_093","fig_094","fig_095","fig_096","fig_097","fig_098","fig_099","fig_108","fig_109","fig_110","fig_111","fig_112","fig_113","fig_114","fig_115","fig_116","fig_117","fig_118","fig_119","fig_191","fig_192","fig_193","fig_194","fig_195","fig_196","fig_197","fig_198","fig_203","fig_204","fig_205","fig_206","fig_207","fig_208","fig_247","fig_248","fig_249","fig_250"],
  Wei: ["fig_021","fig_022","fig_023","fig_024","fig_025","fig_026","fig_027","fig_028","fig_029","fig_030","fig_031","fig_032","fig_033","fig_034","fig_035","fig_036","fig_037","fig_038","fig_039","fig_040","fig_120","fig_121","fig_122","fig_123","fig_124","fig_125","fig_126","fig_127","fig_128","fig_129","fig_130","fig_131","fig_132","fig_133","fig_134","fig_135","fig_136","fig_137","fig_138","fig_139","fig_209","fig_210","fig_211","fig_212","fig_213","fig_214","fig_215","fig_216","fig_217","fig_218"],
  Paul: ["fig_001","fig_002","fig_003","fig_004","fig_005","fig_006","fig_007","fig_008","fig_009","fig_010","fig_011","fig_012","fig_013","fig_014","fig_015","fig_016","fig_017","fig_018","fig_021","fig_022","fig_023","fig_024","fig_025","fig_026","fig_027","fig_028","fig_029","fig_030","fig_041","fig_042","fig_043","fig_044","fig_045","fig_046","fig_047","fig_048","fig_049","fig_050","fig_051","fig_052","fig_053","fig_054","fig_055","fig_056","fig_057","fig_058","fig_059","fig_060","fig_061","fig_062","fig_063","fig_064","fig_065","fig_066","fig_067","fig_068","fig_069","fig_070","fig_071","fig_072","fig_073","fig_074","fig_075","fig_076","fig_077","fig_078","fig_079","fig_080","fig_081","fig_082","fig_083","fig_084","fig_085","fig_086","fig_087","fig_088","fig_089","fig_090","fig_091","fig_100","fig_101","fig_102","fig_103","fig_104","fig_105","fig_106","fig_107","fig_108","fig_109","fig_110","fig_111","fig_112","fig_113","fig_114","fig_115","fig_116","fig_117","fig_120","fig_121","fig_122","fig_123","fig_124","fig_125","fig_126","fig_127","fig_128","fig_129","fig_140","fig_141","fig_142","fig_143","fig_144","fig_145","fig_146","fig_147","fig_148","fig_149","fig_150","fig_151","fig_152","fig_153","fig_154","fig_155","fig_156","fig_157","fig_158","fig_159","fig_160","fig_161","fig_162","fig_163","fig_164","fig_165","fig_166","fig_167","fig_168","fig_169","fig_170","fig_171","fig_172","fig_173","fig_174","fig_175","fig_176","fig_177","fig_178","fig_179","fig_180","fig_181","fig_182","fig_183","fig_184","fig_185","fig_186","fig_187","fig_188","fig_189","fig_190","fig_199","fig_200","fig_201","fig_202","fig_203","fig_204","fig_205","fig_206","fig_207","fig_209","fig_210","fig_211","fig_212","fig_213","fig_219","fig_220","fig_221","fig_222","fig_223","fig_224","fig_225","fig_226","fig_227","fig_228","fig_229","fig_230","fig_231","fig_232","fig_233","fig_234","fig_235","fig_236","fig_237","fig_238","fig_239","fig_240","fig_241","fig_242","fig_243","fig_244","fig_245","fig_246"],
  John: ["fig_001","fig_002","fig_003","fig_004","fig_005","fig_006","fig_007","fig_008","fig_009","fig_010","fig_011","fig_012","fig_013","fig_014","fig_015","fig_016","fig_017","fig_018","fig_021","fig_022","fig_100","fig_101","fig_102","fig_103","fig_104","fig_105","fig_106","fig_107","fig_108","fig_109","fig_110","fig_111","fig_112","fig_113","fig_114","fig_115","fig_116","fig_117","fig_120","fig_121","fig_199","fig_200","fig_201","fig_202","fig_203","fig_204","fig_205","fig_206","fig_207","fig_209"],
  Benedict: ["fig_023","fig_024","fig_025","fig_026","fig_027","fig_028","fig_029","fig_030","fig_041","fig_042","fig_043","fig_044","fig_045","fig_046","fig_047","fig_048","fig_049","fig_050","fig_051","fig_052","fig_122","fig_123","fig_124","fig_125","fig_126","fig_127","fig_128","fig_129","fig_140","fig_141","fig_142","fig_143","fig_144","fig_145","fig_146","fig_147","fig_148","fig_149","fig_150","fig_151","fig_210","fig_211","fig_212","fig_213","fig_219","fig_220","fig_221","fig_222","fig_223","fig_224"],
  Dan: ["fig_073","fig_074","fig_075","fig_076","fig_077","fig_078","fig_079","fig_080","fig_081","fig_082","fig_083","fig_084","fig_085","fig_086","fig_087","fig_088","fig_089","fig_090","fig_091","fig_172","fig_173","fig_174","fig_175","fig_176","fig_177","fig_178","fig_179","fig_180","fig_181","fig_182","fig_183","fig_184","fig_185","fig_186","fig_187","fig_188","fig_189","fig_190","fig_235","fig_236","fig_237","fig_238","fig_239","fig_240","fig_241","fig_242","fig_243","fig_244","fig_245","fig_246"],
  Anthony: ["fig_053","fig_054","fig_055","fig_056","fig_057","fig_058","fig_059","fig_060","fig_061","fig_062","fig_063","fig_064","fig_065","fig_066","fig_067","fig_068","fig_069","fig_070","fig_071","fig_072","fig_152","fig_153","fig_154","fig_155","fig_156","fig_157","fig_158","fig_159","fig_160","fig_161","fig_162","fig_163","fig_164","fig_165","fig_166","fig_167","fig_168","fig_169","fig_170","fig_171","fig_225","fig_226","fig_227","fig_228","fig_229","fig_230","fig_231","fig_232","fig_233","fig_234"],
}

export function figureInRange(figureId: string, name: string): boolean {
  const figs = ANNOTATOR_FIGURES[name]
  if (!figs) return true // Admin sees all
  return figs.includes(figureId)
}
export type Annotator = typeof ANNOTATORS[number]

export interface AuthState {
  name: Annotator
  password: string
}

const STORAGE_KEY = "scifig_auth"

export function isAnnotationMode(): boolean {
  return new URLSearchParams(window.location.search).has("annotate")
}

export function getSavedAuth(): AuthState | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return null
    const parsed = JSON.parse(raw)
    if (parsed.name && parsed.password) return parsed
    return null
  } catch {
    return null
  }
}

export function saveAuth(auth: AuthState) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(auth))
}

export function clearAuth() {
  localStorage.removeItem(STORAGE_KEY)
}

export async function loginAPI(name: string, password: string): Promise<{ ok: boolean; error?: string; created?: boolean }> {
  const res = await fetch("/api/auth", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, password }),
  })
  return res.json()
}

export interface AnnotationEntry {
  figure_id: string
  category: string
  annotator: string
  answer: string
  edited_question: string | null
  change_requested: boolean
  notes: string | null
  timestamp: string
}

export async function getAnnotations(figureId: string): Promise<AnnotationEntry[]> {
  const res = await fetch(`/api/annotations?figure_id=${figureId}`)
  return res.json()
}

export async function saveAnnotation(data: {
  figure_id: string
  category: string
  annotator: string
  password: string
  answer: string
  edited_question?: string
  notes?: string
}): Promise<{ ok: boolean; error?: string }> {
  const res = await fetch("/api/annotations", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
  return res.json()
}
