# Frontend Architecture

## Tech Stack
- React 18 + TypeScript
- Vite for bundling
- react-i18next for i18n (Arabic + English)
- Recharts for data visualization
- Axios for API calls

## Route Structure

```
/                     → LessonList (select lesson)
/session/:lessonId    → StudentSession (adaptive tutoring)
/dashboard            → StudentDashboard (mastery + stats)
```

## Key Components

### LessonList
Displays available lessons. Clicking starts a learning session.

### StudentSession
Adaptive tutoring flow:
1. Calls `POST /tutor/session/step` each iteration
2. Renders EXPLAIN view (text + sources) or QUESTION view
3. On answer submission, sends response back in next step
4. Shows FINISHED state with link to dashboard

### QuestionCard
Displays question with type-specific input:
- MCQ: clickable option buttons
- Cloze/Open: textarea input
- Shows correctness feedback after submission
- Displays source citations

### MasteryHeatmap
Bar chart showing mastery percentage per concept.
Color-coded: green (>=80%), orange (>=60%), red (<40%).

### SourceCitation
Clickable source badges showing where content came from.

## i18n

Supports Arabic (RTL) and English (LTR).
Language toggle in navbar switches entire UI direction.

## State Management

Local component state with React hooks. No global state library needed for MVP.
API client handles auth token via localStorage.
