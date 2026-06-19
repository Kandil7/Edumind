# Assessment Engine

## Question Types

| Type | Generation Method | Grading |
|------|------------------|---------|
| Cloze (Fill-Mask) | Mask key words in text | Token match + semantic similarity |
| MCQ | LLM-generated from context | Option ID match |
| Open Text | Content-based prompts | Semantic similarity |
| VQA | LLaVA on diagrams (future) | LLM comparison |
| Table QA | TAPAS on tables (future) | Model-specific scoring |
| Oral | ASR transcription (future) | Text grading on transcript |

## Question Generation Flow

1. Retrieve content chunks for a concept
2. Extract candidate sentences
3. Generate question based on type:
   - **Cloze**: Mask key word, verify predictability
   - **MCQ**: Create stem + distractors from context
   - **Open Text**: Formulate from content
4. Store with `source_chunk_ids` for provenance

## Grading Logic

```python
def check_correctness(question, response):
    # Exact match
    if response == question.correct_answer:
        return True
    
    # MCQ: check option index
    if question.type == "mcq":
        return options[int(response)].text == correct_answer
    
    # Cloze: containment check
    if question.type == "cloze":
        return correct_answer in response
    
    # Fallback: token overlap >= 60%
    return len(response_tokens & answer_tokens) / len(answer_tokens) >= 0.6
```

## Feature Flags

- `ENABLE_VQA`: Enable image-based questions
- `ENABLE_TABLE_QA`: Enable table comprehension questions
- `ENABLE_ORAL`: Enable speech-based questions

Start with text-only assessment; enable modalities as models are integrated.
