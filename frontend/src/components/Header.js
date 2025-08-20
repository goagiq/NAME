import React from 'react';
import { AppBar, Toolbar, Typography, Box, Button } from '@mui/material';
import { PersonAdd as PersonAddIcon, BugReport as BugReportIcon } from '@mui/icons-material';
import { Link as RouterLink } from 'react-router-dom';

const Header = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <PersonAddIcon sx={{ mr: 2 }} />
        <Box sx={{ flexGrow: 1 }}>
          <Typography variant="h6" component="div">
            Name Generation System
          </Typography>
          <Typography variant="caption" component="div">
            Phase 2 - Web Interface
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button 
            color="inherit" 
            component={RouterLink} 
            to="/"
            startIcon={<PersonAddIcon />}
          >
            Generate Names
          </Button>
          <Button 
            color="inherit" 
            component={RouterLink} 
            to="/test"
            startIcon={<BugReportIcon />}
          >
            Test Component
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
