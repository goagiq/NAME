import React, { useState } from 'react';
import { Container, Paper, Typography, Button, Card, CardContent } from '@mui/material';

const SimpleTest = () => {
  const [testData, setTestData] = useState(null);

  const generateTestData = () => {
    // Simulate the data structure that might be causing issues
    const mockData = {
      first_name: "hsiao-wei",
      middle_name: null,
      last_name: "tsai",
      cultural_context: {
        culture: "Chinese",
        region: "Taiwan",
        naming_conventions: {
          no_middle_names: true,
          surname_first: true
        }
      },
      validation_status: "validated",
      validation_notes: [],
      detailed_traceability: {
        request_parameters: {
          sex: "Female",
          location: "USA",
          race: "Taiwanese"
        },
        cultural_analysis: {
          culture: "Chinese",
          region: "Taiwan",
          naming_conventions: {
            no_middle_names: true,
            surname_first: true
          }
        },
        name_generation_steps: [
          {
            step: 1,
            description: "Generate name",
            result: "Generated hsiao-wei tsai",
            details: {
              culture: "Chinese",
              region: "Taiwan"
            }
          }
        ],
        validation_steps: [
          {
            step: 1,
            description: "Validate name",
            result: "Validated successfully",
            details: {
              candidate_name: "hsiao-wei tsai",
              check_type: "cultural_appropriateness",
              status: "passed"
            }
          }
        ],
        final_result: {
          generated_names: [
            {
              full_name: "hsiao-wei tsai",
              first_name: "hsiao-wei",
              middle_name: null,
              last_name: "tsai",
              validation_status: "validated",
              cultural_notes: "Culturally appropriate Taiwanese name",
              generated_date: "2025-08-20T01:36:55.842131"
            }
          ],
          cultural_summary: {
            primary_culture: "Chinese"
          },
          success_rate: "100%",
          total_generated: 1
        }
      }
    };
    
    setTestData(mockData);
  };

  const safeRender = (value) => {
    if (value === null || value === undefined) {
      return 'Not specified';
    }
    if (typeof value === 'object') {
      return JSON.stringify(value);
    }
    return String(value);
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Simple Test Component
        </Typography>
        
        <Button 
          variant="contained" 
          onClick={generateTestData}
          sx={{ mb: 3 }}
        >
          Generate Test Data
        </Button>

        {testData && (
          <Card>
            <CardContent>
              <Typography variant="h6">
                {safeRender(testData.first_name)} {safeRender(testData.middle_name) || ''} {safeRender(testData.last_name)}
              </Typography>
              <Typography color="text.secondary" sx={{ mt: 1 }}>
                Culture: {safeRender(testData.cultural_context?.culture) || 'Unknown'}
              </Typography>
              <Typography color="text.secondary">
                Status: {safeRender(testData.validation_status)}
              </Typography>
              
              {/* Test detailed traceability */}
              {testData.detailed_traceability && (
                <div style={{ marginTop: '20px' }}>
                  <Typography variant="h6" gutterBottom>
                    Traceability Test
                  </Typography>
                  
                  {/* Request Parameters */}
                  <Typography variant="subtitle1">Request Parameters:</Typography>
                  {Object.entries(testData.detailed_traceability.request_parameters || {}).map(([key, value]) => (
                    <Typography key={key} variant="body2">
                      {key}: {safeRender(value)}
                    </Typography>
                  ))}
                  
                  {/* Cultural Analysis */}
                  <Typography variant="subtitle1" sx={{ mt: 2 }}>Cultural Analysis:</Typography>
                  <Typography variant="body2">
                    Culture: {safeRender(testData.detailed_traceability.cultural_analysis?.culture)}
                  </Typography>
                  <Typography variant="body2">
                    Region: {safeRender(testData.detailed_traceability.cultural_analysis?.region)}
                  </Typography>
                  
                  {/* Name Generation Steps */}
                  <Typography variant="subtitle1" sx={{ mt: 2 }}>Name Generation Steps:</Typography>
                  {(testData.detailed_traceability.name_generation_steps || []).map((step, index) => (
                    <div key={index}>
                      <Typography variant="body2">
                        Step {step.step}: {safeRender(step.description)}
                      </Typography>
                      <Typography variant="body2">
                        Result: {safeRender(step.result)}
                      </Typography>
                    </div>
                  ))}
                  
                  {/* Validation Steps */}
                  <Typography variant="subtitle1" sx={{ mt: 2 }}>Validation Steps:</Typography>
                  {(testData.detailed_traceability.validation_steps || []).map((step, index) => (
                    <div key={index}>
                      <Typography variant="body2">
                        Step {step.step}: {safeRender(step.description)}
                      </Typography>
                      <Typography variant="body2">
                        Result: {safeRender(step.result)}
                      </Typography>
                    </div>
                  ))}
                  
                  {/* Final Results */}
                  <Typography variant="subtitle1" sx={{ mt: 2 }}>Final Results:</Typography>
                  {(testData.detailed_traceability.final_result?.generated_names || []).map((name, index) => (
                    <div key={index}>
                      <Typography variant="body2">
                        Name {index + 1}: {safeRender(name.full_name)}
                      </Typography>
                      <Typography variant="body2">
                        Status: {safeRender(name.validation_status)}
                      </Typography>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        )}
      </Paper>
    </Container>
  );
};

export default SimpleTest;
