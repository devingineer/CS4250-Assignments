import { useState } from "react";
import { TextField, Button, Typography, Box } from "@mui/material";
import axios from "axios";

export default function BooleanSearch() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000/api";
    const res = await axios.post(`${API_URL}/boolean`, { query });
    setResults(res.data);
  };

  return (
    <Box sx={{ mt: 8, p: 2 }}>
      <Typography variant="h4">Boolean Retrieval Search</Typography>
      <TextField
        label="Enter Query"
        fullWidth
        variant="filled"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <Button variant="contained" sx={{ mt: 2 }} onClick={handleSearch}>Search</Button>
      
      <Typography variant="h6" sx={{ mt: 4 }}>Results:</Typography>
      <Typography variant="body1" sx={{ mb: 2 }}>
        {results.length === 0 ? "No results found." : `${results.length} results found.`}
      </Typography>

      <Typography variant="body1" sx={{ mb: 2 }}>
        {results.length > 0 && results.map((doc, i) => (
          <div key={i}>
            <strong>Document {i + 1}:</strong> {doc}
          </div>
        ))}
      </Typography>
    </Box>
  );
}
