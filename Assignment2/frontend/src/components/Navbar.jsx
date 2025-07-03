import { AppBar, Toolbar, Typography, Button } from "@mui/material";
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <AppBar position="fixed">
      <Toolbar>
        <Typography variant="h6" sx={{ flexGrow: 1 }}>
          CS4250 Assignment 2
        </Typography>
        <Button color="inherit" component={Link} to="/">Home</Button>
        <Button color="inherit" component={Link} to="/boolean">Boolean Search</Button>
        <Button color="inherit" component={Link} to="/bm25">BM25 Search</Button>
        <Button color="inherit" component={Link} to="/top-pagerank">PageRank Top 100</Button>
        <Button color="inherit" component={Link} to="/combined-rank">Combined Rank Search</Button>
      </Toolbar>
    </AppBar>
  );
}