import { Routes, Route } from 'react-router-dom'
import Landing from './pages/Landing'
import JudgeReview from './pages/JudgeReview'
import DatasetBrowser from './pages/DatasetBrowser'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/dataset" element={<DatasetBrowser />} />
      <Route path="/review/full" element={<JudgeReview manifestFile="manifest_full.json" title="Full Evaluation" />} />
      <Route path="/review/sample" element={<JudgeReview manifestFile="manifest_sample.json" title="Sample Evaluation" />} />
    </Routes>
  )
}
