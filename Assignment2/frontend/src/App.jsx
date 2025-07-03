import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import BooleanSearch from "./pages/BooleanSearch";
import BM25Search from "./pages/BM25Search";
import CombinedRank from "./pages/CombinedRank";
import PageRankTop100 from "./pages/PageRankTop100";
import Navbar from "./components/Navbar";

const App = () => {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/boolean" element={<BooleanSearch />} />
        <Route path="/bm25" element={<BM25Search />} />
        <Route path="/combined-rank" element={<CombinedRank />} />
        <Route path="/top-pagerank" element={<PageRankTop100 />} />
      </Routes>
    </Router>
  );
};

export default App;