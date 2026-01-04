<!--
  SYNC IMPACT REPORT
  ==================
  Version change: 0.0.0 → 1.0.0
  Bump rationale: MAJOR - Initial constitution creation with full principle definitions

  Modified principles: N/A (new constitution)

  Added sections:
  - 7 Core Principles (Accuracy, Clarity, Reproducibility, Rigor, Security, Testing, Documentation)
  - Constraints section
  - Development Phases section (5 phases: CLI → Web → AI Chatbot → K8s Local → Cloud)
  - Agent Guidelines section
  - Governance section

  Removed sections: N/A (new constitution)

  Templates alignment:
  - ✅ plan-template.md: Constitution Check section aligns with new principles
  - ✅ spec-template.md: Requirements and Success Criteria align with Testing/Documentation principles
  - ✅ tasks-template.md: Test-first approach and phase structure compatible
  - ✅ phr-template.prompt.md: No changes needed

  Follow-up TODOs: None
-->

# The Evolution of Todo Constitution

## Project Overview

**Project**: The Evolution of Todo
**Focus**: From CLI to Distributed Cloud-Native AI Systems
**Goal**: Students act as Product Architects, using AI to build progressively complex software without writing boilerplate code.

## Core Principles

### I. Accuracy

All claims and code MUST follow verified specifications. Every implementation decision MUST be traceable to a specification document or explicit user requirement.

- All code MUST implement exactly what is specified—no more, no less
- Claims about functionality MUST be verifiable through tests or demonstration
- Deviations from specifications MUST be documented and justified
- External API integrations MUST follow official documentation

### II. Clarity

All code, comments, and documentation MUST be readable by computer science-level reviewers. Clarity enables maintainability and knowledge transfer.

- Code MUST use descriptive naming conventions following language standards
- Comments MUST explain "why" rather than "what" (self-documenting code for the latter)
- Documentation MUST be structured consistently across all project phases
- Architecture decisions MUST be recorded in ADRs when significant

### III. Reproducibility

Any feature MUST be implementable using given specs; all claims MUST be traceable. This ensures any developer can recreate the system from specifications alone.

- Build processes MUST be deterministic (same inputs → same outputs)
- Dependencies MUST be version-locked and documented
- Environment setup MUST be scriptable and documented
- All implementation steps MUST reference their source specification

### IV. Rigor

Use peer-reviewed or authoritative sources wherever applicable. Technical decisions MUST be grounded in established best practices.

- Architecture patterns MUST follow industry-accepted principles
- Security implementations MUST align with OWASP guidelines
- Database designs MUST follow normalization best practices (unless justified)
- API designs MUST follow REST/GraphQL conventions as specified

### V. Security

Follow JWT, API security, and data protection best practices. Security is non-negotiable across all project phases.

- Authentication MUST use JWT with proper token management (Phase II+)
- API endpoints MUST validate all inputs and authenticate requests
- Secrets MUST be stored in environment variables, never in code
- Data at rest and in transit MUST be encrypted where applicable
- OWASP Top 10 vulnerabilities MUST be actively prevented

### VI. Testing

Unit, integration, and system tests MUST be defined for each feature. Testing validates that implementations meet specifications.

- Each feature MUST have corresponding test coverage
- Tests MUST be written before implementation when using TDD approach
- Integration tests MUST verify component interactions
- System tests MUST validate end-to-end user journeys
- Test failures MUST block deployment

### VII. Documentation

Each feature MUST have setup instructions and CLAUDE.md guidance. Documentation enables reproducibility and onboarding.

- README.md MUST include project overview and quick start
- CLAUDE.md MUST provide AI assistant guidance for development
- API documentation MUST be generated from code (OpenAPI/Swagger)
- Each phase MUST have its own setup instructions

## Constraints

- **Plagiarism**: 0% tolerance—all code must be original or properly attributed
- **Coding Conventions**: Follow standard conventions for Python (PEP 8) and TypeScript (ESLint/Prettier)
- **Development Methodology**: Specs-driven development is mandatory using Claude Code + Spec-Kit Plus
- **File Formats**: Markdown for specifications, PDF for final reports if any
- **Spec References**: Use @specs/filename.md convention for referencing specifications

## Development Phases

### Phase I: CLI Todo App

**Objectives**:
- Build command-line todo app storing tasks in memory
- Implement all basic features: Add, Delete, Update, View, Mark Complete

**Rules**:
- Follow clean Python project structure
- Use spec-driven implementation; no manual code copying
- Each feature must be testable in console

**Deliverables**: `/src`, `/specs`, `CLAUDE.md`, `README.md`

**Success Criteria**:
- CLI app fully functional with all 5 features
- All specs are referenced and followed
- Tests pass without errors

---

### Phase II: Full-Stack Web App

**Objectives**:
- Transform CLI app into multi-user web application with persistent storage

**Rules**:
- Implement RESTful API endpoints and frontend interface
- JWT-based auth using Better Auth; all API requests must validate JWT
- Database: Neon Serverless PostgreSQL; ORM: SQLModel
- Follow responsive UI principles with Next.js + Tailwind

**Deliverables**: `/frontend`, `/backend`, `/specs`, `CLAUDE.md`, `README.md`

**Success Criteria**:
- Web app fully functional with task CRUD and auth
- API endpoints pass JWT authentication and return correct user-specific data
- UI is responsive and accessible

---

### Phase III: AI Chatbot

**Objectives**:
- Build AI-powered chatbot for managing todos via natural language

**Rules**:
- Use OpenAI Agents SDK + MCP server for task operations
- Stateless server; conversation history stored in database
- Chatbot must use MCP tools: add_task, list_tasks, complete_task, delete_task, update_task
- Agent must confirm all user actions and handle errors gracefully

**Deliverables**: `/frontend` (ChatKit UI), `/backend` (FastAPI + MCP), `/specs`, database migration scripts, `README.md`

**Success Criteria**:
- Chatbot manages tasks via natural language commands
- AI actions correctly invoke MCP tools
- All responses confirm user actions and maintain stateless conversation integrity

---

### Phase IV: Local Kubernetes Deployment

**Objectives**:
- Deploy the chatbot on local Kubernetes cluster (Minikube)

**Rules**:
- Containerize frontend and backend apps (Docker/Gordon)
- Use Helm charts, kubectl-ai, or Kagent for AI-assisted deployment
- Ensure environment reproducibility across developers

**Deliverables**: Helm charts, Dockerfiles, deployment scripts, updated `README.md`

**Success Criteria**:
- App fully deployable locally on Kubernetes
- Containers run correctly; AI agent functional
- Logs and monitoring accessible

---

### Phase V: Cloud Deployment

**Objectives**:
- Deploy app to production-grade Kubernetes (Azure AKS / GCP GKE / Oracle OKE)
- Implement advanced features: recurring tasks, due dates, reminders, event-driven architecture with Kafka and Dapr

**Rules**:
- CI/CD pipeline using GitHub Actions
- Dapr sidecars for Pub/Sub, state management, and service invocation
- Kafka for event-driven messaging; audit logs and real-time updates must work
- Environment variables and secrets configured securely

**Deliverables**: Cloud deployment scripts, CI/CD configuration, full operational system

**Success Criteria**:
- App fully functional in cloud with advanced features
- Event-driven system publishes and consumes messages correctly
- System resilient, scalable, and stateless where required

## Agent Guidelines

- Reference all specs using `@specs/filename.md` convention
- Read relevant CLAUDE.md files for frontend/backend conventions
- Phase-wise rules override global rules when specified
- All deliverables must include setup instructions and test verification
- Use latest MCP context (context7 MCP) for AI-related implementations

## Governance

This constitution supersedes all other development practices for The Evolution of Todo project.

### Amendment Procedure

1. Proposed amendments MUST be documented with rationale
2. Amendments MUST be reviewed and approved before implementation
3. Breaking changes MUST include migration plans
4. All amendments MUST be version-tracked

### Versioning Policy

- **MAJOR**: Backward incompatible principle changes or removals
- **MINOR**: New principles, sections, or materially expanded guidance
- **PATCH**: Clarifications, wording improvements, typo fixes

### Compliance Review

- All PRs MUST verify compliance with relevant principles
- Code reviews MUST check against phase-specific rules
- Complexity beyond specifications MUST be justified in ADRs

**Version**: 1.0.0 | **Ratified**: 2025-12-29 | **Last Amended**: 2025-12-29
