# RAG Design & Provenance Model

## Overview

EduMind's RAG system retrieves relevant content chunks and generates answers with clear source provenance — every fact traces back to its origin (text, audio, video, image).

## Data Model

### content_sources
Raw uploaded content with metadata:
- `type`: text, audio, video, image, table
- `origin`: book, slides, youtube, teacher_upload
- `language`, `url`, `file_path`

### content_chunks
Indexed content segments with embeddings:
- `source_id` → FK to content_sources
- `lesson_id`, `concept_id`, `skill_id` → knowledge hierarchy links
- `content`: the text segment
- `embedding`: pgvector VECTOR for similarity search
- `start_offset`, `end_offset`: page numbers or timecodes
- `metadata`: JSONB with translation_of, OCR_confidence, etc.

## Retrieval Process

1. **Query Embedding**: Student query → embedding vector
2. **Vector Search**: pgvector cosine similarity on `content_chunks.embedding`
3. **Filters**: lesson_id, language, concept_id
4. **Top-K**: Return top 8 most similar chunks
5. **Context Assembly**: Build context with source references
6. **LLM Generation**: Answer with citation instructions
7. **Source Parsing**: Extract structured source list

## Provenance Protocol

Every answer includes:
```json
{
  "answer": "The derivative of x² is 2x...",
  "sources": [
    {
      "source_id": "uuid",
      "source_name": "Calculus Lesson 1",
      "source_type": "text",
      "start_offset": 150,
      "end_offset": 300
    }
  ]
}
```

## Question Provenance

Questions store `source_chunk_ids` linking back to content chunks:
- Traces question → chunks → source file
- Enables content updates to cascade to affected questions
- Supports "where did this come from?" inquiries
