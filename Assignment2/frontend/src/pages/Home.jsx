import { Box, Typography, List, ListItem } from "@mui/material";

export default function Home() {
  return (
    <Box sx={{ mt: 8, p: 2 }}>
      <Typography variant="h3">CS4250 Assignment 2: Retrieval Models & PageRank</Typography>
      <Typography variant="body1" sx={{ mt: 2 }}>
        This is a simple Retrieval Models and PageRank Project for CS 4250 Web Search and Recommender Systems.
      </Typography>

      <Typography variant="h5" sx={{ mt: 3 }}>Group Members</Typography>
      <List>
        <ListItem>Devin Khun</ListItem>
        <ListItem>Daniel Ho</ListItem>
        <ListItem>Caden Minniefield</ListItem>
        <ListItem>Tony Swank</ListItem>
        <ListItem>Thet Wai</ListItem>
      </List>
      
      <Typography variant="h5" sx={{ mt: 3 }}>Project Description</Typography>
      <Typography variant="body1" sx={{ mt: 2 }}>
        We implemented Boolean retrieval and BM25 ranking using an inverted index over a collection of crawled HTML documents. This interface allows users to test both retrieval methods.
      </Typography>

      <Typography variant="h5" sx={{ mt: 3 }}>How to Use</Typography>
      <Typography variant="body1" sx={{ mt: 2 }}>
        To use the retrieval models, select one of the options from the navigation bar above. You can enter your search query and see the results for both Boolean and BM25 retrieval methods.
      </Typography>
    </Box>
  );
}
