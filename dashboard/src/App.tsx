import { Routes, Route } from 'react-router-dom'
import Landing from './pages/Landing'
import JudgeReview from './pages/JudgeReview'
import DatasetBrowser from './pages/DatasetBrowser'
import SectionSelector from './pages/SectionSelector'
import Analytics from './pages/Analytics'
import AdversarialBrowser from './pages/AdversarialBrowser'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/dataset" element={<DatasetBrowser />} />
      <Route
        path="/evaluation"
        element={
          <SectionSelector
            title="Evaluation Review"
            subtitle="Review MQM judge evaluations with annotated error spans across models"
            fullPath="/evaluation/full"
            samplePath="/evaluation/sample"
            fullDesc="Complete dataset evaluation across all figures and models"
            sampleDesc="Curated 120-figure sample with human evaluation comparison"
          />
        }
      />
      <Route path="/evaluation/full" element={<JudgeReview manifestFile="manifest_full.json" title="Full Evaluation" />} />
      <Route path="/evaluation/sample" element={<JudgeReview manifestFile="manifest_sample.json" title="Sample Evaluation" />} />
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
      <Route path="/adversarial" element={<AdversarialBrowser />} />
    </Routes>
  )
}
