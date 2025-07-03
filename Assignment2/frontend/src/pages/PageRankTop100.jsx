import { useEffect, useState } from "react";
import { Box, Typography, Link } from "@mui/material";
import axios from "axios";

export default function PageRankTop100() {
  const [pages, setPages] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000/api";
      const res = await axios.get(`${API_URL}/pagerank-top100`);
      setPages(res.data);
    };

    fetchData();
  }, []);

  return (
    <Box sx={{ mt: 8, p: 2 }}>
      <Typography variant="h4">Top 100 PageRank Results</Typography>
      {pages.length === 0 ? (
        <Typography variant="body1">Loading...</Typography>
      ) : (
        <Box sx={{ mt: 3 }}>
          {pages.map((page, i) => (
            <Typography key={i} variant="body1" sx={{ mb: 1 }}>
              <Typography component="span" fontWeight="bold">Doc #{i + 1}: </Typography>
              <Link href={page.url} target="_blank" rel="noopener">
                {page.url}
              </Link>{" "}
              — Score: {page.score.toFixed(10)}
            </Typography>
          ))}
        </Box>
      )}
    </Box>
  );
}
