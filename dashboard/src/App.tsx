import { Routes, Route } from 'react-router-dom'
import Landing from './pages/Landing'
import JudgeReview from './pages/JudgeReview'
import DatasetBrowser from './pages/DatasetBrowser'
import DatasetSelector from './pages/DatasetSelector'
import SectionSelector from './pages/SectionSelector'
import EvaluationSelector from './pages/EvaluationSelector'
import Analytics from './pages/Analytics'
import AdversarialSampleBrowser from './pages/AdversarialSampleBrowser'
import AdversarialEvaluation from './pages/AdversarialEvaluation'
import InferableBlurs from './pages/InferableBlurs'
import AdversarialResults from './pages/AdversarialResults'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />

      {/* Dataset */}
      <Route path="/dataset" element={<DatasetSelector />} />
      <Route path="/dataset/full" element={<DatasetBrowser />} />
      <Route path="/dataset/sample-120" element={<AdversarialSampleBrowser manifestFile="adversarial_120.json" title="120 Sample" />} />
      <Route path="/dataset/adversarial-subset" element={<AdversarialSampleBrowser manifestFile="adversarial_experiments.json" title="Adversarial Subset (45)" />} />
      <Route path="/dataset/inferable-blurs" element={<InferableBlurs />} />

      {/* Evaluation */}
      <Route path="/evaluation" element={<EvaluationSelector />} />
      <Route path="/evaluation/full" element={<JudgeReview manifestFile="manifest_full.json" title="Full Evaluation" />} />
      <Route path="/evaluation/sample" element={<JudgeReview manifestFile="manifest_sample.json" title="Sample Evaluation" />} />
      <Route path="/evaluation/adversarial" element={<AdversarialEvaluation />} />
      <Route path="/evaluation/adversarial-results" element={<AdversarialResults />} />

      {/* Analytics */}
      <Route
        path="/analytics"
        element={
          <SectionSelector
            title="Analytics"
            subtitle="Cross-model and cross-judge comparison charts, error analysis, and language breakdown"
            fullPath="/analytics/full"
            samplePath="/analytics/sample"
            fullDesc="Aggregate analytics across the complete evaluation dataset"
            sampleDesc="Analytics for the curated 120-figure sample"
          />
        }
      />
      <Route path="/analytics/full" element={<Analytics manifestFile="manifest_full.json" title="Full Analytics" />} />
      <Route path="/analytics/sample" element={<Analytics manifestFile="manifest_sample.json" title="Sample Analytics" />} />
    </Routes>
  )
}
