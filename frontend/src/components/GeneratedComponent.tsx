import FileDownloadIcon from "@mui/icons-material/FileDownload";
import RestartAltIcon from "@mui/icons-material/RestartAlt";
import SettingsIcon from "@mui/icons-material/Settings";
import {
  Box,
  Button,
  FormControlLabel,
  IconButton,
  Switch,
  TextField,
  Typography,
} from "@mui/material";
import React from "react";

const ScreenshotToCodeComponent: React.FC = () => {
  return (
    <Box
      sx={{
        maxWidth: "400px",
        margin: "auto",
        padding: "16px",
        borderRadius: "8px",
        boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
        backgroundColor: "#fff",
      }}
    >
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "24px",
        }}
      >
        <Typography variant="h6" component="h1">
          Screenshot to Code
        </Typography>
        <IconButton aria-label="settings">
          <SettingsIcon />
        </IconButton>
      </Box>

      <Box
        sx={{
          marginBottom: "16px",
        }}
      >
        <Typography
          variant="subtitle1"
          component="div"
          sx={{
            marginBottom: "8px",
          }}
        >
          Generating:
        </Typography>
        <TextField
          fullWidth
          select
          SelectProps={{
            native: true,
          }}
          variant="outlined"
          value="React + MUI"
        >
          <option>React + MUI</option>
        </TextField>
      </Box>

      <TextField
        fullWidth
        multiline
        rows={3}
        placeholder="Tell the AI what to change..."
        variant="outlined"
        sx={{
          marginBottom: "24px",
        }}
      />

      <FormControlLabel
        control={<Switch defaultChecked />}
        label="Include screenshot of current version?"
        sx={{
          display: "block",
          marginBottom: "24px",
        }}
      />

      <Button
        variant="contained"
        fullWidth
        sx={{
          marginBottom: "16px",
          backgroundColor: "#000",
          "&:hover": {
            backgroundColor: "#333",
          },
        }}
      >
        Update
      </Button>

      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
        }}
      >
        <IconButton aria-label="download">
          <FileDownloadIcon />
        </IconButton>
        <IconButton aria-label="reset">
          <RestartAltIcon />
        </IconButton>
      </Box>
    </Box>
  );
};

export default ScreenshotToCodeComponent;
