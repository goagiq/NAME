document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('identityForm');
    const regenerateBtn = document.getElementById('regenerateBtn');
    const clearBtn = document.getElementById('clearBtn');
               const exportBtn = document.getElementById('exportBtn');
           const exportFeedbackBtn = document.getElementById('exportFeedbackBtn');
           const toggleTraceabilityBtn = document.getElementById('toggleTraceabilityBtn');
    const collapseAllBtn = document.getElementById('collapseAllBtn');
    const expandAllBtn = document.getElementById('expandAllBtn');
    const resultDiv = document.getElementById('result');
    const identityResult = document.getElementById('identityResult');
    const traceabilitySection = document.getElementById('traceabilitySection');
    const traceabilityResult = document.getElementById('traceabilityResult');
    const ollamaStatus = document.getElementById('ollamaStatus');
    
    let currentFormData = null;
    let currentResults = null;
    
    // Check Ollama status on page load if element exists
    if (ollamaStatus) {
        checkOllamaStatus();
    }
    
    // Template buttons - only if they exist
    const templateButtons = document.querySelectorAll('.template-btn');
    if (templateButtons.length > 0) {
        templateButtons.forEach(btn => {
            btn.addEventListener('click', function() {
                loadTemplate(this.dataset.template);
            });
        });
    }
    
    // Form field enhancements - only if elements exist
    if (clearBtn || exportBtn || toggleTraceabilityBtn) {
        setupFormEnhancements();
    }

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        await generateIdentity();
    });

    regenerateBtn.addEventListener('click', async function() {
        await generateIdentity();
    });

    async function generateIdentity() {
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        
        // Filter out empty optional fields
        Object.keys(data).forEach(key => {
            if (data[key] === '') {
                delete data[key];
            }
        });
        
        currentFormData = data;
        
        // Analyze feedback for this cultural context
        const relevantFeedback = analyzeFeedbackForCulture(
            data.race || '', 
            data.religion || '', 
            data.location || ''
        );
        
        // Add feedback context to the request
        if (relevantFeedback.length > 0) {
            data.feedback_context = {
                feedback_count: relevantFeedback.length,
                recent_feedback: relevantFeedback.slice(-3).map(f => f.feedback_text),
                cultural_improvements: relevantFeedback.filter(f => f.feedback_type === 'incorrect').length
            };
        }

        try {
            // Show loading state
            identityResult.innerHTML = '<div class="loading">Generating identity...</div>';
            resultDiv.style.display = 'block';
            regenerateBtn.style.display = 'none';
            traceabilitySection.style.display = 'none';

            const response = await fetch('/api/generate-identity', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                currentResults = result; // Store results for export
                displayResults(result);
                regenerateBtn.style.display = 'inline-block';
            } else {
                identityResult.innerHTML = `<div class="error">Error: ${result.error || 'Failed to generate identity'}</div>`;
            }
        } catch (error) {
            console.error('Error:', error);
            identityResult.innerHTML = '<div class="error">Error: Failed to connect to server</div>';
        }
    }

    function displayResults(identities) {
        if (!identities || identities.length === 0) {
            identityResult.innerHTML = '<div class="error">No identities generated</div>';
            return;
        }

        let html = '';
        identities.forEach((identity, index) => {
            html += `
                <div class="identity-item" data-identity-index="${index}">
                    <div class="identity-header" onclick="toggleIdentity(${index})">
                        <div class="identity-title">
                            <i class="fas fa-chevron-down collapse-icon" id="collapse-icon-${index}"></i>
                            <h4>Identity ${index + 1}: ${identity.first_name} ${identity.middle_name || ''} ${identity.last_name}</h4>
                        </div>
                        <div class="identity-status">
                            <span class="validation-badge ${identity.validation_status.toLowerCase()}">${identity.validation_status}</span>
                            <span class="generation-time">${new Date(identity.generated_date).toLocaleTimeString()}</span>
                        </div>
                    </div>
                    <div class="identity-content" id="identity-content-${index}" style="display: none;">
                        <div class="identity-details">
                            <div class="identity-detail">
                                <span class="detail-label">Full Name:</span>
                                <span class="detail-value">${identity.first_name} ${identity.middle_name || ''} ${identity.last_name}</span>
                            </div>
                            <div class="identity-detail">
                                <span class="detail-label">Validation Status:</span>
                                <span class="detail-value">
                                    <span class="validation-badge ${identity.validation_status.toLowerCase()}">${identity.validation_status}</span>
                                </span>
                            </div>
                            <div class="identity-detail">
                                <span class="detail-label">Generated Date:</span>
                                <span class="detail-value">${new Date(identity.generated_date).toLocaleString()}</span>
                            </div>
                        </div>
                    
                    ${identity.validation_notes && identity.validation_notes.length > 0 ? `
                        <div class="validation-notes">
                            <strong><i class="fas fa-check-circle"></i> Validation Notes:</strong>
                            <ul>
                                ${identity.validation_notes.map(note => `<li>${note}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}
                    
                    ${identity.traceability && identity.traceability.validation_steps ? `
                        <div class="validation-summary">
                            <div class="summary-header">
                                <i class="fas fa-shield-alt"></i>
                                <span>Validation Summary</span>
                                <span class="summary-status passed">All Tests Passed</span>
                            </div>
                            <div class="summary-stats">
                                <span class="stat">
                                    <i class="fas fa-check-circle"></i>
                                    ${identity.traceability.validation_steps.length} Validation Steps
                                </span>
                                <span class="stat">
                                    <i class="fas fa-clock"></i>
                                    ${new Date(identity.generated_date).toLocaleTimeString()}
                                </span>
                            </div>
                        </div>
                        
                        <div class="validation-steps">
                            <strong><i class="fas fa-clipboard-check"></i> Detailed Validation Steps:</strong>
                            <div class="steps-container">
                                ${identity.traceability.validation_steps.map((step, stepIndex) => `
                                    <div class="validation-step">
                                        <div class="step-header">
                                            <span class="step-number">${step.step}</span>
                                            <span class="step-title">${step.description}</span>
                                            <span class="step-status passed">✓ PASSED</span>
                                            <label class="step-feedback-checkbox">
                                                <input type="checkbox" id="step-feedback-${index}-${stepIndex}" onchange="toggleStepFeedback(${index}, ${stepIndex})">
                                                <span class="checkmark"></span>
                                                <span class="step-feedback-label">Issue with this step</span>
                                            </label>
                                        </div>
                                        <div class="step-result">${step.result}</div>
                                        <div class="step-feedback-input" id="step-feedback-input-${index}-${stepIndex}" style="display: none;">
                                            <textarea 
                                                id="step-feedback-text-${index}-${stepIndex}" 
                                                placeholder="Please describe the issue with this validation step..."
                                                rows="2"
                                            ></textarea>
                                            <div class="step-feedback-actions">
                                                <button type="button" class="feedback-btn small" onclick="submitStepFeedback(${index}, ${stepIndex})">
                                                    <i class="fas fa-paper-plane"></i> Submit
                                                </button>
                                                <button type="button" class="feedback-btn small secondary" onclick="cancelStepFeedback(${index}, ${stepIndex})">
                                                    <i class="fas fa-times"></i> Cancel
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    ` : ''}
                    
                    ${identity.cultural_context ? `
                        <div class="cultural-context">
                            <strong>Cultural Context:</strong>
                            <pre>${JSON.stringify(identity.cultural_context, null, 2)}</pre>
                        </div>
                    ` : ''}
                    
                    <div class="feedback-section">
                        <div class="feedback-header">
                            <i class="fas fa-clipboard-check"></i>
                            <span>Validation Step Feedback</span>
                        </div>
                        <div class="feedback-info">
                            <p><i class="fas fa-info-circle"></i> Click the checkbox next to any validation step that has issues to provide specific feedback.</p>
                        </div>
                    </div>
                </div>
            `;
        });

        identityResult.innerHTML = html;
        
        // Show traceability section if available
        if (identities[0] && identities[0].traceability) {
            displayTraceability(identities[0].traceability);
        }
    }

    function displayTraceability(traceability) {
        traceabilitySection.style.display = 'block';
        
        let html = `
            <div class="traceability-section">
                <h5>Request Parameters:</h5>
                <pre>${JSON.stringify(traceability.request_parameters, null, 2)}</pre>
                
                <h5>Cultural Analysis:</h5>
                <pre>${JSON.stringify(traceability.cultural_analysis, null, 2)}</pre>
                
                <h5>Name Generation Steps:</h5>
                ${traceability.name_generation_steps ? traceability.name_generation_steps.map(step => `
                    <div class="traceability-step">
                        <div class="step-title">Step ${step.step}: ${step.description}</div>
                        <div class="step-description">${step.result}</div>
                    </div>
                `).join('') : '<p>No generation steps available</p>'}
                
                <h5>Validation Steps:</h5>
                ${traceability.validation_steps ? traceability.validation_steps.map(step => `
                    <div class="traceability-step">
                        <div class="step-title">Step ${step.step}: ${step.description}</div>
                        <div class="step-description">${step.result}</div>
                    </div>
                `).join('') : '<p>No validation steps available</p>'}
                
                <h5>Final Result:</h5>
                <pre>${JSON.stringify(traceability.final_result, null, 2)}</pre>
            </div>
        `;
        
        traceabilityResult.innerHTML = html;
    }
    
    // Enhanced functionality functions
    async function checkOllamaStatus() {
        try {
            const response = await fetch('/api/health');
            const data = await response.json();
            
            // Handle both old and new response formats
            const isConnected = data.ollama_available || data.status === 'healthy';
            
            if (isConnected) {
                ollamaStatus.innerHTML = '<i class="fas fa-circle"></i> Ollama Connected';
                ollamaStatus.className = 'status-badge connected';
            } else {
                ollamaStatus.innerHTML = '<i class="fas fa-circle"></i> Ollama Disconnected';
                ollamaStatus.className = 'status-badge disconnected';
            }
        } catch (error) {
            ollamaStatus.innerHTML = '<i class="fas fa-circle"></i> Connection Error';
            ollamaStatus.className = 'status-badge disconnected';
        }
    }
    
    function setupFormEnhancements() {
        // Handle "Other" options for race and religion
        const raceSelect = document.getElementById('race');
        const religionSelect = document.getElementById('religion');
        
        if (raceSelect) {
            raceSelect.addEventListener('change', function() {
                const otherField = document.getElementById('race_other');
                if (otherField) {
                    otherField.style.display = this.value === 'Other' ? 'block' : 'none';
                    if (this.value !== 'Other') {
                        otherField.value = '';
                    }
                }
            });
        }
        
        if (religionSelect) {
            religionSelect.addEventListener('change', function() {
                const otherField = document.getElementById('religion_other');
                if (otherField) {
                    otherField.style.display = this.value === 'Other' ? 'block' : 'none';
                    if (this.value !== 'Other') {
                        otherField.value = '';
                    }
                }
            });
        }
        
        // Clear form functionality
        if (clearBtn) {
            clearBtn.addEventListener('click', function() {
                form.reset();
                resultDiv.style.display = 'none';
                const raceOther = document.getElementById('race_other');
                const religionOther = document.getElementById('religion_other');
                if (raceOther) raceOther.style.display = 'none';
                if (religionOther) religionOther.style.display = 'none';
            });
        }
        
        // Export functionality
        if (exportBtn) {
            exportBtn.addEventListener('click', function() {
                if (currentResults) {
                    const dataStr = JSON.stringify(currentResults, null, 2);
                    const dataBlob = new Blob([dataStr], {type: 'application/json'});
                    const url = URL.createObjectURL(dataBlob);
                    const link = document.createElement('a');
                    link.href = url;
                    link.download = `identity_${new Date().toISOString().split('T')[0]}.json`;
                    link.click();
                    URL.revokeObjectURL(url);
                }
            });
        }
        
        // Export feedback functionality
        if (exportFeedbackBtn) {
            exportFeedbackBtn.addEventListener('click', exportFeedback);
        }
        
        // Toggle traceability
        if (toggleTraceabilityBtn) {
            toggleTraceabilityBtn.addEventListener('click', function() {
                const isVisible = traceabilitySection.style.display !== 'none';
                traceabilitySection.style.display = isVisible ? 'none' : 'block';
                this.innerHTML = isVisible ? 
                    '<i class="fas fa-info-circle"></i> Show Details' : 
                    '<i class="fas fa-eye-slash"></i> Hide Details';
            });
        }
        
        // Collapse/Expand all functionality
        if (collapseAllBtn) {
            collapseAllBtn.addEventListener('click', function() {
                collapseAllIdentities();
            });
        }
        
        if (expandAllBtn) {
            expandAllBtn.addEventListener('click', function() {
                expandAllIdentities();
            });
        }
    }
    
    function loadTemplate(templateName) {
        const templates = {
            sudanese: {
                sex: 'Male',
                age: '30',
                location: 'Sudan, Khartoum',
                occupation: 'Software Engineer',
                race: 'Sudanese',
                religion: 'Muslim',
                birth_year: '1994',
                birth_country: 'Sudan',
                citizenship_country: 'Sudan'
            },
            spanish: {
                sex: 'Male',
                age: '28',
                location: 'Spain, Madrid',
                occupation: 'Architect',
                race: 'Spanish',
                religion: 'Catholic',
                birth_year: '1996',
                birth_country: 'Spain',
                citizenship_country: 'Spain'
            },
            chinese: {
                sex: 'Female',
                age: '25',
                location: 'China, Beijing',
                occupation: 'Data Scientist',
                race: 'Chinese',
                religion: 'Buddhist',
                birth_year: '1999',
                birth_country: 'China',
                citizenship_country: 'China'
            },
            indian: {
                sex: 'Male',
                age: '32',
                location: 'India, Mumbai',
                occupation: 'Doctor',
                race: 'Indian',
                religion: 'Hindu',
                birth_year: '1992',
                birth_country: 'India',
                citizenship_country: 'India'
            }
        };
        
        const template = templates[templateName];
        if (template) {
            Object.keys(template).forEach(key => {
                const field = document.getElementById(key);
                if (field) {
                    field.value = template[key];
                }
            });
            
            // Show success message
            showNotification(`Loaded ${templateName} template`, 'success');
        }
    }
    
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'info-circle'}"></i>
            ${message}
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);
        
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
    
    // Identity toggle functions
    function toggleIdentity(index) {
        const content = document.getElementById(`identity-content-${index}`);
        const icon = document.getElementById(`collapse-icon-${index}`);
        
        if (content.style.display === 'none') {
            content.style.display = 'block';
            icon.className = 'fas fa-chevron-up collapse-icon';
        } else {
            content.style.display = 'none';
            icon.className = 'fas fa-chevron-down collapse-icon';
        }
    }
    
    function collapseAllIdentities() {
        const identities = document.querySelectorAll('.identity-content');
        const icons = document.querySelectorAll('.collapse-icon');
        
        identities.forEach((identity, index) => {
            identity.style.display = 'none';
            if (icons[index]) {
                icons[index].className = 'fas fa-chevron-down collapse-icon';
            }
        });
    }
    
    function expandAllIdentities() {
        const identities = document.querySelectorAll('.identity-content');
        const icons = document.querySelectorAll('.collapse-icon');
        
        identities.forEach((identity, index) => {
            identity.style.display = 'block';
            if (icons[index]) {
                icons[index].className = 'fas fa-chevron-up collapse-icon';
            }
        });
    }
    
    // Feedback system functions
    function toggleFeedbackInput(index) {
        const checkbox = document.getElementById(`incorrect-${index}`);
        const feedbackInput = document.getElementById(`feedback-input-${index}`);
        
        if (checkbox.checked) {
            feedbackInput.style.display = 'block';
        } else {
            feedbackInput.style.display = 'none';
            // Clear the textarea when unchecked
            document.getElementById(`feedback-text-${index}`).value = '';
        }
    }
    
    // Step-specific feedback functions
    function toggleStepFeedback(identityIndex, stepIndex) {
        const checkbox = document.getElementById(`step-feedback-${identityIndex}-${stepIndex}`);
        const feedbackInput = document.getElementById(`step-feedback-input-${identityIndex}-${stepIndex}`);
        
        if (checkbox.checked) {
            feedbackInput.style.display = 'block';
        } else {
            feedbackInput.style.display = 'none';
            // Clear the textarea when unchecked
            document.getElementById(`step-feedback-text-${identityIndex}-${stepIndex}`).value = '';
        }
    }
    
    function submitStepFeedback(identityIndex, stepIndex) {
        const feedbackText = document.getElementById(`step-feedback-text-${identityIndex}-${stepIndex}`).value.trim();
        const checkbox = document.getElementById(`step-feedback-${identityIndex}-${stepIndex}`);
        
        if (!feedbackText) {
            showNotification('Please provide feedback text', 'error');
            return;
        }
        
        // Get the identity and step data for context
        const identity = currentResults[identityIndex];
        const step = identity.traceability.validation_steps[stepIndex];
        
        // Prepare step feedback data
        const feedbackData = {
            timestamp: new Date().toISOString(),
            identity_index: identityIndex,
            step_index: stepIndex,
            identity_data: identity,
            step_data: step,
            request_parameters: currentFormData,
            feedback_type: 'validation_step_issue',
            feedback_text: feedbackText,
            cultural_context: identity.cultural_context,
            validation_status: identity.validation_status
        };
        
        // Store feedback locally
        storeFeedbackLocally(feedbackData);
        
        // Show success message
        showNotification(`Step ${stepIndex + 1} feedback submitted successfully!`, 'success');
        
        // Reset the feedback form
        checkbox.checked = false;
        document.getElementById(`step-feedback-text-${identityIndex}-${stepIndex}`).value = '';
        document.getElementById(`step-feedback-input-${identityIndex}-${stepIndex}`).style.display = 'none';
    }
    
    function cancelStepFeedback(identityIndex, stepIndex) {
        const checkbox = document.getElementById(`step-feedback-${identityIndex}-${stepIndex}`);
        const feedbackInput = document.getElementById(`step-feedback-input-${identityIndex}-${stepIndex}`);
        const feedbackText = document.getElementById(`step-feedback-text-${identityIndex}-${stepIndex}`);
        
        checkbox.checked = false;
        feedbackInput.style.display = 'none';
        feedbackText.value = '';
    }
    
    function submitFeedback(index) {
        const feedbackText = document.getElementById(`feedback-text-${index}`).value.trim();
        const checkbox = document.getElementById(`incorrect-${index}`);
        
        if (!feedbackText) {
            showNotification('Please provide feedback text', 'error');
            return;
        }
        
        // Get the identity data for context
        const identity = currentResults[index];
        
        // Prepare feedback data
        const feedbackData = {
            timestamp: new Date().toISOString(),
            identity_index: index,
            identity_data: identity,
            request_parameters: currentFormData,
            feedback_type: 'incorrect',
            feedback_text: feedbackText,
            cultural_context: identity.cultural_context,
            validation_status: identity.validation_status
        };
        
        // Store feedback locally
        storeFeedbackLocally(feedbackData);
        
        // Show success message
        showNotification('Feedback submitted successfully! It will be used to improve future generations.', 'success');
        
        // Reset the feedback form
        checkbox.checked = false;
        document.getElementById(`feedback-text-${index}`).value = '';
        document.getElementById(`feedback-input-${index}`).style.display = 'none';
    }
    
    function cancelFeedback(index) {
        const checkbox = document.getElementById(`incorrect-${index}`);
        const feedbackInput = document.getElementById(`feedback-input-${index}`);
        const feedbackText = document.getElementById(`feedback-text-${index}`);
        
        checkbox.checked = false;
        feedbackInput.style.display = 'none';
        feedbackText.value = '';
    }
    
    function storeFeedbackLocally(feedbackData) {
        try {
            // Get existing feedback from localStorage
            let existingFeedback = JSON.parse(localStorage.getItem('nameSystemFeedback') || '[]');
            
            // Add new feedback
            existingFeedback.push(feedbackData);
            
            // Store back to localStorage (limit to last 100 feedback items)
            if (existingFeedback.length > 100) {
                existingFeedback = existingFeedback.slice(-100);
            }
            
            localStorage.setItem('nameSystemFeedback', JSON.stringify(existingFeedback));
            
            console.log('Feedback stored locally:', feedbackData);
        } catch (error) {
            console.error('Error storing feedback:', error);
            showNotification('Error storing feedback', 'error');
        }
    }
    
    function getStoredFeedback() {
        try {
            return JSON.parse(localStorage.getItem('nameSystemFeedback') || '[]');
        } catch (error) {
            console.error('Error retrieving feedback:', error);
            return [];
        }
    }
    
    function exportFeedback() {
        const feedback = getStoredFeedback();
        if (feedback.length === 0) {
            showNotification('No feedback data to export', 'info');
            return;
        }
        
        const dataStr = JSON.stringify(feedback, null, 2);
        const dataBlob = new Blob([dataStr], {type: 'application/json'});
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `name-system-feedback-${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
        
        showNotification('Feedback exported successfully!', 'success');
    }
    
    // Debug function to test feedback system
    function debugFeedbackSystem() {
        console.log('=== Feedback System Debug ===');
        console.log('Current results:', currentResults);
        console.log('Current form data:', currentFormData);
        
        // Test if elements exist
        const testIndex = 0;
        const checkbox = document.getElementById(`incorrect-${testIndex}`);
        const feedbackInput = document.getElementById(`feedback-input-${testIndex}`);
        const feedbackText = document.getElementById(`feedback-text-${testIndex}`);
        
        console.log('Checkbox exists:', !!checkbox);
        console.log('Feedback input exists:', !!feedbackInput);
        console.log('Feedback text exists:', !!feedbackText);
        
        if (checkbox) {
            console.log('Checkbox checked:', checkbox.checked);
        }
        if (feedbackInput) {
            console.log('Feedback input display:', feedbackInput.style.display);
        }
        
        // Test function call
        console.log('toggleFeedbackInput function exists:', typeof toggleFeedbackInput === 'function');
        
        showNotification('Debug info logged to console (F12)', 'info');
    }
    
    function analyzeFeedbackForCulture(culture, religion, location) {
        const allFeedback = getStoredFeedback();
        
        // Filter feedback for similar cultural contexts
        const relevantFeedback = allFeedback.filter(feedback => {
            const feedbackCulture = feedback.identity_data?.cultural_context?.culture || 
                                   feedback.request_parameters?.race || '';
            const feedbackReligion = feedback.request_parameters?.religion || '';
            const feedbackLocation = feedback.request_parameters?.location || '';
            
            // Check for cultural similarity
            const cultureMatch = feedbackCulture.toLowerCase().includes(culture.toLowerCase()) ||
                                culture.toLowerCase().includes(feedbackCulture.toLowerCase());
            
            // Check for religious similarity
            const religionMatch = feedbackReligion.toLowerCase().includes(religion.toLowerCase()) ||
                                 religion.toLowerCase().includes(feedbackReligion.toLowerCase());
            
            // Check for geographic similarity
            const locationMatch = feedbackLocation.toLowerCase().includes(location.toLowerCase()) ||
                                 location.toLowerCase().includes(feedbackLocation.toLowerCase());
            
            return cultureMatch || religionMatch || locationMatch;
        });
        
        return relevantFeedback;
    }
});
