import { useState } from "react";
import { TextField, Button, Typography, Box, Link } from "@mui/material";
import axios from "axios";

export default function CombinedRankSearch() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000/api";
    const res = await axios.post(`${API_URL}/combined-rank`, { query });
    setResults(res.data);
  };

  return (
    <Box sx={{ mt: 8, p: 2 }}>
      <Typography variant="h4">Combined BM25 × PageRank Search</Typography>
      <TextField
        label="Enter Query"
        fullWidth
        variant="filled"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <Button variant="contained" sx={{ mt: 2 }} onClick={handleSearch}>Search</Button>

      <Typography variant="h6" sx={{ mt: 4 }}>Top Results:</Typography>
      <Typography variant="body1" sx={{ mb: 2 }}>
        {results.length === 0 ? "No results found." : `${results.length} results found.`}
      </Typography>

      {results.map((result, i) => (
        <Box key={i} sx={{ mb: 1 }}>
          <Typography variant="body1">
            <strong>Document {i + 1}:</strong> {result.doc_id} – Score: {result.score.toFixed(6)}<br />
            <Link href={result.url} target="_blank" rel="noopener noreferrer">
              {result.url}
            </Link>
          </Typography>
        </Box>
      ))}
    </Box>
  );
}
