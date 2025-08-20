import React, { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Box,
  Card,
  CardContent,
  Alert,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions
} from '@mui/material';
import { Refresh as RefreshIcon, Visibility as VisibilityIcon } from '@mui/icons-material';
import axios from 'axios';
import TraceabilityView from './TraceabilityView';

const IdentityGenerator = () => {
  const [formData, setFormData] = useState({
    sex: 'Female',
    location: 'USA',
    age: '25',
    occupation: 'Engineer',
    race: 'Asian',
    religion: 'None',
    birth_year: '1998',
    birth_country: '',
    citizenship_country: '',
    diaspora_generation: ''
  });

  const [identities, setIdentities] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [traceabilityModal, setTraceabilityModal] = useState({
    open: false,
    requestId: null
  });

  // Function to parse names from AI text response
  const parseNamesFromText = (text) => {
    const names = [];
    
    // Look for numbered lists with names
    const numberedPattern = /(\d+\.\s*)([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)/g;
    let match;
    
    while ((match = numberedPattern.exec(text)) !== null) {
      const fullName = match[2].trim();
      const nameParts = fullName.split(/\s+/);
      
      if (nameParts.length >= 2) {
        names.push({
          first_name: nameParts[0],
          middle_name: nameParts.length > 2 ? nameParts.slice(1, -1).join(' ') : "",
          last_name: nameParts[nameParts.length - 1],
          cultural_context: {
            culture: "Mixed",
            region: formData.location || "Unknown",
            language: "English"
          },
          validation_status: "generated",
          validation_notes: ["AI-generated name"],
          full_name: fullName
        });
      }
    }
    
    // If no numbered names found, look for names in quotes or parentheses
    if (names.length === 0) {
      const quotePattern = /["']([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)["']/g;
      while ((match = quotePattern.exec(text)) !== null) {
        const fullName = match[1].trim();
        const nameParts = fullName.split(/\s+/);
        
        if (nameParts.length >= 2) {
          names.push({
            first_name: nameParts[0],
            middle_name: nameParts.length > 2 ? nameParts.slice(1, -1).join(' ') : "",
            last_name: nameParts[nameParts.length - 1],
            cultural_context: {
              culture: "Mixed",
              region: formData.location || "Unknown",
              language: "English"
            },
            validation_status: "generated",
            validation_notes: ["AI-generated name"],
            full_name: fullName
          });
        }
      }
    }
    
    return names;
  };

  const handleInputChange = (field) => (event) => {
    setFormData({
      ...formData,
      [field]: event.target.value
    });
  };

  const generateIdentity = async () => {
    setLoading(true);
    setError('');
    
    try {
      // Format the request according to the API structure
      const apiRequest = {
        category: "person",
        parameters: {
          sex: formData.sex,
          location: formData.location,
          age: parseInt(formData.age) || 25,
          occupation: formData.occupation,
          race: formData.race,
          religion: formData.religion,
          birth_year: parseInt(formData.birth_year) || 1990,
          birth_country: formData.birth_country,
          citizenship_country: formData.citizenship_country,
          diaspora_generation: formData.diaspora_generation ? parseInt(formData.diaspora_generation) : null,
          fast_mode: true  // Enable fast mode for better performance
        }
      };
      
      const response = await axios.post('/api/names/generate', apiRequest);
      console.log('API Response:', response.data); // Debug log
      
      // Handle the response structure from our API
      if (response.data.success && response.data.result) {
        // Parse the text response from AI agents
        const resultText = response.data.result;
        console.log('Raw API Response:', resultText);
        
        // Extract names from the text response
        const extractedNames = parseNamesFromText(resultText);
        
        if (extractedNames.length > 0) {
          setIdentities(extractedNames);
        } else {
          // Fallback: create a structured response from the text
          const fallbackIdentity = {
            first_name: "AI",
            middle_name: "",
            last_name: "Generated",
            cultural_context: {
              culture: "Mixed",
              region: formData.location || "Unknown",
              language: "English"
            },
            validation_status: "generated",
            validation_notes: ["AI-generated response"],
            full_response: resultText,
            full_name: "AI Generated Names"
          };
          setIdentities([fallbackIdentity]);
        }
      } else {
        // Create a mock identity for testing if API doesn't return expected format
        const mockIdentity = {
          first_name: "Test",
          middle_name: "User",
          last_name: "Generated",
          cultural_context: {
            culture: "Test Culture",
            region: formData.location,
            language: "English"
          },
          validation_status: "validated",
          validation_notes: ["Mock data for testing"]
        };
        setIdentities([mockIdentity]);
      }
    } catch (err) {
      console.error('API Error:', err);
      setError(err.response?.data?.detail || 'Failed to generate identity');
    } finally {
      setLoading(false);
    }
  };

  const regenerateIdentity = async () => {
    setLoading(true);
    setError('');
    
    try {
      // Format the request according to the API structure
      const apiRequest = {
        category: "person",
        parameters: {
          sex: formData.sex,
          location: formData.location,
          age: parseInt(formData.age) || 25,
          occupation: formData.occupation,
          race: formData.race,
          religion: formData.religion,
          birth_year: parseInt(formData.birth_year) || 1990,
          birth_country: formData.birth_country,
          citizenship_country: formData.citizenship_country,
          diaspora_generation: formData.diaspora_generation ? parseInt(formData.diaspora_generation) : null,
          fast_mode: true  // Enable fast mode for better performance
        }
      };
      
      const response = await axios.post('/api/names/generate', apiRequest);
      console.log('Regenerate API Response:', response.data); // Debug log
      
      // Handle the response structure from our API
      if (response.data.success && response.data.result) {
        // Parse the text response from AI agents
        const resultText = response.data.result;
        console.log('Regenerate Raw API Response:', resultText);
        
        // Extract names from the text response
        const extractedNames = parseNamesFromText(resultText);
        
        if (extractedNames.length > 0) {
          setIdentities(extractedNames);
        } else {
          // Fallback: create a structured response from the text
          const fallbackIdentity = {
            first_name: "AI",
            middle_name: "",
            last_name: "Regenerated",
            cultural_context: {
              culture: "Mixed",
              region: formData.location || "Unknown",
              language: "English"
            },
            validation_status: "generated",
            validation_notes: ["AI-generated response"],
            full_response: resultText,
            full_name: "AI Regenerated Names"
          };
          setIdentities([fallbackIdentity]);
        }
      } else {
        // Create a mock identity for testing if API doesn't return expected format
        const mockIdentity = {
          first_name: "Regenerated",
          middle_name: "User",
          last_name: "Identity",
          cultural_context: {
            culture: "Test Culture",
            region: formData.location,
            language: "English"
          },
          validation_status: "validated",
          validation_notes: ["Mock data for testing"]
        };
        setIdentities([mockIdentity]);
      }
    } catch (err) {
      console.error('Regenerate API Error:', err);
      setError(err.response?.data?.detail || 'Failed to regenerate identity');
    } finally {
      setLoading(false);
    }
  };

  const viewTraceability = (requestId, identity) => {
    setTraceabilityModal({
      open: true,
      requestId,
      identityData: identity
    });
  };

  const isFormValid = () => {
    // Required fields: sex, location, age, occupation, race
    // Made religion and birth_year optional for easier testing
    const requiredFields = ['sex', 'location', 'age', 'occupation', 'race'];
    return requiredFields.every(field => formData[field] !== '');
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" gutterBottom>
          Generate New Identity
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
          Enter your information to generate culturally appropriate identities
        </Typography>

        <Grid container spacing={3}>
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth>
              <InputLabel>Sex</InputLabel>
              <Select
                value={formData.sex}
                label="Sex"
                onChange={handleInputChange('sex')}
              >
                <MenuItem value="Male">Male</MenuItem>
                <MenuItem value="Female">Female</MenuItem>
                <MenuItem value="Non-binary">Non-binary</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Location (Country, City)"
              value={formData.location}
              onChange={handleInputChange('location')}
              placeholder="e.g., Spain, Madrid"
            />
          </Grid>
          
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Age"
              type="number"
              value={formData.age}
              onChange={handleInputChange('age')}
            />
          </Grid>
          
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Occupation"
              value={formData.occupation}
              onChange={handleInputChange('occupation')}
            />
          </Grid>
          
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Race/Ethnicity"
              value={formData.race}
              onChange={handleInputChange('race')}
            />
          </Grid>
          
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Religion"
              value={formData.religion}
              onChange={handleInputChange('religion')}
            />
          </Grid>
          
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Birth Year"
              type="number"
              value={formData.birth_year}
              onChange={handleInputChange('birth_year')}
            />
          </Grid>
          
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Birth Country"
              value={formData.birth_country}
              onChange={handleInputChange('birth_country')}
              placeholder="e.g., Cambodia, China, India"
              helperText="Country of birth/origin (optional - will be auto-detected from ethnicity)"
            />
          </Grid>
          
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Citizenship Country"
              value={formData.citizenship_country}
              onChange={handleInputChange('citizenship_country')}
              placeholder="e.g., United States, Canada"
              helperText="Current citizenship (optional)"
            />
          </Grid>
          
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="Diaspora Generation"
              type="number"
              value={formData.diaspora_generation}
              onChange={handleInputChange('diaspora_generation')}
              placeholder="1, 2, 3"
              helperText="Immigrant generation (1st, 2nd, 3rd gen) - optional"
            />
          </Grid>
        </Grid>

        <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
          <Button
            variant="contained"
            onClick={generateIdentity}
            disabled={!isFormValid() || loading}
            startIcon={loading ? <CircularProgress size={20} /> : null}
          >
            Generate Identity
          </Button>
          
          {identities.length > 0 && (
            <Button
              variant="outlined"
              onClick={regenerateIdentity}
              disabled={loading}
              startIcon={<RefreshIcon />}
            >
              Regenerate
            </Button>
          )}
        </Box>

        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}

        {identities.length > 0 && (
          <Box sx={{ mt: 4 }}>
            <Typography variant="h5" gutterBottom>
              Generated Identities
            </Typography>
            <Grid container spacing={2}>
              {identities.map((identity, index) => (
                <Grid item xs={12} key={index}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6">
                        {identity.full_name || `${identity.first_name} ${identity.middle_name} ${identity.last_name}`.trim()}
                      </Typography>
                      <Typography color="text.secondary" sx={{ mt: 1 }}>
                        Culture: {identity.cultural_context?.culture || 'Mixed'}
                      </Typography>
                      <Typography color="text.secondary">
                        Status: {identity.validation_status || 'Generated'}
                      </Typography>
                      {identity.full_response && (
                        <Typography color="text.secondary" sx={{ mt: 1, fontSize: '0.875rem' }}>
                          <strong>AI Response:</strong> {identity.full_response.substring(0, 200)}...
                        </Typography>
                      )}
                      <Box sx={{ mt: 2 }}>
                        <Button
                          size="small"
                          startIcon={<VisibilityIcon />}
                          onClick={() => viewTraceability(`request-${index}`, identity)}
                        >
                          View Traceability
                        </Button>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Box>
        )}
      </Paper>

      {/* Traceability Modal */}
      <Dialog
        open={traceabilityModal.open}
        onClose={() => setTraceabilityModal({ open: false, requestId: null, identityData: null })}
        maxWidth="lg"
        fullWidth
      >
        <DialogTitle>Traceability Report</DialogTitle>
        <DialogContent>
          <TraceabilityView 
            requestId={traceabilityModal.requestId} 
            identityData={traceabilityModal.identityData}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setTraceabilityModal({ open: false, requestId: null, identityData: null })}>
            Close
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default IdentityGenerator;
