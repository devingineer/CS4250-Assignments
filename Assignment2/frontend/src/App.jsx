import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import BooleanSearch from "./pages/BooleanSearch";
import BM25Search from "./pages/BM25Search";
import Navbar from "./components/Navbar";

const App = () => {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/boolean" element={<BooleanSearch />} />
        <Route path="/bm25" element={<BM25Search />} />
      </Routes>
    </Router>
  );
};

export default App;