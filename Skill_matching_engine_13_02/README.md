# Skill Matching Engine – Module Overview

The Skill Matching Engine is an AI-driven employee-task allocation system designed to automate resource planning by evaluating employee skills, workload, and task requirements. The system follows a modular architecture where each component performs an independent responsibility within the overall assignment pipeline.

---

## Module 1 — Employee Skill Profile Management

### Objective
Collect and maintain structured employee information required for intelligent task allocation.

### Responsibilities
- Employee authentication
- Personal information management
- Technical skill collection
- Programming language selection
- Framework and technology mapping
- Experience management
- Tool and IDE selection
- Availability information
- Employee profile storage

### Output
Structured employee profile stored in the database.
---
## Module 2 — Task Requirement Management

### Objective
Capture task requirements from project managers in a structured format.

### Responsibilities
- Create new task
- Task description
- Required technologies
- Required programming languages
- Experience requirements
- Priority definition
- Start date
- Deadline
- Estimated effort
- Complexity information

### Output
Structured task profile stored in the database.

---

## Module 3 — Requirement Extraction Engine

### Objective
Convert task information into an AI-compatible requirement profile.

### Responsibilities
- Process task description
- Extract required technologies
- Identify skill requirements
- Normalize task metadata
- Prepare task embedding input
- Generate structured task representation

### Output
AI-ready task requirement profile.
---

## Module 4 — Employee Feature Engineering Engine

### Objective
Transform employee profile data into machine-readable feature vectors.

### Responsibilities
- Process employee skills
- Normalize technical information
- Generate employee embeddings
- Store employee vectors
- Maintain vector database

### Output
PRE-PROCESSING and skill validation using Geminie API. Display Score. 
---

## Module 5 — Skill Matching Engine

### Objective
Calculate semantic similarity between employee skills and task requirements.

### Responsibilities
- Retrieve employee embeddings
- Retrieve task embeddings
- Calculate cosine similarity
- Generate employee-task similarity matrix
- Store recommendation results

### Output
Employee-task similarity scores.

---

## Module 6 — Resource Balancing Engine

### Objective
Evaluate employee workload before assigning a task to ensure balanced resource utilization.

### Responsibilities
- Calculate available working hours
- Compute active task count
- Estimate workload
- Calculate utilization percentage
- Generate workload score
- Calculate resource balancing score
- Produce final workload score

### Output
Employee workload assessment.
---

## Module 7 — Assignment Decision Engine

### Objective
Select the most suitable employee for each task using skill similarity and workload analysis.

### Responsibilities
- Merge similarity score
- Merge workload score
- Calculate final assignment score
- Apply one employee–one task constraint
- Apply one task–one employee constraint
- Rank candidates
- Generate final task assignments
- Store assignment results

### Output
Final employee-task assignment.
---

## Module 8 — Assignment Visualization Dashboard

### Objective
Provide a clear explanation of the assignment decision to employees and administrators.

### Responsibilities
- Display assigned task
- Display employee information
- Display similarity score
- Display workload score
- Display overall match score
- Visualize assignment metrics
- Present assignment summary

### Output
Interactive assignment dashboard.
---

# Complete Workflow

```
Employee Registration
        │
        ▼
Employee Skill Profile Management
        │
        ▼
Task Requirement Management
        │
        ▼
Requirement Extraction Engine
        │
        ▼
Employee Feature Engineering Engine
        │
        ▼
Skill Matching Engine
        │
        ▼
Resource Balancing Engine
        │
        ▼
Assignment Decision Engine
        │
        ▼
Assignment Visualization Dashboard
```
---

# Installation

Clone repository

```bash
git clone https://github.com/username/AI-Skill-Matching-Engine.git
```

Move into project

```bash
cd Skill_matching_engine
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create

```
.env
```

Add

```env
SUPABASE_URL=YOUR_SUPABASE_URL

SUPABASE_KEY=YOUR_SUPABASE_KEY

GEMINI_API_KEY= YOUR_GEMINIE_KEY
```

---

# Running Backend

```bash
python -m uvicorn backend.main:app --reload
```

---

# Running AI Engine

```bash
python -m backend.ai_engine.run_engine
```
---

# Key Features

- AI-based semantic skill matching
- Sentence embedding generation
- Cosine similarity computation
- Workload-aware resource balancing
- Automated task assignment
- One Employee → One Task allocation
- One Task → One Employee allocation
- Assignment explanation dashboard
- Modular and scalable architecture
- REST API integration using FastAPI
