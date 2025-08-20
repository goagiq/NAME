import React, { useState, useEffect, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Box,
  List,
  ListItem,
  ListItemText,
  Divider,
  Alert,
  CircularProgress
} from '@mui/material';
import axios from 'axios';

const TraceabilityView = ({ requestId, identityData }) => {
  const [traceabilityData, setTraceabilityData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const params = useParams();

  // Use requestId prop if provided, otherwise use URL params
  const actualRequestId = requestId || params.requestId;

  const fetchTraceabilityData = useCallback(async () => {
    setLoading(true);
    setError('');
    
    try {
      // If we have identityData directly, use it
      if (identityData && identityData.traceability) {
        setTraceabilityData(identityData.traceability);
      } else {
        // Fallback to API call if needed
        const response = await axios.get(`/api/traceability/${actualRequestId}`);
        setTraceabilityData(response.data);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch traceability data');
    } finally {
      setLoading(false);
    }
  }, [actualRequestId, identityData]);

  useEffect(() => {
    if (actualRequestId || identityData) {
      fetchTraceabilityData();
    }
  }, [actualRequestId, identityData, fetchTraceabilityData]);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" p={3}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ m: 2 }}>
        {error}
      </Alert>
    );
  }

  if (!traceabilityData) {
    return (
      <Alert severity="info" sx={{ m: 2 }}>
        No traceability data available
      </Alert>
    );
  }

  // Helper function to safely render values
  const safeRender = (value) => {
    if (value === null || value === undefined) {
      return 'Not specified';
    }
    if (typeof value === 'object') {
      return JSON.stringify(value);
    }
    return String(value);
  };

  const steps = [
    {
      label: 'Request Parameters',
      content: (
        <Box>
          <Typography variant="h6" gutterBottom>
            User Input Parameters
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            This step captures all the user-provided information that will be used to generate culturally appropriate names.
          </Typography>
          <List dense>
            {Object.entries(traceabilityData.request_parameters || {}).map(([key, value]) => (
              <ListItem key={key}>
                <ListItemText
                  primary={key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                  secondary={safeRender(value)}
                />
              </ListItem>
            ))}
          </List>
        </Box>
      )
    },
    {
      label: 'Cultural Analysis',
      content: (
        <Box>
          <Typography variant="h6" gutterBottom>
            Cultural Context Analysis
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            This step analyzes the user's ethnicity and location to determine the appropriate cultural context, 
            including ethnicity mapping, diaspora detection, and naming conventions.
          </Typography>
          <List dense>
            {/* Basic cultural info */}
            <ListItem>
              <ListItemText
                primary="Primary Culture"
                secondary={safeRender(traceabilityData.cultural_analysis?.culture) || 'Unknown'}
              />
            </ListItem>
            <ListItem>
              <ListItemText
                primary="Region"
                secondary={safeRender(traceabilityData.cultural_analysis?.region) || 'Unknown'}
              />
            </ListItem>
            <ListItem>
              <ListItemText
                primary="Sub-Region"
                secondary={safeRender(traceabilityData.cultural_analysis?.sub_region) || 'None'}
              />
            </ListItem>
            <ListItem>
              <ListItemText
                primary="Country of Origin"
                secondary={safeRender(traceabilityData.cultural_analysis?.country_of_origin) || 'Unknown'}
              />
            </ListItem>
            <ListItem>
              <ListItemText
                primary="Language"
                secondary={safeRender(traceabilityData.cultural_analysis?.language) || 'Unknown'}
              />
            </ListItem>
            
            {/* Ethnicity mapping details */}
            {traceabilityData.cultural_analysis?.ethnicity_mapping && (
              <>
                <Divider sx={{ my: 1 }} />
                <Typography variant="subtitle2" color="primary" sx={{ mt: 2, mb: 1 }}>
                  Ethnicity Mapping
                </Typography>
                <ListItem>
                  <ListItemText
                    primary="Input Race/Ethnicity"
                    secondary={safeRender(traceabilityData.cultural_analysis.ethnicity_mapping.input_race)}
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="Mapped Culture"
                    secondary={safeRender(traceabilityData.cultural_analysis.ethnicity_mapping.mapped_culture)}
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="Regional Modifier"
                    secondary={safeRender(traceabilityData.cultural_analysis.ethnicity_mapping.regional_modifier) || 'None'}
                  />
                </ListItem>
              </>
            )}
            
            {/* Diaspora context */}
            {traceabilityData.cultural_analysis?.diaspora_context && (
              <>
                <Divider sx={{ my: 1 }} />
                <Typography variant="subtitle2" color="primary" sx={{ mt: 2, mb: 1 }}>
                  Diaspora Context
                </Typography>
                <ListItem>
                  <ListItemText
                    primary="Birth Country"
                    secondary={safeRender(traceabilityData.cultural_analysis.diaspora_context.birth_country) || 'Not specified'}
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="Citizenship Country"
                    secondary={safeRender(traceabilityData.cultural_analysis.diaspora_context.citizenship_country) || 'Not specified'}
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="Diaspora Generation"
                    secondary={safeRender(traceabilityData.cultural_analysis.diaspora_context.diaspora_generation) || 'Not specified'}
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="Is Diaspora"
                    secondary={safeRender(traceabilityData.cultural_analysis.diaspora_context.is_diaspora) ? 'Yes' : 'No'}
                  />
                </ListItem>
              </>
            )}
            
            {/* Naming conventions */}
            {traceabilityData.cultural_analysis?.naming_conventions && (
              <>
                <Divider sx={{ my: 1 }} />
                <Typography variant="subtitle2" color="primary" sx={{ mt: 2, mb: 1 }}>
                  Naming Conventions
                </Typography>
                {Object.entries(traceabilityData.cultural_analysis.naming_conventions).map(([key, value]) => (
                  <ListItem key={key}>
                    <ListItemText
                      primary={key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                      secondary={
                        typeof value === 'boolean' 
                          ? (value ? 'Yes' : 'No') 
                          : Array.isArray(value) 
                            ? `${value.length} items`
                            : safeRender(value)
                      }
                    />
                  </ListItem>
                ))}
              </>
            )}
          </List>
        </Box>
      )
    },
    {
      label: 'Name Generation Steps',
      content: (
        <Box>
          <Typography variant="h6" gutterBottom>
            Name Generation Process
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            This step details how names are generated using the cultural context, including name pool selection, 
            generation methodology, and uniqueness constraints.
          </Typography>
          <List dense>
                         {(traceabilityData.name_generation_steps || []).map((step, index) => (
               <ListItem key={index} sx={{ flexDirection: 'column', alignItems: 'flex-start' }}>
                 <ListItemText
                   primary={`Step ${step.step}: ${safeRender(step.description)}`}
                   secondary={safeRender(step.result)}
                   sx={{ width: '100%' }}
                 />
                 {step.details && (
                   <Box sx={{ mt: 1, width: '100%' }}>
                     <Typography variant="subtitle2" color="primary" gutterBottom>
                       Detailed Analysis:
                     </Typography>
                     {step.details.culture && (
                       <Typography variant="body2" color="text.secondary">
                         <strong>Culture:</strong> {safeRender(step.details.culture)}
                       </Typography>
                     )}
                     {step.details.region && (
                       <Typography variant="body2" color="text.secondary">
                         <strong>Region:</strong> {safeRender(step.details.region)}
                       </Typography>
                     )}
                     {step.details.sub_region && (
                       <Typography variant="body2" color="text.secondary">
                         <strong>Sub-Region:</strong> {safeRender(step.details.sub_region)}
                       </Typography>
                     )}
                     {step.details.name_pools_used && (
                       <Typography variant="body2" color="text.secondary">
                         <strong>Name Pools Used:</strong> {safeRender(step.details.name_pools_used.pools_used?.join(', '))}
                       </Typography>
                     )}
                     {step.details.candidates && (
                       <Typography variant="body2" color="text.secondary">
                         <strong>Generated Candidates:</strong> {safeRender(step.details.candidates.length)} unique names
                       </Typography>
                     )}
                     {step.details.generation_method && (
                       <Typography variant="body2" color="text.secondary">
                         <strong>Method:</strong> {safeRender(step.details.generation_method)}
                       </Typography>
                     )}
                   </Box>
                 )}
               </ListItem>
             ))}
          </List>
        </Box>
      )
    },
    {
      label: 'Validation Steps',
      content: (
        <Box>
          <Typography variant="h6" gutterBottom>
            Validation Process
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            This step validates each generated name for cultural appropriateness, uniqueness, and compliance 
            with naming conventions and special requirements.
          </Typography>
          <List dense>
                         {(traceabilityData.validation_steps || []).map((step, index) => (
               <ListItem key={index} sx={{ flexDirection: 'column', alignItems: 'flex-start' }}>
                 <ListItemText
                   primary={`Step ${step.step}: ${safeRender(step.description)}`}
                   secondary={safeRender(step.result)}
                   sx={{ width: '100%' }}
                 />
                 {step.details && (
                   <Box sx={{ mt: 1, width: '100%' }}>
                     <Typography variant="subtitle2" color="primary" gutterBottom>
                       Validation Details:
                     </Typography>
                     {step.details.candidate_name && (
                       <Typography variant="body2" color="text.secondary">
                         <strong>Candidate Name:</strong> {safeRender(step.details.candidate_name)}
                       </Typography>
                     )}
                     {step.details.check_type && (
                       <Typography variant="body2" color="text.secondary">
                         <strong>Check Type:</strong> {safeRender(step.details.check_type)}
                       </Typography>
                     )}
                     {step.details.status && (
                       <Typography variant="body2" color="text.secondary">
                         <strong>Status:</strong> {safeRender(step.details.status)}
                       </Typography>
                     )}
                     {step.details.overall_score && (
                       <Typography variant="body2" color="text.secondary">
                         <strong>Cultural Appropriateness Score:</strong> {safeRender(step.details.overall_score)}
                       </Typography>
                     )}
                     {step.details.culture && (
                       <Typography variant="body2" color="text.secondary">
                         <strong>Culture Validated:</strong> {safeRender(step.details.culture)}
                       </Typography>
                     )}
                     {step.details.naming_conventions && (
                       <Typography variant="body2" color="text.secondary">
                         <strong>Naming Conventions:</strong> {safeRender(step.details.naming_conventions)}
                       </Typography>
                     )}
                   </Box>
                 )}
               </ListItem>
             ))}
          </List>
        </Box>
      )
    },
    {
      label: 'Final Result',
      content: (
        <Box>
          <Typography variant="h6" gutterBottom>
            Final Generated Identities
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            This step shows the final generated identities with their validation status, cultural context, 
            and summary of the generation process.
          </Typography>
          <List dense>
            {traceabilityData.final_result?.generated_names ? (
              traceabilityData.final_result.generated_names.map((name, index) => (
                <ListItem key={index} sx={{ flexDirection: 'column', alignItems: 'flex-start' }}>
                  <ListItemText
                    primary={`Identity ${index + 1}: ${safeRender(name.full_name)}`}
                    secondary={`Status: ${safeRender(name.validation_status)}`}
                    sx={{ width: '100%' }}
                  />
                  <Box sx={{ mt: 1, width: '100%' }}>
                    <Typography variant="body2" color="text.secondary">
                      First Name: {safeRender(name.first_name)}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Middle Name: {safeRender(name.middle_name) || 'None'}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Last Name: {safeRender(name.last_name)}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Cultural Notes: {safeRender(name.cultural_notes)}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Generated: {new Date(name.generated_date).toLocaleString()}
                    </Typography>
                  </Box>
                </ListItem>
              ))
            ) : (
              <ListItem>
                <ListItemText
                  primary="Generated Name"
                  secondary={safeRender(traceabilityData.final_result?.generated_name) || 'Not available'}
                />
              </ListItem>
            )}
            
            {/* Cultural summary */}
            {traceabilityData.final_result?.cultural_summary && (
              <>
                <Divider sx={{ my: 2 }} />
                <Typography variant="subtitle2" color="primary" gutterBottom>
                  Cultural Summary
                </Typography>
                <ListItem>
                  <ListItemText
                    primary="Primary Culture"
                    secondary={safeRender(traceabilityData.final_result.cultural_summary.primary_culture)}
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="Success Rate"
                    secondary={safeRender(traceabilityData.final_result.success_rate)}
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="Total Generated"
                    secondary={safeRender(traceabilityData.final_result.total_generated)}
                  />
                </ListItem>
              </>
            )}
          </List>
        </Box>
      )
    }
  ];

  return (
    <Container maxWidth="lg" sx={{ mt: 2, mb: 2 }}>
      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Traceability Report
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          Request ID: {actualRequestId}
        </Typography>

        <Stepper orientation="vertical">
          {steps.map((step, index) => (
            <Step key={index} active={true}>
              <StepLabel>
                <Typography variant="h6">{step.label}</Typography>
              </StepLabel>
              <StepContent>
                <Box sx={{ mb: 2 }}>
                  {step.content}
                </Box>
                {index < steps.length - 1 && <Divider sx={{ my: 2 }} />}
              </StepContent>
            </Step>
          ))}
        </Stepper>
      </Paper>
    </Container>
  );
};

export default TraceabilityView;
