import React from 'react';
import { Box, Typography, Button, Chip, Avatar, Stack } from '@mui/material';
import ArrowDropUpIcon from '@mui/icons-material/ArrowDropUp';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import ShareIcon from '@mui/icons-material/Share';
import EditIcon from '@mui/icons-material/Edit';
import FollowTheSignsIcon from '@mui/icons-material/FollowTheSigns';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';

const QuestionPage = () => {
  return (
    <Box sx={{ maxWidth: '800px', margin: 'auto' }}>
      <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold', mt: 4, mb: 2 }}>
        How to copy files
      </Typography>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="body2" color="text.secondary">
          Asked 15 years, 2 months ago
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Modified 4 months ago
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Viewed 3.6m times
        </Typography>
      </Box>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <Button sx={{ minWidth: 'auto', p: 1, mr: 1 }}>
          <ArrowDropUpIcon fontSize="large" />
        </Button>
        <Typography variant="h5" component="span" sx={{ fontWeight: 'bold', mr: 1 }}>
          3749
        </Typography>
        <Button sx={{ minWidth: 'auto', p: 1 }}>
          <ArrowDropDownIcon fontSize="large" />
        </Button>
      </Box>
      <Typography variant="h6" component="h2" sx={{ mb: 1 }}>
        How do I copy a file in Python?
      </Typography>
      <Stack direction="row" spacing={1} sx={{ mb: 2 }}>
        <Chip label="python" variant="outlined" />
        <Chip label="file" variant="outlined" />
        <Chip label="copy" variant="outlined" />
        <Chip label="filesystems" variant="outlined" />
        <Chip label="file-copying" variant="outlined" />
      </Stack>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <Button startIcon={<ShareIcon />} sx={{ textTransform: 'none', mr: 1 }}>
          Share
        </Button>
        <Button startIcon={<EditIcon />} sx={{ textTransform: 'none', mr: 1 }}>
          Edit
        </Button>
        <Button startIcon={<FollowTheSignsIcon />} sx={{ textTransform: 'none' }}>
          Follow
        </Button>
      </Box>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 4 }}>
        <Button sx={{ minWidth: 'auto', p: 1, mr: 1 }}>
          <ContentCopyIcon />
        </Button>
        <Typography variant="body2" color="text.secondary" sx={{ flexGrow: 1 }}>
          edited Dec 7, 2022 at 3:37
        </Typography>
        <Avatar src="https://placehold.co/40x40" alt="Profile image of Peter Mortensen" sx={{ width: 40, height: 40, mr: 1 }} />
        <Box>
          <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
            Peter Mortensen
          </Typography>
          <Typography variant="body2" color="text.secondary">
            30.8k
          </Typography>
        </Box>
      </Box>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <Avatar src="https://placehold.co/40x40" alt="Profile image of Matt" sx={{ width: 40, height: 40, mr: 1 }} />
        <Box>
          <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
            Matt
          </Typography>
          <Typography variant="body2" color="text.secondary">
            85.2k
          </Typography>
        </Box>
      </Box>
    </Box>
  );
};

export default QuestionPage;