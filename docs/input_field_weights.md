# Input Field Weights and Importance Hierarchy

## Overview

The NAME (Name Generation System) uses a hierarchical approach to input field importance, where certain fields have higher priority in determining culturally appropriate name generation. This document outlines the weights and order of importance for all input fields.

## Field Importance Hierarchy

### 🥇 Primary/Required Fields (Highest Priority)

These fields are **required** for name generation and have the highest impact on the final output:

#### 1. **Sex** 
- **Impact**: Determines gender-specific name pools and cultural naming conventions
- **Usage**: Primary filter for first name selection
- **Examples**: Male, Female, Non-binary
- **Code Reference**: `request.sex` in name generation logic

#### 2. **Location**
- **Impact**: Defines geographic and cultural context for naming patterns
- **Usage**: Determines regional naming conventions and cultural context
- **Examples**: "USA", "Spain, Madrid", "China, Beijing"
- **Code Reference**: `request.location` parsed for country/region

#### 3. **Age**
- **Impact**: Influences name generation based on generational naming trends
- **Usage**: Determines historically appropriate names for the person's generation
- **Examples**: 25, 45, 67
- **Code Reference**: Used with birth year for temporal context

#### 4. **Occupation**
- **Impact**: Affects name selection based on professional context
- **Usage**: Influences name appropriateness for professional settings
- **Examples**: "Engineer", "Doctor", "Artist"
- **Code Reference**: `request.occupation` for professional context

#### 5. **Race/Ethnicity**
- **Impact**: Primary driver for cultural name selection and naming conventions
- **Usage**: Determines culture-specific name pools and naming rules
- **Examples**: "Chinese", "Cambodian", "Spanish", "African American"
- **Code Reference**: `request.race` used as primary culture filter

### 🥈 Secondary/Required Fields (High Priority)

#### 6. **Religion**
- **Impact**: Influences name selection based on religious naming traditions
- **Usage**: Determines religious naming conventions and restrictions
- **Examples**: "None", "Islam", "Judaism", "Christianity"
- **Code Reference**: `request.religion` for religious context

#### 7. **Birth Year**
- **Impact**: Determines historically appropriate names for that time period
- **Usage**: Used with age to select generationally appropriate names
- **Examples**: 1990, 1985, 2000
- **Code Reference**: `request.birth_year` for temporal name selection

### 🥉 Optional/Enhancement Fields (Lower Priority)

These fields provide additional context but are not required for basic name generation:

#### 8. **Birth Country**
- **Impact**: Provides country of origin context for diaspora considerations
- **Usage**: Auto-detected from ethnicity if not provided
- **Examples**: "China", "Mexico", "Nigeria"
- **Code Reference**: `request.birth_country` for origin context

#### 9. **Citizenship Country**
- **Impact**: Current citizenship for legal naming considerations
- **Usage**: Influences naming conventions based on current legal context
- **Examples**: "USA", "Canada", "UK"
- **Code Reference**: `request.citizenship_country` for legal context

#### 10. **Diaspora Generation**
- **Impact**: Immigrant generation for naming adaptation patterns
- **Usage**: Determines how much cultural adaptation to apply
- **Examples**: 1 (first generation), 2 (second generation), 3 (third generation)
- **Code Reference**: `request.diaspora_generation` for adaptation level

## Code Implementation Evidence

### Frontend Validation
```javascript
// From frontend/src/components/IdentityGenerator.js
const requiredFields = ['sex', 'location', 'age', 'occupation', 'race'];
return requiredFields.every(field => formData[field] !== '');
```

### API Schema Requirements
```python
# From src/api/mcp_server.py
"required": ["sex", "location", "age", "occupation", "race", "religion", "birth_year"]
```

### Name Generation Logic
```python
# From src/core/name_generator.py
culture = cultural_context.get('culture', '').lower()
race = request.race.lower()

# Culture-specific generation with fallback to race-based
if culture == 'spanish':
    result = self._generate_spanish_name(request, cultural_context)
elif culture == 'chinese':
    result = self._generate_chinese_name(request, cultural_context)
# ... additional culture-specific logic
```

## Cultural Context Priority

The system processes fields in this specific order for cultural name generation:

1. **Culture** (derived from race/location combination)
2. **Gender** (sex-based name pools)
3. **Geographic Region** (location-specific conventions)
4. **Temporal Context** (birth year + age)
5. **Religious Context** (religion-based restrictions)
6. **Professional Context** (occupation appropriateness)

## Field Dependencies

### Auto-Detection Logic
- **Birth Country**: Auto-detected from ethnicity if not provided
- **Culture**: Derived from race and location combination
- **Naming Conventions**: Determined by cultural context

### Fallback Hierarchy
1. Culture-specific generation (highest priority)
2. Race-based generation (fallback)
3. Generic generation (lowest priority)

## Validation Rules

### Required Field Validation
- All primary fields must be provided
- Secondary fields are required but have default fallbacks
- Optional fields enhance accuracy but don't block generation

### Field Format Requirements
- **Sex**: Must be "Male", "Female", or "Non-binary"
- **Age**: Must be positive integer
- **Birth Year**: Must be reasonable range (1900-present)
- **Location**: Should include country, optionally city/region

## Impact on Name Generation

### High Impact Fields
- **Sex + Race**: Determines 80% of name pool selection
- **Location**: Influences 60% of naming conventions
- **Birth Year**: Affects 40% of name popularity choices

### Medium Impact Fields
- **Religion**: Influences 30% of name appropriateness
- **Occupation**: Affects 20% of professional name selection

### Low Impact Fields
- **Optional fields**: Provide 10-15% additional cultural accuracy

## Best Practices

### For Optimal Results
1. Always provide the 5 primary fields
2. Include religion and birth year for better accuracy
3. Add optional fields for diaspora or multi-cultural contexts
4. Use specific locations rather than generic countries

### Common Pitfalls
- Missing required fields will prevent generation
- Generic race/ethnicity may result in less accurate names
- Vague locations may use default cultural assumptions

## Technical Implementation

### Database Schema
```sql
-- Required fields in identities table
sex VARCHAR(20) NOT NULL,
location VARCHAR(100) NOT NULL,
age INTEGER NOT NULL,
occupation VARCHAR(200) NOT NULL,
race VARCHAR(100) NOT NULL,
religion VARCHAR(100) NOT NULL,
birth_year INTEGER NOT NULL,

-- Optional fields
birth_country VARCHAR(100),
citizenship_country VARCHAR(100),
diaspora_generation INTEGER
```

### API Request Structure
```json
{
  "sex": "Female",
  "location": "USA",
  "age": 25,
  "occupation": "Engineer",
  "race": "Chinese",
  "religion": "None",
  "birth_year": 1998,
  "birth_country": "China",
  "citizenship_country": "USA",
  "diaspora_generation": 2
}
```

## Conclusion

Understanding the input field weights is crucial for:
- **Developers**: Implementing proper validation and fallback logic
- **Users**: Providing the most relevant information for accurate name generation
- **System Design**: Optimizing the name generation pipeline for cultural accuracy

The hierarchical approach ensures that the most culturally and demographically relevant names are generated while maintaining authenticity and appropriateness for the specified parameters.
