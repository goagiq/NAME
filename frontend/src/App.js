import React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import CssBaseline from '@mui/material/CssBaseline';
import Header from './components/Header';
import IdentityGenerator from './components/IdentityGenerator';
import TraceabilityView from './components/TraceabilityView';
import SimpleTest from './components/SimpleTest';

// Create a theme instance
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <div className="App">
          <Header />
          <Routes>
            <Route path="/" element={<IdentityGenerator />} />
            <Route path="/test" element={<SimpleTest />} />
            <Route path="/identity" element={<IdentityGenerator />} />
            <Route path="/traceability/:requestId" element={<TraceabilityView />} />
          </Routes>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;
