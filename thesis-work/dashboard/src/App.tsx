import { Routes, Route, Navigate } from 'react-router-dom'
import TabLayout from './components/TabLayout'
import JudgeReview from './pages/JudgeReview'
import DatasetBrowser from './pages/DatasetBrowser'
import Analytics from './pages/Analytics'
import AdversarialSampleBrowser from './pages/AdversarialSampleBrowser'
import AdversarialEvaluation from './pages/AdversarialEvaluation'
import InferableBlurs from './pages/InferableBlurs'
import AdversarialResults from './pages/AdversarialResults'
import TransformEvaluation from './pages/TransformEvaluation'
import FinalResults from './pages/FinalResults'
import Presentation from './pages/Presentation'

export default function App() {
  return (
    <Routes>
      {/* Redirect root and legacy routes */}
      <Route path="/" element={<Navigate to="/dataset/full" replace />} />
      <Route path="/analytics" element={<Navigate to="/results/analytics" replace />} />
      <Route path="/analytics/*" element={<Navigate to="/results/analytics" replace />} />

      {/* Presentation — standalone full-screen, no TabLayout */}
      <Route path="/presentation" element={<Presentation />} />

      {/* All tabbed routes share the TabLayout shell */}
      <Route element={<TabLayout />}>
        {/* ── Dataset ── */}
        <Route path="/dataset/full" element={<DatasetBrowser />} />
        <Route path="/dataset/sample-120" element={<AdversarialSampleBrowser manifestFile="adversarial_120.json" title="120 Sample" />} />
        <Route path="/dataset/adversarial-subset" element={<AdversarialSampleBrowser manifestFile="adversarial_experiments.json" title="Adversarial Subset (45)" />} />
        <Route path="/dataset/inferable-blurs" element={<InferableBlurs />} />
        <Route path="/dataset" element={<Navigate to="/dataset/full" replace />} />

        {/* ── Evaluation ── */}
        <Route path="/evaluation/full" element={<JudgeReview manifestFile="manifest_full.json" title="Full Evaluation" />} />
        <Route path="/evaluation/sample" element={<JudgeReview manifestFile="manifest_sample.json" title="Sample Evaluation" />} />
        <Route path="/evaluation/transform-mqm" element={<TransformEvaluation />} />
        <Route path="/evaluation/adversarial" element={<AdversarialEvaluation />} />
        <Route path="/evaluation" element={<Navigate to="/evaluation/full" replace />} />

        {/* ── Results ── */}
        <Route path="/results/overview" element={<FinalResults />} />
        <Route path="/results/adversarial" element={<AdversarialResults />} />
        <Route path="/results/analytics" element={<Analytics manifestFile="manifest_sample.json" title="Analytics" />} />
        <Route path="/results" element={<Navigate to="/results/overview" replace />} />
      </Route>
    </Routes>
  )
}
