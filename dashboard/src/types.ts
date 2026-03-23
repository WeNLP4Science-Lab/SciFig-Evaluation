export interface MQMError {
  category: string
  sub_type: string
  severity: string
  weight: number
  text_span: string | null
  evidence: string
}

export interface JudgeResult {
  figure_key: string
  model_name: string
  figure_type: string
  judge_type: string
  judge_model: string
  errors: MQMError[]
  mqm_score: number
  total_penalty: number
  error_count: number
}

export type JudgeResults = {
  reference_free?: JudgeResult
  reference_only?: JudgeResult
  reference_with_image?: JudgeResult
}

export interface FigureEval {
  figure_key: string
  model_name: string
  figure_type: string
  annotation: string
  caption: string
  paper_title: string
  subfolder: string
  figure_image: string
  judges: Record<string, JudgeResults>
}

export interface DataManifest {
  generated_at: string
  judge_models: string[]
  models: string[]
  subfolders: string[]
  figures: FigureEval[]
}

export type JudgeType = 'reference_free' | 'reference_only' | 'reference_with_image'

export const JUDGE_LABELS: Record<JudgeType, string> = {
  reference_free: 'Reference Free',
  reference_only: 'Reference Only',
  reference_with_image: 'Reference + Image',
}

// M3-aligned category colors
export const CATEGORY_COLORS: Record<string, { main: string; container: string; onContainer: string }> = {
  'Accuracy': {
    main: '#e8403f',
    container: 'rgba(232,64,63,0.12)',
    onContainer: '#f2b8b5',
  },
  'Completeness': {
    main: '#e88d3f',
    container: 'rgba(232,141,63,0.12)',
    onContainer: '#ffd9b3',
  },
  'Clarity and Readability': {
    main: '#4caf7c',
    container: 'rgba(76,175,124,0.12)',
    onContainer: '#b4e8cb',
  },
}

export const CATEGORY_COLORS_LIGHT: Record<string, { main: string; container: string; onContainer: string }> = {
  'Accuracy': {
    main: '#ba1a1a',
    container: 'rgba(186,26,26,0.08)',
    onContainer: '#410e0b',
  },
  'Completeness': {
    main: '#b3590a',
    container: 'rgba(179,89,10,0.08)',
    onContainer: '#3c1500',
  },
  'Clarity and Readability': {
    main: '#1a6b3e',
    container: 'rgba(26,107,62,0.08)',
    onContainer: '#002110',
  },
}

export const SEVERITY_COLORS: Record<string, { bg: string; text: string; border: string }> = {
  'Major': { bg: 'rgba(232,64,63,0.12)', text: '#f2b8b5', border: 'rgba(232,64,63,0.2)' },
  'Minor': { bg: 'rgba(232,180,63,0.12)', text: '#ffd9b3', border: 'rgba(232,180,63,0.2)' },
}

export const SEVERITY_COLORS_LIGHT: Record<string, { bg: string; text: string; border: string }> = {
  'Major': { bg: 'rgba(186,26,26,0.08)', text: '#ba1a1a', border: 'rgba(186,26,26,0.15)' },
  'Minor': { bg: 'rgba(179,89,10,0.08)', text: '#b3590a', border: 'rgba(179,89,10,0.15)' },
}

export interface DatasetAnnotation {
  annotation_language: string
  annotation: string
  annotated_by: number
  figure_type: string
}

export interface DatasetFigure {
  figure_key: string
  subfolder: string
  paper_title: string
  paper_language: string
  caption: string
  figure_type: string
  figure_image: string
  annotations: DatasetAnnotation[]
}

export interface DatasetManifest {
  generated_at: string
  subfolders: string[]
  subfolder_counts: Record<string, number>
  figures: DatasetFigure[]
}
