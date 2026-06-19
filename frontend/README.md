# EduMind Frontend

React + TypeScript frontend for the EduMind adaptive learning platform.

## Setup

```bash
npm install
npm run dev
```

## Development

- **Dev server**: http://localhost:3000
- **API proxy**: Proxied to http://localhost:8000/api/v1
- **i18n**: Arabic (RTL) and English (LTR) with language toggle

## Build

```bash
npm run build    # Production build
npm run preview  # Preview production build
```

## Project Structure

```
src/
├── api/          # Axios API client with JWT auth
├── components/   # Reusable UI components
├── hooks/        # Custom React hooks
├── i18n/         # Internationalization config
├── pages/        # Page components
│   ├── StudentSession.tsx    # Adaptive tutoring flow
│   ├── StudentDashboard.tsx  # Mastery + stats
│   └── TeacherDashboard.tsx  # Content management
└── types/        # TypeScript interfaces
```

## Features

- **Student Flow**: Select lesson → adaptive session (explanations + questions) → dashboard
- **Teacher Flow**: Upload content, create lessons, view analytics
- **i18n**: Full Arabic/English support with RTL layout
- **Provenance**: Every answer shows source references
