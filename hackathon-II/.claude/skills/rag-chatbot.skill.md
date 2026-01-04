# Skill: RAG Chatbot Development

## Metadata
- **Name**: rag-chatbot
- **Category**: development
- **Tags**: rag, chatbot, semantic-search, embeddings, llm, grounding, citations

## Description
Complete workflow for building, debugging, and validating Retrieval-Augmented Generation (RAG) chatbots with strict grounding, citation support, and production-ready error handling. Based on battle-tested patterns from Physical AI Robotics textbook chatbot.

## Inputs
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| mode | string | No | build | Workflow mode: build, debug, validate |
| stack | string | No | full | Stack: full, backend-only, frontend-only |
| deployment | string | No | hf-spaces | Target: hf-spaces, vercel, docker |

## Outputs
- Production-ready RAG chatbot with grounded responses
- Comprehensive error handling with user-friendly messages
- Citation support in `[Source: Title](URL)` format
- Dual-mode support (retrieval + selection)

---

# PART 1: BUILD WORKFLOW

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React)                         │
│  ChatWidget.jsx + CSS (floating, responsive, SSE streaming)     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                             │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────────┐ │
│  │ Rate Limiter│  │ Error Handler│  │ Streaming Service (SSE) │ │
│  └─────────────┘  └──────────────┘  └─────────────────────────┘ │
│                              │                                   │
│  ┌───────────────────────────┼───────────────────────────────┐  │
│  │                    ROUTER SERVICE                          │  │
│  │    Selection Mode ◄──────┴──────► Retrieval Mode          │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                   │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────────┐ │
│  │ Embedding   │  │ Search       │  │ Context Service         │ │
│  │ (Cohere)    │  │ (Qdrant)     │  │ (Token Management)      │ │
│  └─────────────┘  └──────────────┘  └─────────────────────────┘ │
│                              │                                   │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────────┐ │
│  │ Scope       │  │ Agent        │  │ Citation Service        │ │
│  │ Detection   │  │ (Gemini LLM) │  │                         │ │
│  └─────────────┘  └──────────────┘  └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │ Qdrant   │   │ Postgres │   │ Gemini   │
        │ (Vectors)│   │ (Content)│   │ (LLM)    │
        └──────────┘   └──────────┘   └──────────┘
```

## Stack Decisions (Non-Negotiable)

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Embeddings | Cohere embed-english-v3.0 | Best quality/cost ratio, 1024 dims |
| Vector DB | Qdrant Cloud | Free tier generous, fast, reliable |
| LLM | Gemini 2.5 Flash | Fast streaming, good grounding |
| Metadata | Neon Postgres | Serverless, free tier, reliable |
| Backend | FastAPI + Uvicorn | Async, SSE support, production-ready |
| Frontend | React widget | Embeddable, responsive |
| Deployment | HuggingFace Spaces | Free Docker hosting, secrets management |

## Directory Structure
```
chatbot/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app + CORS + middleware
│   ├── config.py            # Settings from environment
│   ├── exceptions.py        # Custom exceptions with user messages
│   ├── routers/
│   │   ├── chat.py          # /api/chat and /api/chat/stream
│   │   └── health.py        # /api/health
│   ├── services/
│   │   ├── agent_service.py     # LLM + prompts (CRITICAL)
│   │   ├── embedding_service.py # Cohere embeddings
│   │   ├── search_service.py    # Qdrant similarity search
│   │   ├── context_service.py   # Token budgeting
│   │   ├── scope_service.py     # Out-of-scope detection
│   │   ├── citation_service.py  # Citation extraction
│   │   ├── streaming_service.py # SSE handling
│   │   └── metadata_service.py  # Postgres content retrieval
│   └── models/
│       ├── chat_request.py
│       ├── chat_response.py
│       ├── query_context.py
│       └── book_chunk.py
├── requirements.txt
├── Dockerfile
├── README.md             # HF Spaces metadata required
└── .gitignore
```

---

## CRITICAL: Grounding Prompts

### Selection Mode Prompt (Hard Guardrail - Forbids External Knowledge)
```python
SELECTION_MODE_SYSTEM_PROMPT = """You are a helpful assistant explaining ONLY the user-selected text.

ABSOLUTE RULES (MUST FOLLOW):
1. You can ONLY use information from the selected text provided below.
2. You MUST NOT use any external knowledge, prior training, or information from other sources.
3. If the answer is not present in the selected text, you MUST respond EXACTLY with:
   "This information is not present in the selected text."
4. Do NOT guess, infer beyond what's written, or add context from outside the selection.
5. Do NOT cite any external sources - you are ONLY explaining the user's selection.
6. Keep explanations clear and focused on what is LITERALLY in the selected text.

IMPORTANT: If asked about something that cannot be directly answered from the selected text,
respond with: "This information is not present in the selected text."
"""
```

### Retrieval Mode Prompt (Grounded with Citations)
```python
RETRIEVAL_MODE_SYSTEM_PROMPT = """You are a helpful assistant for readers of the [BOOK_NAME] textbook.

RULES:
1. Answer ONLY using the provided context from the book
2. If context is insufficient, say "I couldn't find information about that in the book"
3. Include citations in format: [Source: {title}]({url})
4. Keep responses concise and educational
5. If asked about topics not in context, politely decline
6. Be honest about uncertainty - if you can't answer based on the context, say so clearly
"""
```

### Context Formatting for Prompts
```python
def format_context_for_prompt(self, context: QueryContext) -> str:
    if context.mode == "selection":
        # Clear boundaries for selection mode
        return f"""
SELECTED TEXT (this is the ONLY information you may use):
---
{selected_chunk.content}
---

User's question about this selection: {context.query}
"""
    else:
        # Retrieval mode with XML-style context
        formatted_chunks = []
        for chunk in context.chunks:
            formatted_chunks.append(
                f'<context source="{chunk.chapter_title}" section="{chunk.section_title}" url="{chunk.source_url}">\n{chunk.content}\n</context>'
            )
        return f"CONTEXT FROM BOOK:\n\n{context_text}\n\nQuestion: {context.query}"
```

---

## Out-of-Scope Detection

### Similarity Threshold
```python
SIMILARITY_THRESHOLD = 0.65  # Below this = out of scope
```

### Dual Detection (Similarity + LLM Response Analysis)
```python
def detect_out_of_scope(self, chunks, llm_response, llm_indicates_out_of_scope):
    # No chunks = definitely out of scope
    if not chunks:
        return True, "No relevant content found in the book", 1.0

    # Get highest similarity score
    highest_score = max(chunk.similarity_score for chunk in chunks)
    similarity_out_of_scope = highest_score < self.similarity_threshold

    # Both agree = high confidence out of scope
    if similarity_out_of_scope and llm_indicates_out_of_scope:
        return True, f"Low similarity ({highest_score:.2f}) and LLM uncertainty", 0.9

    # Only similarity indicates = medium confidence
    elif similarity_out_of_scope:
        return True, f"Low similarity ({highest_score:.2f})", 0.7

    # Only LLM indicates = lower confidence
    elif llm_indicates_out_of_scope:
        return True, "LLM indicated insufficient context", 0.7

    return False, "Relevant content found", highest_score
```

### LLM Response Analysis for Out-of-Scope
```python
OUT_OF_SCOPE_INDICATORS = [
    "couldn't find information about that in the book",
    "not mentioned in the provided context",
    "not covered in the provided text",
    "no information provided about",
    "not found in the context",
    "not in the book",
    "out of scope",
    "not discussed",
    "not addressed"
]

def is_out_of_scope_response(self, response_text: str) -> bool:
    response_lower = response_text.lower()
    return any(indicator in response_lower for indicator in OUT_OF_SCOPE_INDICATORS)
```

---

## Error Handling Pattern

### Custom Exception Hierarchy
```python
class ErrorCode(str, Enum):
    RATE_LIMIT_COHERE = "RATE_LIMIT_COHERE"
    RATE_LIMIT_GEMINI = "RATE_LIMIT_GEMINI"
    EMBEDDING_FAILED = "EMBEDDING_FAILED"
    VECTOR_SEARCH_FAILED = "VECTOR_SEARCH_FAILED"
    DATABASE_ERROR = "DATABASE_ERROR"
    LLM_ERROR = "LLM_ERROR"
    CONTEXT_OVERFLOW = "CONTEXT_OVERFLOW"

class ChatbotException(Exception):
    def __init__(self, message, error_code, user_message, details=None, recoverable=False):
        self.error_code = error_code
        self.user_message = user_message  # CRITICAL: User-friendly message
        self.recoverable = recoverable

class RateLimitError(ChatbotException):
    def __init__(self, provider: str):
        user_message = (
            f"The {provider.title()} API rate limit has been reached. "
            "This is a temporary issue. Please try again in a few minutes, "
            "or select text from the book and ask a question about it "
            "(selection mode works without embeddings)."
        )
        super().__init__(
            message=f"{provider} rate limit exceeded",
            error_code=ErrorCode.RATE_LIMIT_COHERE if provider == "cohere" else ErrorCode.RATE_LIMIT_GEMINI,
            user_message=user_message,
            recoverable=True
        )
```

### Rate Limit Detection Pattern
```python
def embed_text(self, text):
    try:
        response = self.client.embed(texts=[text], model=self.model, input_type="search_query")
        return response.embeddings[0]
    except Exception as e:
        error_str = str(e)

        # Check for rate limit (HTTP 429)
        if "429" in error_str or "rate limit" in error_str.lower() or "Too Many Requests" in error_str:
            raise RateLimitError(provider="cohere")

        # Check for auth errors
        if "401" in error_str or "403" in error_str:
            raise EmbeddingError(message="Authentication failed")

        raise EmbeddingError(message=f"Failed: {error_str}")
```

---

## Token Budget Management

```python
class ContextService:
    MAX_CONTEXT_TOKENS = 4000
    MAX_QUERY_TOKENS = 2000  # Leave room for response

    def assemble_context(self, query, retrieved_chunks, session_id, max_tokens=2000):
        current_tokens = self.count_tokens(query)
        selected_chunks = []

        # Add conversation history (last 2 exchanges)
        if session_id:
            for msg in session.messages[-4:]:
                msg_tokens = self.count_tokens(msg.content)
                if current_tokens + msg_tokens > max_tokens:
                    break
                current_tokens += msg_tokens

        # Add retrieved chunks until budget exhausted
        for chunk in retrieved_chunks:
            chunk_tokens = self.count_tokens(chunk.content)
            if current_tokens + chunk_tokens <= max_tokens:
                selected_chunks.append(chunk)
                current_tokens += chunk_tokens
            else:
                break

        return QueryContext(mode="retrieval", chunks=selected_chunks, total_tokens=current_tokens)
```

---

## SSE Streaming Implementation

### Backend Streaming
```python
async def generate_response_stream(self, context: QueryContext) -> AsyncGenerator[str, None]:
    response_stream = self.client.models.generate_content_stream(
        model=self.model_name,
        contents=full_prompt,
        config=types.GenerateContentConfig(temperature=0.3, max_output_tokens=1000)
    )

    for chunk in response_stream:
        if chunk.text:
            yield chunk.text
```

### Frontend SSE Handling
```javascript
const handleStreamingResponse = async (query, contextSelection) => {
    const response = await fetch(`${API_CONFIG.baseUrl}/api/chat/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'text/event-stream' },
        body: JSON.stringify({ query, session_id: sessionId, context_selection: contextSelection })
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let accumulatedText = '';

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');

        for (const line of lines) {
            if (line.startsWith('data: ')) {
                const data = line.slice(6);
                if (data === '[DONE]') break;

                const parsed = JSON.parse(data);
                if (parsed.type === 'content') {
                    accumulatedText += parsed.text;
                    setStreamingText(accumulatedText);  // Progressive update
                }
            }
        }
    }
};
```

---

## Environment Variables

```env
# Vector Database
QDRANT_URL=https://your-cluster.cloud.qdrant.io
QDRANT_API_KEY=your_qdrant_key

# Embeddings
COHERE_API_KEY=your_cohere_key

# LLM
GEMINI_API_KEY=your_gemini_key

# Metadata Store
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require

# Application
BOOK_BASE_URL=https://your-book-url.com/
CORS_ORIGINS=["http://localhost:3000", "https://your-domain.com"]
RATE_LIMIT_PER_MINUTE=30
RATE_LIMIT_PER_DAY=500
```

---

## HuggingFace Spaces Deployment

### README.md Metadata (Required)
```markdown
---
title: RAG Chatbot API
emoji: [emoji]
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---
```

### Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc g++ curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

### .gitignore for HF Spaces
```gitignore
.env
.env.*
!.env.example
__pycache__/
*.pyc
venv/
.venv/
```

---

# PART 2: DEBUG WORKFLOW

## Diagnostic Flow
```
1. Check API Response → 2. Check Retrieval Quality → 3. Check Prompt → 4. Check LLM Output
```

## Error Database

### Backend Errors

| Symptom | Cause | Solution |
|---------|-------|----------|
| `429 Too Many Requests` | Cohere rate limit | Use selection mode or upgrade tier |
| `Empty retrieval results` | Qdrant connection failed | Check QDRANT_URL and API key |
| `Hallucinated response` | Weak grounding prompt | Use ABSOLUTE RULES in prompt |
| `No citations in response` | LLM ignored format | Add fallback citation extraction |
| `Timeout on first request` | Cold start | Add loading indicator for first message |
| `CORS error` | Missing middleware | Add CORSMiddleware with correct origins |

### Frontend Errors

| Symptom | Cause | Solution |
|---------|-------|----------|
| `Failed to fetch` | CORS or network | Check CORS_ORIGINS matches frontend URL |
| Widget not visible | CSS positioning | Use `position: fixed` with high z-index |
| Streaming not working | SSE handling | Check Accept header and reader handling |
| Multiple widgets | React StrictMode | Add singleton guard with instanceCount |

## Health Check Endpoint
```python
@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "services": {
            "qdrant": await vector_store.ping(),
            "postgres": await metadata_service.ping(),
            "gemini": await agent_service.ping(),
            "cohere": await embedding_service.ping()
        }
    }
```

## Debug Logging Pattern
```python
logger.info(f"Query received: {query[:50]}...")
logger.info(f"Mode: {context.mode}, Chunks: {len(context.chunks)}")
logger.info(f"Highest similarity: {highest_score:.3f}")
logger.info(f"Out of scope: {is_out_of_scope}")
logger.info(f"Response length: {len(response_text)} chars")
```

---

# PART 3: VALIDATION WORKFLOW

## Quality Checklist

### Grounding Validation
- [ ] Response uses ONLY information from retrieved context
- [ ] No external knowledge or hallucinations
- [ ] "I don't know" response when context insufficient
- [ ] Citations present in `[Source: Title](URL)` format

### Response Quality
- [ ] Logical flow from context to answer
- [ ] Evidence integrated naturally (not copied verbatim)
- [ ] Clear conclusion that answers the question
- [ ] Explicit uncertainty when information missing

### Selection Mode Validation
- [ ] Only uses selected text (no vector search triggered)
- [ ] Responds with "not in selected text" when appropriate
- [ ] No external knowledge leakage

### Error Handling Validation
- [ ] Rate limit returns user-friendly message
- [ ] Graceful degradation when services unavailable
- [ ] Error codes present for debugging
- [ ] Recoverable flag indicates retry possibility

## Test Scenarios

### 1. In-Scope Question
```
Query: "What is inverse kinematics?"
Expected: Response with content from book + citations
Validate: similarity_score > 0.65, sources array not empty
```

### 2. Out-of-Scope Question
```
Query: "What is the weather today?"
Expected: "I couldn't find information about that in the book"
Validate: out_of_scope=true, similarity_score < 0.65
```

### 3. Selection Mode
```
Query: "Explain this" + selected_text="Inverse kinematics..."
Expected: Response using ONLY selected text
Validate: mode="selection", no vector search logged
```

### 4. Rate Limit Scenario
```
Trigger: Multiple rapid requests
Expected: User-friendly rate limit message with alternative suggestion
Validate: error_code="RATE_LIMIT_COHERE", recoverable=true
```

## Metrics to Track

| Metric | Target | Critical Threshold |
|--------|--------|-------------------|
| Response latency p95 | < 3s | > 10s |
| Retrieval accuracy | > 90% | < 70% |
| Grounding rate | 100% | < 95% |
| Citation presence | > 95% | < 80% |
| Error rate | < 1% | > 5% |

---

## Related Skills
- `chatkit-backend` - Alternative ChatKit approach
- `chatkit-frontend` - Frontend patterns
- `chatkit-debug` - General debugging

## References
- Cohere Embed v3.0 docs
- Qdrant Cloud docs
- Google Gemini API docs
- FastAPI SSE patterns
