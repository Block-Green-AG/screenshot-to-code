import { Box, Typography } from "@mui/material";

const Loading = () => {
  return (
    <Box sx={{ maxWidth: "300px", margin: "auto", textAlign: "center" }}>
      <Typography variant="h1">Generating code....</Typography>
    </Box>
  );
};

export default Loading;
