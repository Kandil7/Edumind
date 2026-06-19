<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# ai_projects_batch2_arabic.html

Here’s a concise readout of the attached HTML: it contains **4 AI portfolio projects** — FrameAI, DesignForge, EduMind, and CodeGraph — each with architecture, Hugging Face task mappings, tech stack, resume metrics, timeline, and JD-alignment sections.[^1_1]

## Project list

- **FrameAI**: a video intelligence semantic search platform focused on frame extraction, ASR, captioning, multimodal indexing, temporal grounding, and visual QA.[^1_1]
- **DesignForge**: an AI-powered brand intelligence and generative design platform centered on brand-conditioned image generation, CLIP-based compliance scoring, and inpainting workflows.[^1_1]
- **EduMind**: an adaptive multimodal learning and assessment platform using knowledge tracing, VQA, table QA, fill-mask, ASR, and TTS for personalized education.[^1_1]
- **CodeGraph**: an AI code security and architecture intelligence platform using AST parsing, call/data-flow graphs, GNNs, and CI integration for vulnerability detection.[^1_1]


## Notable patterns

The document is clearly structured as a portfolio/positioning artifact rather than a normal HTML app, with sections for pipeline components, resume bullets, timelines, and hiring-match analysis for each project. It emphasizes production-grade AI system design, multimodal retrieval, evaluation, orchestration, and backend infrastructure.[^1_1]

## What it looks useful for

This file is well-suited for turning into a portfolio summary, extracting project bullets for a CV, or generating structured JSON/CSV from the project data. It also appears to be tailored for technical hiring, especially AI engineer, multimodal AI, MLOps, and applied NLP roles.[^1_1]

Would you like me to extract it into a clean table or convert it into JSON?

<div align="center">⁂</div>

[^1_1]: ai_projects_batch2_arabic.html


---

# yes

Done — I extracted the projects into both CSV and JSON formats. The generated files are available as `output/ai_projects_extracted.csv` and `output/ai_projects_extracted.json` .

The extracted set includes the four projects FrameAI, DesignForge, EduMind, and CodeGraph, preserving their subtitles, problem statements, tech stacks, and resume bullets .

Would you like me to also turn this into a Markdown table or a cleaned CV-ready summary?

---

# EduMind

**EduMind** is the adaptive multimodal learning and assessment platform in the portfolio, built around personalized education, knowledge tracing, and multimodal evaluation.[^3_1]

## What it does

EduMind targets the “one-size-fits-all” problem in education by adapting content difficulty to each learner using a knowledge tracing model. Its pipeline includes a profiler, content adapter, assessment engine, speech evaluator, gap detector, and tutor agent. It supports multimodal assessment through VQA, Table QA, Fill-Mask, ASR, and TTS, with multilingual output and RTL UI support.[^3_1]

## Key technical points

The project uses pyBKT and Deep Knowledge Tracing concepts to estimate mastery across concepts and route learning content dynamically. It combines TAPAS for table QA, LLaVA for visual QA, RoBERTa for cloze testing, and Whisper for oral evaluation, removing the need for manual question authoring. The stack also includes FastAPI, LangGraph, Celery, Redis, pgvector, PostgreSQL, TimescaleDB, React, i18n RTL, and Recharts.[^3_1]

## Resume-ready bullets

- Built adaptive learning engines using Bayesian Knowledge Tracing to model per-student concept mastery probability across 50 knowledge components and dynamically route content difficulty.[^3_1]
- Implemented multimodal assessment pipelines combining TAPAS Table QA, LLaVA Visual QA, RoBERTa Fill-Mask cloze testing, and Whisper oral evaluation, eliminating manual question authoring.[^3_1]
- Designed misconception detection by clustering wrong-answer patterns using Sentence Similarity to identify systematic gaps versus random errors and surface targeted remediation exercises.[^3_1]
- Integrated multilingual TTS and ASR feedback loops supporting 10 languages, enabling spoken explanations and oral answers with real-time transcription and evaluation.[^3_1]
- Built automatic cloze question generation using Fill-Mask models on lesson content to generate 100 assessment items per lesson with zero manual authoring.[^3_1]


## JD alignment

The document frames EduMind as a strong match for AI Engineer in EdTech, NLP Engineer, Applied AI Arabic NLP, and Full-Stack AI roles. Its strongest differentiators are adaptive learning, multimodal assessment, multilingual NLP, and RTL-aware product design.[^3_1]

Would you like a tighter one-paragraph version for a resume or LinkedIn project section?

<div align="center">⁂</div>

[^3_1]: ai_projects_batch2_arabic.html


---

# ابنيه ازاي

ابنيه على شكل **منصة تعليمية adaptive** فيها 5 طبقات أساسية: ingestion للمحتوى، student modeling، assessment generation، tutoring loop، وdashboard.[^4_1]

## المعمارية

- **Content ingestion**: تدخل الدروس والملفات والشرائح والـ transcripts وتفهرسها في pgvector/LlamaIndex، مع chunking بحسب الدرس والمفهوم.[^4_1]
- **Student profiler**: تبني ملفًا لكل طالب باستخدام pyBKT أو Deep Knowledge Tracing لتقدير mastery لكل concept وتحديثه بعد كل إجابة.[^4_1]
- **Assessment engine**: تولّد وتنفذ أسئلة VQA وTable QA وFill-Mask وASR وTTS حسب نوع المحتوى، بدل الاعتماد على أسئلة ثابتة.[^4_1]
- **Gap detector**: تجمع الأخطاء وتعمل clustering لأنماط الغلط لاكتشاف misconceptions وليس فقط scores خام.[^4_1]
- **Tutor agent**: يختار أنسب remedial content ويشرحها بصوت أو نص، مع دعم multilingual وRTL.[^4_1]


## التنفيذ المقترح

1. ابدأ بـ **MVP للـ content ingestion + QA**: ارفع الدروس، اعمل chunking، وابنِ RAG بسيط للشرح والبحث.[^4_1]
2. أضف **knowledge tracing**: خزّن attempts لكل student-skill pair وحدث probability للمastery بعد كل interaction.[^4_1]
3. فعّل **assessment generation**: استخدم Fill-Mask لتوليد cloze items، وTAPAS للـ tables، وLLaVA للصور/الرسوم، وWhisper للإجابات الصوتية.[^4_1]
4. ابنِ **remediation loop**: لو الطالب أخطأ في concept معين، اعرض شرحًا مختصرًا ثم سؤالًا أسهل ثم سؤال تحقق.[^4_1]
5. أخيرًا، أضف **dashboard** للطالب والمعلم مع progress charts وgap analytics.[^4_1]

## Stack عملي

- **Backend**: FastAPI + LangGraph + Celery + Redis.[^4_1]
- **Data**: PostgreSQL + TimescaleDB + pgvector.[^4_1]
- **Models**: pyBKT / DKT, TAPAS, LLaVA, RoBERTa Fill-Mask, Whisper, TTS.[^4_1]
- **Frontend**: React مع RTL/i18n وRecharts.[^4_1]


## ترتيب بناء سريع

- أسبوع 1-2: ingestion + RAG + basic quiz API.[^4_1]
- أسبوع 3-5: multimodal assessment engine.[^4_1]
- أسبوع 6-8: knowledge tracing + adaptive routing.[^4_1]
- أسبوع 9-10: ASR/TTS + multilingual support.[^4_1]
- أسبوع 11-12: dashboard + deploy.[^4_1]

لو تريد، أقدر أحول ده إلى **خطة هندسية أدق جدًا** فيها schema للجداول، APIs، وخريطة services.

<div align="center">⁂</div>

[^4_1]: ai_projects_batch2_arabic.html


---

# 📚

EduMind
Adaptive Multimodal Learning \& Assessment Platform
مدرس AI شخصي يتكيف مع مستوى كل طالب ويقيّم فهمه من النص والصوت والصور معاً
المشكلة الحقيقية: التعليم التقليدي one-size-fits-all يفشل مع 60% من الطلاب. المدرس الخصوصي حل ممتاز لكنه غير متاح للجميع. EduMind يبني مسار تعليمي شخصي لكل طالب، يقيّمه بطرق متعددة (نص + صوت + صور)، ويكتشف gaps في الفهم قبل ما الطالب يعرف إن عنده مشكلة.
ArchitectureHF TasksTech StackResume MetricsTimelineJD Alignment
Agent Pipeline
Profiler
يبني student knowledge model من أول تفاعل
Content Adapter
يعدل مستوى الشرح والأمثلة حسب مستوى الطالب
Assessment Engine
VQA + Table QA + Fill-Mask = أسئلة متعددة الأنواع
Speech Evaluator
ASR يسمع إجابة الطالب الشفهية ويقيّمها
Gap Detector
يحلل pattern الأخطاء ويكتشف الـ misconceptions
Tutor Agent
يشرح السبب ويقترح تمارين targeted للـ gap المحدد
ما يميز المشروع
Knowledge tracing model — Bayesian Knowledge Tracing يتتبع احتمالية إتقان كل concept لكل طالب عبر الزمن، مش بس "أجاب صح أو غلط"
Multimodal assessment — سؤال تعريف نصي + سؤال على جدول بيانات + سؤال على صورة diagram + إجابة شفهية = تقييم شامل حقيقي
Fill-Mask for cloze testing — توليد أسئلة cloze تلقائياً من محتوى الدرس بدون manual authoring
Multilingual support — التقييم والشرح بلغة الطالب، ترجمة تلقائية للمحتوى الأجنبي HF Tasks الأساسية
Visual Question AnsweringTable Question AnsweringFill-MaskAutomatic Speech RecognitionText-to-SpeechTranslationText Generation
HF Tasks الثانوية
SummarizationQuestion AnsweringSentence SimilarityZero-Shot ClassificationImage-to-Text
Table Question Answering و Fill-Mask من أندر الـ tasks في أي portfolio — مش ناس كتير تعرف إنهم موجودين حتى. استخدامهم في educational assessment context هو application حقيقي ومبتكر مش مجرد demo.NLP \& Assessment Models
TAPAS (Table QA)LLaVA (VQA)RoBERTa Fill-MaskWhisperTTS-1
Knowledge Tracing
pyBKTDeep Knowledge TracingPostgreSQLTimescaleDB
Backend \& Orchestration
FastAPILangGraphCeleryRedispgvector
Frontend
Reacti18n + RTLRecharts progressWeb Speech API 7
HF task types
BKT
Knowledge tracing model
4
Assessment modalities
10+
Languages supported
Built adaptive learning engine using Bayesian Knowledge Tracing (pyBKT) to model per-student concept mastery probability across 50+ knowledge components; dynamically routes content difficulty
Implemented multimodal assessment pipeline combining TAPAS Table QA, LLaVA Visual QA, RoBERTa Fill-Mask cloze testing, and Whisper oral evaluation — eliminating manual question authoring
Designed misconception detection system clustering wrong-answer patterns using Sentence Similarity to identify systematic gaps vs. random errors; surfaces targeted remediation exercises
Integrated multilingual TTS + ASR feedback loop supporting 10+ languages; students receive spoken explanations and can answer orally with real-time transcription and evaluation
Built automatic cloze question generation using Fill-Mask models on lesson content; generates 100+ assessment items per lesson with zero manual authoring
Content ingestion + RAG
Weeks 1–2
LlamaIndex document loader، pgvector، lesson chunking، basic QA
Assessment engine (VQA + TableQA + Fill-Mask)
Weeks 3–5
TAPAS، LLaVA، RoBERTa cloze generation، answer evaluation
Knowledge tracing + adaptation
Weeks 6–8
pyBKT model، student profile DB، content difficulty routing، gap detection
ASR + TTS + multilingual
Weeks 9–10
Whisper oral eval، TTS explanations، Translation، RTL UI support
Dashboard + deploy
Weeks 11–12
Student progress charts، teacher dashboard، Docker، public demo بمادة حقيقية AI Engineer — EdTech
Adaptive learning, NLP assessment, multimodal AI, personalization
Direct match — full EdTech AI stack
NLP Engineer
QA systems, text generation, multilingual NLP, Fill-Mask
Strong match — 7 NLP task types
Applied AI — Arabic NLP
Arabic language models, RTL, multilingual, translation
Unique differentiator in MENA market
Full-Stack → AI pivot
React, FastAPI, PostgreSQL, Docker
Strong SWE foundations + AI layer

ده بروجيكت مكتمل ومكتوب ممتاز فعلًا. أقدر أساعدك في تحويله لـ blueprint تنفيذي (schemas + services + APIs) أو تحسين الpitch. من كلامك، واضح إنك حابب تبنيه فعلًا، فهامشي على ده.

## 1. Core components كـ خدمات

خلّيه 6 خدمات واضحة، كل واحدة موديل + endpoints:

- **Content Service (RAG)**
    - إدخال الدروس (PDF/HTML/Slides) → chunking → pgvector مع `lesson_id`, `concept_id`.[^5_1]
    - Endpoints:
        - `POST /lessons` رفع درس.
        - `POST /lessons/{id}/index` تشغيل chunking + embedding.
        - `POST /lessons/search` سؤال عام يرجّع مقطع + سياق.
- **Student Profiler (Knowledge Tracing)**
    - جدول `students`, `skills`, `student_skill_state` فيه $p(mastery)$ لكل concept.[^5_1]
    - يستخدم pyBKT/ DKT لتحديث الاحتمال بعد كل محاولة.[^5_1]
    - Endpoints:
        - `POST /attempts` (student_id, skill_id, correct, meta…) → يرجّع mastery الجديد.
        - `GET /students/{id}/profile` يرجّع خريطة mastery.
- **Assessment Engine**
    - يجمع TAPAS, LLaVA, RoBERTa Fill-Mask, Whisper، ويقرر نوع السؤال حسب الـcontent type.[^5_1]
    - Endpoints:
        - `POST /assessments/generate` (lesson_id, skill_ids, difficulty) → list أسئلة (متعددة modalities).
        - `POST /assessments/grade` (question + answer) → score + skill_id.[^5_1]
- **Speech Evaluator**
    - واجهة حول Whisper + TTS-1.[^5_1]
    - Endpoints:
        - `POST /speech/tts` نص → audio.
        - `POST /speech/asr` audio → transcript + تقييم pronunciation (optional).
- **Gap Detector**
    - consumer للـattempts من queue (Celery/Redis)، يعمل clustering للأخطاء باستخدام sentence similarity.[^5_1]
    - يخرج `misconception_id` وارتباطها بـskills.
    - Endpoints:
        - `GET /students/{id}/gaps`
        - `GET /skills/{id}/misconceptions`
- **Tutor Agent**
    - orchestrator مبني على LangGraph: يأخذ (student_profile, gaps, lesson chunks) ويكوّن حوار + تمارين.[^5_1]
    - Endpoints:
        - `POST /tutor/next-step` يرجع: شرح + سؤال + modality مقترحة.

كلهم خلف **FastAPI** واحد أو micro-services حسب حبك للتفكيك.[^5_1]

## 2. Data model (Postgres + Timescale + pgvector)

جداول أساسية:

- `lessons(id, title, topic, grade, language, created_at...)`
- `concepts(id, lesson_id, name, description)`
- `lesson_chunks(id, lesson_id, concept_id, content, embedding VECTOR, metadata JSONB)`.[^5_1]
- `students(id, name, language, level, meta)`
- `skills(id, concept_id, name, description)`
- `student_skill_state(student_id, skill_id, p_mastery, attempts_count, last_updated)`.[^5_1]
- `attempts(id, student_id, skill_id, question_id, correct, response, modality, created_at)` → جدوله في TimescaleDB لسهولة time-series.[^5_1]
- `misconceptions(id, skill_id, centroid_embedding, description)`
- `misconception_instances(id, student_id, misconception_id, first_seen_at, last_seen_at)`.[^5_1]

pgvector تستخدمه في:

- similarity search على `lesson_chunks`.
- clustering wrong answers في Gap Detector.[^5_1]


## 3. Model wiring (MVP realistic)

ابدأ بانتقاء موديلات عملية بدل ideal فقط:

- **RAG + Text QA**: LLM واحد (مثلاً Arabiyah/Command-R + embeddings mE5) يكفي كبداية، بدون TAPAS/LLaVA فورًا.
- **BKT**: pyBKT standalone service، تخزين parameters في JSON أو جداول.[^5_1]
- **Assessment**:
    - Cloze: RoBERTa-base أو AraBERT مع task Fill-Mask على النص الإنجليزي/العربي.[^5_1]
    - Image/diagram: لاحقًا LLaVA جاهز hosted (HF Inference/Replicate).
    - Table QA: TAPAS ممكن تأجيله للـphase 2 لو الscope ضاغط.[^5_1]
- **ASR/TTS**: Whisper-small/medium + TTS-1 (أو أي TTS عربي معقول).[^5_1]

LangGraph:

- graph nodes: `Select_skill`, `Select_content`, `Generate_question`, `Grade`, `Update_BKT`, `Decide_next_action`.
- conditions مبنية على `p_mastery`, عدد المحاولات الفاشلة, وجود misconception.


## 4. Execution plan أسبوعي (عملي)

متوافق تقريبًا مع الـtimeline اللي كتبته لكن من زاوية تنفيذ:

1. **أسبوع 1–2: Content + RAG + basic quiz**[^5_1]
    - API لرفع الدروس + chunking + pgvector.
    - Endpoint `ask-lesson` + simple MCQ generator من LLM على نفس النص.
2. **أسبوع 3–4: Assessment Engine v1**[^5_1]
    - Cloze generation (Fill-Mask) + grading.
    - Table QA placeholder (just convert table to text) لحين TAPAS.
    - Frontend بسيط لعرض سؤال واحد لكل مرة مع RTL.
3. **أسبوع 5–6: Knowledge Tracing (pyBKT)**[^5_1]
    - mapping concepts → skills.
    - حساب p_mastery بعد كل attempt + API تعرض heatmap profile.
4. **أسبوع 7–8: Adaptive routing + Gap Detector v1**[^5_1]
    - rules: لو p_mastery < threshold → أسئلة أسهل + شروحات.
    - clustering مبدئي باستعمال embeddings + k-means على wrong answers.
5. **أسبوع 9–10: ASR/TTS + Multilingual**[^5_1]
    - endpoints للصوت + دعم UI للصوت.
    - إضافة translation step لو محتوى أجنبي.
6. **أسبوع 11–12: Dashboard + polish + Docker demo**[^5_1]
    - Recharts لعرض progress.
    - roles: student/teacher.
    - docker-compose لكل الخدمات + demo على مادة حقيقية (مثلاً رياضيات ثانوي/فيزياء).

## 5. Stack details aligned مع أسلوبك

- **Backend**: FastAPI, LangGraph, Celery, Redis, pgvector extension, Timescale على نفس Postgres cluster.[^5_1]
- **Frontend**: React + i18n (react-i18next) + RTL theme (MUI أو Tailwind)، Web Speech API لintegration الصوتي في المتصفح.[^5_1]
- **Infra**: Docker, ملحقة لاحقًا بـ Modal/RunPod لو هتطلع inference خارجياً زي ما عامل في DesignForge.[^5_1]


## 6. هدف Demo واضح

أقترح scope demo واحد واضح:

- مادة واحدة (مثلاً “مقدمة في التفاضل”)، حوالي 5–10 دروس، وكل درس له 3–5 concepts.
- طالب يدخل، يختار الدرس، يعمل 10–15 سؤال متنوع (نص + جدول + صورة + صوت)، يشوف في الآخر dashboard mastery + gaps + توصيات.

ده يبقى story ممتازة في interview + case study في Athar/Baligh.

ما أكثر حاجة حابب تبدأ بها فعلًا: الـBKT stack ولا assessment engine ولا RAG layer؟

<div align="center">⁂</div>

[^5_1]: ai_projects_batch2_arabic.html


---

# عاوزه يحدد مصدر المعلومات سواء قطع نصيه او صوتيه او اي مصدر بحيث تكون فيه مرجعيه في نظام RAG

الفكرة الصح هنا إن كل إجابة أو سؤال يطلع من EduMind يكون عنده **سلسلة نسب (provenance)** واضحة: جاي منين بالضبط، أي فقرة، أي ملف، أي تسجيل صوتي.[^6_1]

## 1. نموذج المرجعية في RAG

خلّي كل chunk عندك يحمل ميتاداتا غنية، مثل:

- `source_type`: `text`, `audio_transcript`, `video_transcript`, `image_caption`, `table`, `teacher_note`.[^6_1]
- `source_id`: id ثابت للدرس/الملف الأصلي (مثلاً `lesson_123`, `audio_45`).[^6_1]
- `source_name`: اسم الدرس أو اسم الملف (مثلاً "مقدمة في التفاضل – درس 1").[^6_1]
- `origin`: `book`, `slide`, `youtube`, `teacher_upload` … إلخ.
- `start_offset`, `end_offset`:
    - في النص: character offsets أو رقم الصفحة/الفقرة.
    - في الصوت/الفيديو: timecodes بالثواني (مثلاً 120–150 ثانية).[^6_1]
- `concept_id`, `skill_id`: تربط chunk بالكونسبت/skill في BKT.[^6_1]
- `language`, `translation_of`: لو chunk ناتج من ترجمة، خزن id chunk الأصلي.

هذي الميتاداتا تتحفظ في جدول `lesson_chunks` (أو جدول شبيه) مع عمود `embedding` (pgvector).[^6_1]

## 2. كيف retrieval يحافظ على المرجعية

عند الاسترجاع:

1. نموذج embeddings يرجّع top-k chunks.
2. لكل chunk، تبقي الميتاداتا كما هي وتبعثها للـLLM.
3. في الـprompt، تلزم الـLLM يرجّع **قائمة بالمصادر** مع كل إجابة:
    - مثال تنسيق:
        - `sources: [{source_id, source_name, source_type, locator}]`
    - `locator`: صفحة/فقرة/توقيت صوت.

في الـfrontend، تقدر:

- تعرض "جملة مقتبسة" مع زر "اذهب للمصدر" يفتح الدرس في المكان الصحيح.
- لو مصدر صوتي، تستعمل `start_offset` لـseek في الـaudio player.


## 3. الربط بالأسئلة والتقييم

لكل سؤال يتكوّن في Assessment Engine، خزن:

- في جدول `questions`:
    - `id`
    - `stem` (نص السؤال)
    - `modality` (نص/صورة/جدول/صوت)
    - `source_chunk_ids` (list)[^6_1]
    - `source_type`, `source_id`, `start_offset`, `end_offset` (أو مجرد تخزينها في chunk وربط السؤال بها عبر join).

بهذا:

- لو طالب اشتكى من سؤال، تقدر تعرف من أي فقرة أو أي جزء من الفيديو طلع.
- لو عدّلت المحتوى الأصلي (مثلاً دكتور صحح سطر في السلايد)، تقدر ترجع كل الأسئلة المبنية عليه وتعيد توليدها.


## 4. مثال مخطط جداول مبسط

- `content_sources`
    - `id` (uuid)
    - `type` (`text`, `audio`, `video`, `image`, `table`)
    - `origin` (`book`, `ppt`, `youtube`, ...)
    - `title`, `author`, `url`, `file_path`, `created_at`
- `content_chunks`
    - `id`
    - `source_id` → FK لـ`content_sources.id`
    - `concept_id` → FK
    - `skill_id` → FK
    - `content` (النص/الوصف)
    - `embedding` (VECTOR)
    - `start_offset`, `end_offset` (صفحة/ثواني/indices)
    - `metadata` (JSONB: language, translation_of, extra)
- `questions`
    - `id`
    - `type` (`cloze`, `mcq`, `vqa`, `table_qa`, `oral`)
    - `skill_id`
    - `stem`, `options`, `answer`
    - `source_chunk_ids` (Array/JSONB)

بهذا، علاقة:

- سؤال ↔ skills ↔ chunks ↔ source file/lesson.


## 5. بروتوكول الLLM للمرجعية

في الـTutor Agent / RAG QA prompt، أضف تعليمات مثل:

> عند الإجابة:
> - لا تستخدم إلا المعلومات الموجودة في السياق.
> - لكل جملة تقريبًا، أرفق `[#source_i]` حيث `source_i` هو index لقطعة في قائمة السياق.
> - في النهاية أرجع قائمة `sources` فيها: `source_id`, `source_name`, `source_type`, `locator`.

ثم في backend:

- تحوّل هذه الـ`#source_i` إلى أزرار قابلة للنقر في UI، مع metadata الخارجي.

بهذه الطريقة يكون عندك مرجعية واضحة لأي تجلٍ للمعلومة، سواء كان قادم من نص أو صوت أو صورة.

هل تحب نرسم schema SQL حقيقي للجداول (`content_sources`, `content_chunks`, `questions`) مع أنواع الأعمدة وindexes (خصوصًا pgvector + البحث بالـsource_id والـconcept_id)؟

<div align="center">⁂</div>

[^6_1]: ai_projects_batch2_arabic.html


---

# PRD بالتفصيل

PRD مناسب لـ EduMind عندك هو مستند يترجم كل اللي فوق إلى منتج واضح: من هم المستخدمون، ما السيناريوهات، ما الميزات، ما البيانات، وما القيود. أكتب لك نسخة تفصيلية لكن مركّزة على أول نسخة (MVP) مع الإشارة للـRAG والمرجعية اللي طلبتها.[^7_1]

## 1. مقدمة المنتج

EduMind هو **نظام تعلم تكيفي متعدد الوسائط** يشتغل كـ"مدرس AI شخصي" يحلل أداء الطالب على دروس حقيقية ويكيّف المحتوى والأسئلة حسب مستواه، مع مرجعية واضحة لكل معلومة إلى مصدرها الأصلي (نص، صوت، فيديو، صورة، جدول).[^7_1]

### أهداف الإصدار الأول (MVP)

- توفير مسار تعلم شخصي لمادة واحدة (مثلاً رياضيات ثانوي)، مع 5–10 دروس، لكل درس مفاهيم (concepts) محددة.[^7_1]
- دعم تقييم متعدد الوسائط: نص + جدول + صورة + إجابة صوتية.[^7_1]
- تتبع mastery لكل concept لكل طالب عبر الزمن (Bayesian Knowledge Tracing).[^7_1]
- نظام RAG بمراجع واضحة لكل إجابة/سؤال (source, offsets, timecodes).[^7_1]


### المستخدمون المستهدفون

- طلاب ثانوي/جامعة في مادة واحدة كبداية.
- معلم واحد أو أكثر يشرف على المادة ويراجع المحتوى والتقييم.
- لاحقًا: مشرف/أدمن منصة.


## 2. المستخدمون وPersonas

### Persona 1: طالب

- يريد فهم درس معين (مثلاً "مشتقات") حسب مستواه.
- يتفاعل مع أسئلة نصية وبصرية وصوتية.
- يحب أن يعرف "من أين أتى هذا الشرح/المعلومة؟" (مرجعية) ليعود للدرس/الكتاب.


### Persona 2: معلم

- يرفع محتوى دروس من ملفات (PDF, slides, نصوص، فيديو مسجل).
- يريد رؤية تحليلات gaps والمفاهيم الصعبة على الطلاب.
- يحتاج لإمكانية مراجعة الأسئلة والمحتوى المعتمد.


## 3. نطاق الإصدار الأول (In Scope / Out of Scope)

### In Scope

- مادة واحدة، مسار تعلم واحد.
- دعم لغتين على الأقل (عربي + إنجليزي) للمحتوى والواجهة.[^7_1]
- RAG layer بدعم:
    - نصوص (كتب، مذكرات، slides).
    - Transcripts لصوت/فيديو (Whisper).[^7_1]
- Assessment modalities:
    - نصية (MCQ, Cloze).
    - جدول (Table QA).[^7_1]
    - صورة بسيطة (شكل/رسم – VQA).[^7_1]
    - سؤال وإجابة صوتية (ASR/TTS).[^7_1]
- Knowledge tracing باستخدام pyBKT.[^7_1]
- Dashboard مبسط للطالب والمعلم.


### Out of Scope (لاحقًا)

- دعم مواد متعددة بمخططات مختلفة.
- Authoring manual معقد للأسئلة (نبدأ بتوليد تلقائي + بعض التعديل البسيط).
- تكامل كامل مع LMS خارجي (Moodle, Classroom…).
- Gamification متقدمة (نكتفي بprogress bars).


## 4. سيناريوهات الاستخدام الأساسية (User Flows)

### Flow 1: رفع محتوى درس (المعلم)

1. المعلم يسجل الدخول.
2. يختار "إضافة درس جديد".
3. يرفع ملفات: PDF / Slides / فيديو / Audio.
4. يحدد:
    - عنوان الدرس، المستوى، اللغة.
    - concepts داخل هذا الدرس (إدخال يدوي أو استيراد من template).
5. النظام يعمل:
    - استخراج نص (OCR لو احتج، بعدين).
    - chunking حسب الفقرات والمفاهيم.
    - embeddings + تخزين في pgvector مع metadata (type, source_id, offsets, concept_id, language).[^7_1]
6. المعلم يراجع preview للـchunks ويمكنه تعديل/إزالة بعض القطع.

### Flow 2: جلسة تعلم للطالب

1. الطالب يسجل الدخول، يختار مادة ودرس.
2. النظام يسترجع profile الطالب (p_mastery لكل concept مرتبط بهذا الدرس).[^7_1]
3. Tutor Agent يقرر:
    - هل يبدأ بشرح مبسط (RAG + LLM) أم يدخل مباشرة في تقييم؟
4. في كل خطوة:
    - يعرض سؤال (نصي/جدول/صورة/شفهي).
    - الطالب يجاوب: كتابة أو صوت.
    - Assessment Engine يقيّم الإجابة ويحدد `correct` + المهارة (skill_id).[^7_1]
    - Student Profiler (BKT) يحدّث p_mastery.[^7_1]
    - Gap Detector يجمع البيانات في الخلفية ويحدّد أنماط الأخطاء لاحقًا.[^7_1]
5. بعد عدة أسئلة، النظام:
    - يقدّم شرح مخصص للمفاهيم التي mastery فيها منخفض.
    - يرفق لكل فقرة شرح "مصادر" واضحة (مثلاً: من كتاب X، صفحة 10، أو فيديو Y من الدقيقة 2:00–2:30).

### Flow 3: مراجعة التقدم (Dashboard)

1. الطالب يفتح صفحة "التقدم":
    - خريطة مفاهيم (concept map) عليها ألوان mastery.
    - قائمة gaps (مثلاً: "مشكلة في فهم تعريف المشتقة").
2. المعلم يفتح Dashboard المعلم:
    - قائمة الطلاب مع مستوى التقدم.
    - أكثر المفاهيم التي بها misconceptions عبر الصف.[^7_1]
    - إمكانية تصفية حسب concept أو درس.

## 5. الميزات التفصيلية

### 5.1 Content \& RAG مع المرجعية

- إدخال مصادر:
    - أنواع: `text`, `audio`, `video`, `image`, `table`.
    - كل مصدر له metadata: عنوان، origin (كتاب، يوتيوب، محاضرة)، لغة.
- Chunking:
    - Text: تقسيم حسب الفقرات والعناوين، مع ربط كل chunk بـconcept/skill إن أمكن.[^7_1]
    - Audio/Video: Whisper → transcript؛ تقطيع transcript إلى segments مع timecodes.
    - Image: caption أو alt-text بالإضافة إلى وصف يدوي من المعلم إن لزم.
    - Table: تمثيل كـstructure (CSV/JSON) + text flattening لـTAPAS.[^7_1]
- تخزين:
    - لكل chunk:
        - `source_id`, `source_type`, `origin`, `start_offset`, `end_offset`.
        - `concept_id`, `skill_id`.
        - `language`, `translation_of` لو مترجم.
        - `embedding`.
- Retrieval:
    - البحث حسب سؤال الطالب:
        - vector search في `content_chunks`.
        - filter بالـlanguage والدرس والمستوى إن لزم.
    - إخراج:
        - context + قائمة sources مع locators واضحة.
    - الـLLM ملزم بإرجاع references ضمن الإجابة بالتنسيق المتفق عليه.


### 5.2 Assessment Engine

- أنواع أسئلة:
    - Cloze (Fill-Mask) من نص الدرس.[^7_1]
    - MCQ تُبنى من cloze أو من Q/A بسيطة.
    - Table QA باستخدام TAPAS من جداول مرتبطة بالدرس.[^7_1]
    - VQA على diagrams (LLaVA).[^7_1]
    - Oral questions/answers:
        - السؤال يظهر نصًا وصوتًا (TTS).[^7_1]
        - إجابة الطالب تُسجّل وتُمرّر إلى Whisper ثم تُقيّم.[^7_1]
- خصائص:
    - كل سؤال مرتبط بـ:
        - `skill_id`, `concept_id`.
        - `source_chunk_ids` (واحد أو أكثر).
    - تقييم:
        - نص: string similarity/LLM rubric.
        - Cloze: exact أو token-level.
        - Table/VQA: LLM أو model-specific scoring.
        - Oral: transcription + نفس منطق scoring النصي.


### 5.3 Student Profiler (Knowledge Tracing)

- نموذج:
    - pyBKT لكل skill، يخزن parameters في DB.[^7_1]
    - p_mastery محدث بعد كل attempt.[^7_1]
- واجهات:
    - استعلام profile طالب: يعيد p_mastery لكل skill.
    - تحديث بعد attempt: يأخذ (student_id, skill_id, correct) ويعيد p_new.


### 5.4 Gap Detector

- clustering للخطأ:
    - يأخذ نص إجابات خاطئة + سياق السؤال → embeddings.
    - يعمل clustering per skill → misconceptions.[^7_1]
- يربط كل طلب gap بمفهوم + وصف بسيط (LLM-generated).
- يظهر للمعلم:
    - "أكثر خطأ شائع في مهارة X هو كذا…".


### 5.5 Tutor Agent

- orchestrator بالـLangGraph:[^7_1]
    - خطوة اختيار skill الذي نركز عليه (low mastery).
    - اختيار المحتوى (chunks مناسبة).
    - اختيار نوع السؤال (نص/جدول/صورة/شفهي) حسب المرحلة.
    - بعد محاولة أو اثنتين فاشلة:
        - تقديم explanation + مثال.
        - ثم سؤال تحقق أسهل.


## 6. متطلبات غير وظيفية

- اللغات: دعم واجهة عربية (RTL) + إنجليزية؛ دعم محتوى 10+ لغات على مستوى ASR/TTS/ترجمة في backend.[^7_1]
- الأداء:
    - استجابة أسئلة الطالب (generation + grading) < 3–5 ثوانٍ في المتوسط.
    - indexing أولي للدرس ممكن يستغرق حتى دقائق لكن يتم في الخلفية.
- الأمن والخصوصية:
    - تخزين بيانات الطلاب مشفرة في rest (DB) وعلى النقل (HTTPS).
    - إمكانية حذف حساب طالب بالكامل.
- التوسع:
    - دعم إضافة مواد ومحتويات جديدة بدون إعادة نشر الكود (config-driven).


## 7. قياس النجاح (KPIs)

- نسبة الأسئلة ذات المرجع الواضح (كل إجابة تحتوي على sources قابلة للنقر) ≥ 95%.
- تحسن p_mastery لمفاهيم مختارة بعد جلسات تدريبية.
- معدل إكمال جلسة تعلم (10–15 سؤال) per student.
- Feedback من المعلم:
    - جودة تحليل gaps.
    - نسبة الأسئلة “غير مناسبة” التي تحتاج تعديل يدوي.

***

هذا PRD يعطيك skeleton واضح من منظور product وties مباشرة مع المعمارية اللي اتكلمنا عنها (RAG + BKT + multimodal assessment + provenance).[^7_1]

هل تحب الخطوة الجاية تكون: تفصيل الـSQL schema + API contracts (Swagger-style)، ولا نضبط نسخة PRD إنجليزي جاهزة للـhiring / pitch deck؟

<div align="center">⁂</div>

[^7_1]: ai_projects_batch2_arabic.html


---

# full implementation plan in details

Here is a concrete, end‑to‑end implementation plan for EduMind, from repo layout to deployment, aligned with the architecture and timeline you already sketched.[^8_1]

***

## 1. High‑level phases and milestones

We structure implementation into five main phases, each with clear milestones. Durations roughly follow the 12‑week timeline you wrote (can compress/expand).[^8_1]

1. **Foundation \& Content/RAG (Weeks 1–2)**
    - Repos, infra, base schemas, auth, content ingestion, chunking, pgvector, basic RAG QA.[^8_1]
2. **Assessment Engine (Weeks 3–5)**
    - Question generation (cloze, MCQ, simple VQA/Table QA), grading, question store, linking to content provenance.[^8_1]
3. **Knowledge Tracing \& Adaptation (Weeks 6–8)**
    - pyBKT service, student_skill_state, update pipeline, rules‑based adaptive routing, gap detector v1.[^8_1]
4. **Multimodal (ASR/TTS) \& Multilingual (Weeks 9–10)**
    - Whisper + TTS integration, audio pipelines, translation, RTL/i18n UI.[^8_1]
5. **Dashboards, polish, deployment \& demo (Weeks 11–12)**
    - Student/teacher dashboards, analytics, Docker, demo with real course.[^8_1]

***

## 2. Repository \& service architecture

Use a mono‑repo with clearly separated modules, but keep it small enough for rapid iteration.[^8_1]

### 2.1 Repo structure

```text
edumind/
  backend/
    app/
      api/
        v1/
          content.py
          questions.py
          students.py
          tracing.py
          tutor.py
          auth.py
      core/
        config.py
        db.py
        logging.py
      models/        # ORM models
      services/
        rag/
        assessment/
        tracing/
        gap_detector/
        tutor/
        speech/
      workers/
        celery_app.py
        tasks/
  frontend/
    src/
      pages/
      components/
      api/
      hooks/
      i18n/
  infra/
    docker/
      backend.Dockerfile
      frontend.Dockerfile
      docker-compose.yml
    migrations/
      alembic/
  notebooks/
    experiments_bkt.ipynb
    experiments_cloze.ipynb
```

Backend: FastAPI + SQLAlchemy/psycopg, Celery + Redis, pgvector + TimescaleDB on Postgres.[^8_1]
Frontend: React + MUI/Tailwind + react‑i18next for i18n + RTL.[^8_1]

***

## 3. Data model \& databases

### 3.1 Core tables

Design them so provenance and adaptation are first‑class.[^8_1]

- `content_sources`
    - `id` (UUID, PK)
    - `type` (`text`, `audio`, `video`, `image`, `table`)
    - `origin` (`book`, `slides`, `youtube`, `teacher_upload`, …)
    - `title`, `description`
    - `language`
    - `url` (for remote) / `file_path` (for uploaded)
    - `created_by`, `created_at`
- `lessons`
    - `id` (PK)
    - `title`, `subject`, `grade_level`
    - `language`
    - `description`
    - `is_active`
- `concepts`
    - `id` (PK)
    - `lesson_id` (FK)
    - `name`, `description`
    - `difficulty_level` (enum / int)
- `skills`
    - `id` (PK)
    - `concept_id` (FK)
    - `name`
    - `description`
- `content_chunks` (pgvector + Timescale if you want time dimension; otherwise Postgres table)[^8_1]
    - `id` (PK)
    - `source_id` (FK → content_sources)
    - `lesson_id` (FK)
    - `concept_id` (FK)
    - `skill_id` (FK, nullable)
    - `language`
    - `content` (TEXT)
    - `embedding` (VECTOR)
    - `source_type` (duplicated from source for quick filter)
    - `start_offset`, `end_offset` (page/char for text, seconds for audio/video)
    - `metadata` (JSONB: translation_of, OCR_confidence, etc.)
    - Index:
        - `USING ivfflat (embedding vector_cosine_ops)`
        - `BTREE` on `(lesson_id, concept_id, skill_id)`
- `students`
    - `id` (PK)
    - `name`
    - `email`
    - `preferred_language`
    - `level` (e.g. `beginner|intermediate|advanced`)
    - `created_at`
- `student_skill_state` (candidate for Timescale hypertable keyed by student_id, skill_id)[^8_1]
    - `student_id` (FK)
    - `skill_id` (FK)
    - `p_mastery` (float)
    - `num_attempts`
    - `last_updated`
    - `initialized` (bool)
- `questions`
    - `id` (PK)
    - `type` (`cloze`, `mcq`, `open_text`, `vqa`, `table_qa`, `oral`)
    - `lesson_id`, `concept_id`, `skill_id`
    - `stem` (TEXT)
    - `options` (JSONB)
    - `correct_answer` (TEXT/JSON)
    - `difficulty`
    - `source_chunk_ids` (JSONB array of content_chunk ids)  ← provenance link.[^8_1]
    - `generator_metadata` (JSONB: model, params, etc.)
- `attempts` (Timescale hypertable by time)[^8_1]
    - `id` (PK)
    - `student_id`
    - `question_id`
    - `skill_id`
    - `correct` (bool)
    - `response_text`
    - `response_audio_path`
    - `modality` (`text`, `oral`, …)
    - `created_at`
    - `metadata` (JSONB: latency, hints used, etc.)
- `misconceptions`
    - `id` (PK)
    - `skill_id`
    - `description`
    - `centroid_embedding` (VECTOR)
    - `metadata`
- `misconception_instances`
    - `id`
    - `student_id`
    - `misconception_id`
    - `first_seen_at`
    - `last_seen_at`
    - `num_occurrences`

***

## 4. Phase 1 – Foundation \& Content/RAG (Weeks 1–2)

### 4.1 Infra \& scaffolding

- Initialize repo, basic CI (lint, test).
- Create Docker images:
    - Postgres with pgvector + Timescale extensions.
    - Redis for Celery.
    - Backend image with FastAPI, Uvicorn, Celery worker.
- Add Alembic migrations for base tables above.[^8_1]


### 4.2 Authentication \& roles

- Simple JWT auth (FastAPI + fastapi-users or custom) with roles:
    - `student`, `teacher`, `admin`.


### 4.3 Content ingestion APIs

Implement endpoints:

- `POST /v1/content-sources`
    - body: `type`, `origin`, `title`, `language`, file upload or URL.
    - action: store metadata, store file, return `source_id`.
- `POST /v1/lessons`
    - body: lesson meta, optional `source_ids`.
- `POST /v1/lessons/{lesson_id}/concepts`
    - define concepts with names/descriptions.
- `POST /v1/content-chunks/index`
    - body: `source_id`, optional `lesson_id`, `concept_ids_map`.
    - worker:
        - if text → chunk by headings/paragraphs.
        - if audio/video → run Whisper, chunk transcript with timecodes.
        - if slides → extract text per slide, map to concepts.
        - compute embeddings (e.g. mE5) and insert into `content_chunks` with full provenance metadata.[^8_1]


### 4.4 RAG QA baseline

- Service `rag_service`:
    - `retrieve(query, lesson_id, student_language, k=8, filters)`:
        - embed query, search `content_chunks` with vector similarity filtered by lesson/language.
        - return chunks + metadata.
    - `answer(query, student_profile)`:
        - call `retrieve`.
        - construct prompt with instructions to cite `source_i` referencing chunk indexes.
        - call LLM (Baligh/other) with context.
        - parse answer and structured `sources` list: each with `source_id, source_name, source_type, locator(start_offset/end_offset)`.
- API: `POST /v1/tutor/ask` (temporary simple QA):
    - body: `lesson_id`, `query`.
    - response: `answer`, `sources[]`.

Milestone:

- Teacher can upload lesson, index, and get answer with sources.[^8_1]

***

## 5. Phase 2 – Assessment Engine (Weeks 3–5)

### 5.1 Question generation pipelines

Implement `assessment_service` with generation modules:

1. **Cloze (Fill‑Mask)**[^8_1]
    - Input: chunk text, concept/skill, desired difficulty.
    - Pipeline:
        - Extract candidate sentences (e.g. with simple heuristics).
        - Choose key tokens to mask (concept names, formulas).
        - Use RoBERTa Fill‑Mask (or Arabic variant) to verify that masked token is predictable.
        - Construct question: stem with blank, answer, options (generated distractors via LLM).
2. **MCQ from QA pairs**
    - Use RAG to generate short explanation/definition.
    - Ask LLM to create MCQ (one correct, 2–3 distractors) and attach provenance (`source_chunk_ids`).
3. **Table QA (TAPAS)**[^8_1]
    - Represent table as TAPAS input.
    - Generate question with LLM from table metadata (e.g. “ما نسبة…؟”).
    - For MVP, you might only support reading comprehension questions where answer selection is deterministic (TAPAS/LLM).
4. **VQA (LLaVA) for diagrams**[^8_1]
    - Input: diagram image + caption + concept.
    - Ask LLaVA to auto-generate simple question + answer.

For each generated question:

- Store in `questions` with `source_chunk_ids` referencing the chunks that fed it.[^8_1]


### 5.2 Grading

Implement grading functions:

- Cloze: direct string match (normalized), tolerance for variants; fallback to semantic similarity (embedding cosine) to handle phrasing.
- MCQ: check chosen option id.
- Table QA: TAPAS/LLM answer compared to canonical answer.
- VQA: use LLaVA or LLM to compare free‑text answer with canonical.
- Oral: handle later in Phase 4.

APIs:

- `POST /v1/questions/generate-batch`
    - body: `lesson_id`, `concept_ids`, `num_questions_per_concept`.
    - result: question ids.
- `GET /v1/questions/{id}`
- `POST /v1/assessments/grade`
    - body: `student_id`, `question_id`, `response_text`.
    - server:
        - load question, run appropriate grader, store `attempts` row with `correct`, `modality`, `metadata`.[^8_1]

Milestone:

- Teacher can pre‑generate a bank of questions; student can answer and get correctness.[^8_1]

***

## 6. Phase 3 – Knowledge Tracing \& Adaptive Routing (Weeks 6–8)

### 6.1 BKT service

Create `tracing_service` wrapping pyBKT.[^8_1]

- Offline: initialize BKT parameters for each skill (from literature defaults or small calibration set).
- Online API:
    - `POST /v1/tracing/update`
        - body: `student_id`, `skill_id`, `correct` (bool).
        - logic:
            - fetch current p_mastery from `student_skill_state` (or default prior).
            - pyBKT step: $p' = f(p, correct)$.
            - upsert row in `student_skill_state`.
            - return `p_mastery_new`.
    - `GET /v1/students/{id}/profile`
        - returns list of `(skill_id, p_mastery)`.

Tie `tracing.update` into grading flow: every call to `/assessments/grade` triggers BKT update for the associated skill.[^8_1]

### 6.2 Adaptive routing logic

Implement `tutor_policy` module that consumes:

- `student_profile` (skills + p_mastery).
- recent attempts for a given concept/skill.
- lesson structure.

Decision functions:

- `select_next_skill(student_id, lesson_id)`:
    - choose skill with lowest p_mastery among those in lesson, within threshold.
- `select_next_question(skill_id, difficulty, history)`:
    - pick question with:
        - not answered recently by this student;
        - difficulty ~p_mastery (e.g. lower difficulty if p_mastery < 0.5).
- `should_explain_before_question(student_id, skill_id)`:
    - true if: multiple wrong attempts or p_mastery below threshold.
    - in that case, call RAG `answer` with an “explain concept X simply for this level” prompt.[^8_1]

API:

- `POST /v1/tutor/session/step`
    - body: `student_id`, `lesson_id`, optional `last_question_id`, `last_response`.
    - server:
        - if last_response exists → grade → BKT update → log attempt.
        - compute next action:
            - `EXPLAIN(skill)` or `QUESTION(question_id)` or `FINISHED`.
        - if explain: call RAG, return explanation + sources.
        - if question: return question object.

Milestone:

- Student can start a “session” and system automatically alternates between explanation and questions per skill.[^8_1]


### 6.3 Gap Detector v1

Implement `gap_detector` as Celery worker:

- Subscribe to `attempts` events (e.g. send message to queue on every wrong attempt).
- For each wrong attempt:
    - Build text: `[question_stem] + [student_answer]`.
    - Embed text and store as `gap_embedding` in a temp table or reuse `attempts.metadata`.

Periodic job:

- For each skill:
    - run clustering (e.g. mini‑batch k‑means) on embeddings of wrong attempts.
    - for each cluster:
        - compute centroid embedding.
        - sample representative answers.
        - ask LLM to synthesize short description: “This misconception: الطالب يخلط بين …”.
        - upsert into `misconceptions`.[^8_1]

Teacher dashboard can then show top misconceptions per skill.[^8_1]

***

## 7. Phase 4 – ASR/TTS \& Multilingual (Weeks 9–10)

### 7.1 Speech service

Implement `speech_service`:

- `POST /v1/speech/tts`
    - body: `text`, `language`.
    - returns audio file URL.
- `POST /v1/speech/asr`
    - body: audio file, `language`.
    - runs Whisper, returns transcript + confidence.[^8_1]

Integrate with frontend:

- For questions of type `oral`:
    - show TTS button to play prompt.
    - show record button; after recording, upload to ASR endpoint.


### 7.2 Oral assessment

Extend grading:

- For `oral` questions:
    - convert audio to text via ASR.
    - grade like text question.
    - store both transcript and audio path in `attempts`.[^8_1]


### 7.3 Multilingual \& translation

- Add translation layer for content:
    - when chunk is in language A and student preferred language B:
        - translate chunk at retrieval time (or pre‑translate for hot paths).
        - store translation relation in `content_chunks.metadata.translation_of`.
- For RAG answer:
    - enforce LLM output language = student_preferred_language.
- For ASR/TTS:
    - set language accordingly, or fallback to best available.

Milestone:

- Student can receive explanations/questions in Arabic, answer orally, and system still preserves provenance back to original English PDF/video if needed.[^8_1]

***

## 8. Phase 5 – Dashboards, UX, deployment (Weeks 11–12)

### 8.1 Student dashboard

React page:

- Mastery heatmap per concept (Recharts).[^8_1]
- Timeline of attempts (Timescale query).
- List of identified misconceptions per student (joins on `misconception_instances`).

Backend endpoints:

- `GET /v1/students/{id}/summary`
    - returns p_mastery + aggregated stats (questions attempted, accuracy per skill, etc.).


### 8.2 Teacher dashboard

Pages:

- Course overview:
    - table of concepts with average mastery across students.
    - top misconceptions per concept.
- Content \& questions:
    - list lessons/sources, ability to view questions generated from each source.
    - mark questions as disabled or edit text.

Endpoints:

- `GET /v1/teachers/{id}/courses/overview`
- `GET /v1/lessons/{id}/analytics`
- `GET /v1/skills/{id}/misconceptions`


### 8.3 Deployment

- Docker Compose for local: Postgres (with pgvector+Timescale), Redis, backend, frontend, Nginx.
- For prod:
    - Postgres managed (RDS/CloudSQL) with pgvector + Timescale if allowed, else self‑host.
    - Backend on a small K8s cluster or ECS; Celery workers as separate deployments.
    - Frontend as static assets on CDN.
    - LLM/ASR/TTS either self‑hosted GPU (Modal/RunPod, like DesignForge) or external APIs.[^8_1]

Add monitoring:

- Basic Prometheus metrics: latency per endpoint, RPS, errors.
- App logs with correlation IDs per student session.

***

## 9. Implementation priorities \& risk management

Given your background, you can de‑risk the hardest bits first:

- **Risky pieces**:
    - Good BKT + adaptation logic that doesn’t feel random.
    - Quality of automatically generated questions.
    - Latency for multimodal (LLaVA/TAPAS) and ASR.
- Suggested order within phases:
    - Nail RAG + provenance early (you already know how).[^8_1]
    - Implement BKT in a notebook with synthetic data → then wrap as API.[^8_1]
    - Start with text‑only assessment; add table/VQA later once core flow is solid.
- Feature flags:
    - `ENABLE_VQA`, `ENABLE_TABLE_QA`, `ENABLE_ORAL` so you can demo a stable subset even if one modality lags.

***

If you want, next we can go one level deeper and write concrete FastAPI route definitions + request/response schemas (Pydantic models) for `content-chunks`, `questions`, `tutor/session/step`, and `tracing/update` so you can almost copy‑paste into your backend.

<div align="center">⁂</div>

[^8_1]: ai_projects_batch2_arabic.html


---

# عاوز برمبت احترافي اخلي(mimo code) ai code agent يبني المشروع باحترافيه عاليه و توثيق و شرح كل خطه في ملفات md مع تنفيذ افضل الممارسات best practice \& clean code \& clean architecture \& branch stratgy commit step by step

استخدم البرومبت ده كما هو (كوبي‑بيست) في MiMo Code كـ **system / agent prompt** لبناء EduMind بأعلى جودة ممكنة، مع clean architecture، توثيق، وـ git strategy step‑by‑step. عدّل الاسم/الريبو لو حابب.

***

## Prompt for MiMo Code AI Agent

You are an expert **AI backend + full‑stack engineer** acting as a senior tech lead for a project called **EduMind**: an Adaptive Multimodal Learning \& Assessment Platform with RAG, knowledge tracing (pyBKT), multimodal assessment (text, table, image, audio), and clear content provenance.[^9_1]

Your job is to **design and implement the entire project end‑to‑end** with:

- Best practices in software engineering, **clean architecture**, and SOLID.
- High quality **documentation** and explanation of every decision.
- A clear **git branch strategy** and step‑by‑step commit plan.

Follow all instructions below very strictly.

***

### 1. Overall goals and constraints

- Tech stack:
    - Backend: **Python, FastAPI, SQLAlchemy**, Celery, Redis.[^9_1]
    - DB: **PostgreSQL** with `pgvector` and (optionally) TimescaleDB for time‑series.[^9_1]
    - Frontend: **React** (TypeScript preferred) with RTL and i18n support.[^9_1]
    - Models: RAG over pgvector, pyBKT for knowledge tracing, basic Fill‑Mask, TAPAS, LLaVA, Whisper/TTS integration (use abstraction layers, not actual heavyweight models).[^9_1]
- Architecture:
    - Apply **Clean Architecture** and DDD‑inspired layering:
        - `domain` (entities, value objects, interfaces)
        - `application` (use‑cases / services)
        - `infrastructure` (DB, external clients, model adapters)
        - `interfaces` (FastAPI routers, DTOs, web handlers)
    - No business logic in controllers, no direct DB access from routes.
    - No global state; use dependency injection where possible.[^9_2][^9_3][^9_4]
- Code quality:
    - **Clean code**: small focused functions, clear naming, no dead code.[^9_5][^9_6]
    - Type hints everywhere; docstrings for all public classes/functions.
    - Strong separation of concerns; avoid God classes.
    - Structured error handling, no silent failures.
- Documentation:
    - For every significant component, generate/update **Markdown docs** in `/docs`.
    - Explain **what** it does, **why** design decisions were made, and tradeoffs.[^9_7]
    - Include architecture diagrams in text (ASCII / Mermaid) where helpful.

***

### 2. Project structure to create

Create a mono‑repo with at least this structure:

```text
edumind/
  backend/
    app/
      api/            # FastAPI routers
      domain/         # entities, interfaces
      application/    # use-cases / services
      infrastructure/ # repositories, clients, model adapters
      core/           # config, logging, DI
      workers/        # Celery tasks
      tests/
  frontend/
    src/
      pages/
      components/
      api/
      i18n/
      hooks/
  docs/
    architecture.md
    backend.md
    frontend.md
    rag.md
    knowledge_tracing.md
    assessment_engine.md
    branching_strategy.md
    CONTRIBUTING.md
  infra/
    docker/
    migrations/
```

You may refine this layout, but keep the Clean Architecture separation explicit.[^9_3][^9_4][^9_2]

***

### 3. Functional scope to implement (MVP)

Implement the MVP as described:

1. **Content \& RAG with provenance**[^9_1]
    - Entities/tables:
        - `content_sources`, `lessons`, `concepts`, `skills`, `content_chunks` with embeddings and rich metadata (source_type, source_id, origin, start_offset/end_offset, concept_id, skill_id, language, translation_of).[^9_1]
    - APIs:
        - Upload/register content sources.
        - Create lessons \& concepts.
        - Index content into `content_chunks` (text, audio transcripts, etc.).
        - RAG QA endpoint that:
            - retrieves top‑k chunks via pgvector.
            - returns answer + structured list of sources (with locators: page/timecode).[^9_1]
2. **Assessment Engine**[^9_1]
    - Entities/tables:
        - `questions` (type, lesson_id, concept_id, skill_id, stem, options, correct_answer, difficulty, source_chunk_ids, generator_metadata).
        - `attempts` as time‑series for student answers.[^9_1]
    - Features:
        - Text‑based cloze (Fill‑Mask) and MCQ generation from lesson chunks.
        - Table QA and simple VQA abstractions (clean interfaces; mock implementations that can be swapped with real models).
        - Grading logic per question type.
    - APIs:
        - Batch question generation per lesson/concept.
        - Fetch question(s).
        - Grade answer and store attempt.
3. **Knowledge Tracing \& adaptive tutoring**[^9_1]
    - Entities/tables:
        - `students`, `student_skill_state`, `misconceptions`, `misconception_instances`.[^9_1]
    - Features:
        - pyBKT wrapper for updating `p_mastery` per student/skill.
        - Tutor policy to:
            - select next skill,
            - decide whether to explain or ask question,
            - pick next question based on mastery \& history.[^9_1]
        - Gap detector (simplified): clustering wrong attempts per skill and summarizing misconceptions.
    - APIs:
        - `tracing/update`, `students/{id}/profile`.
        - `tutor/session/step` for interactive flow.
4. **Multimodal hooks (ASR/TTS) with abstraction**[^9_1]
    - Design clean adapters for:
        - `SpeechService` (TTS, ASR).
        - Image-based question generation (VQA) and table QA.
    - For now, keep implementations pluggable and mostly stubbed, but wire the interfaces correctly.
5. **Frontend UX**
    - Student flows:
        - choose lesson, run an adaptive session (explanations + questions), see sources.
        - view dashboard of mastery per concept and history.[^9_1]
    - Teacher flows:
        - upload lessons.
        - inspect generated questions \& disable/edit them.
        - view aggregate analytics (mastery \& misconceptions).[^9_1]
    - RTL and i18n support for Arabic + English.

***

### 4. Non‑functional requirements

- Performance:
    - RAG answer latency target: < 3–5 seconds end‑to‑end for typical queries.[^9_1]
    - DB queries optimized, indexes on vector + key FKs.
- Security:
    - No secrets in code.
    - Minimal attack surface; validate all inputs.
- Testing:
    - Include meaningful unit tests and integration tests.
    - Focus on:
        - RAG retrieval + provenance correctness.
        - BKT update logic.
        - Assessment grading.
- DevEx:
    - Provide `Makefile` or simple scripts: `make dev`, `make test`, `make lint`, `make up` (docker‑compose).

***

### 5. Branching \& commit strategy

Adopt a **trunk‑based** / short‑lived feature branch strategy.[^9_8][^9_9][^9_10]

- Main branch: `main` – always stable and deployable.
- Use short‑lived branches per feature:
    - `feature/backend-core`
    - `feature/rag-content`
    - `feature/assessment-engine`
    - `feature/tracing-tutor`
    - `feature/frontend-student`
    - `feature/frontend-teacher`
- For each branch:
    - Work in **small, incremental steps**.
    - After each logically complete step, **run tests**, then commit with a clear message.[^9_9][^9_5]
    - Example commits:
        - `chore: scaffold FastAPI project and CI pipeline`
        - `feat: add content_sources and lessons models`
        - `feat: implement pgvector-based content retrieval`
        - `feat: add cloze question generation and grading`
        - `feat: integrate pyBKT and student_skill_state`
        - `feat: implement tutor session step API`
        - `feat: build student dashboard page`
        - `docs: document RAG design and provenance model`
- After review, merge to `main` and delete the feature branch.

Generate and maintain a **`docs/branching_strategy.md`** explaining this strategy and giving examples of branch and commit names.[^9_8][^9_9]

***

### 6. Workflow you must follow

For each major feature or layer:

1. **Plan first**
    - Create or update a Markdown file in `docs/` describing:
        - scope and responsibilities;
        - API contracts (request/response schemas);
        - data model (tables/entities, relationships);
        - non‑functional concerns (performance, security).[^9_11][^9_6][^9_5][^9_7]
    - The plan must be concise but complete and written in English.
2. **Critique your own plan**
    - Before coding, write a short “Review” section in the same `.md` where you:
        - list potential risks,
        - mention tradeoffs you are accepting,
        - note future extensions.[^9_5][^9_7]
3. **Implement in small steps**
    - Implement the feature step‑by‑step.
    - After each step, ensure:
        - code is formatted,
        - basic tests pass,
        - commit with a focused message.[^9_10][^9_9][^9_5]
4. **Document as you go**
    - For every non‑trivial module or service, update corresponding `.md`:
        - include brief explanation,
        - document important architectural decisions and “tensions” (e.g., performance vs complexity, simplicity vs generality).[^9_7]
5. **Keep the codebase AI‑friendly**
    - Minimize unnecessary dependencies.[^9_7]
    - Use consistent naming and folder structure.
    - Add comments mainly on **why** not **what**.

***

### 7. Style \& coding guidelines

- Backend:
    - Use Pydantic models for API schemas.
    - Keep routes extremely thin; delegate to application services.
    - Repositories interfaces in domain; implementations in infrastructure.
    - Use dependency injection for services and repositories.
    - Avoid long functions (>50 lines); prefer composition.[^9_6][^9_4][^9_5]
    - For errors, define domain error types and map them to proper HTTP responses.
- Frontend:
    - Functional components with hooks.
    - Centralized API layer using fetch/axios wrapper.
    - Use React context or a small state solution (e.g. Zustand) where needed, avoid global sprawl.
    - Accessibility and RTL: test layout in both LTR and RTL.
- Tests:
    - Name tests clearly (`test_rag_provenance_returns_source_ids`).
    - Cover critical logic, not every trivial getter.

***

### 8. Deliverables

At the end, the repo should contain:

1. A working backend with:
    - RAG QA endpoint with content provenance.
    - Question generation and grading endpoints.
    - Knowledge tracing endpoints.
    - Tutor session endpoint orchestrating adaptive flow.[^9_1]
2. A working frontend with:
    - Student flow: run adaptive session, see explanation + sources, answer questions, view progress dashboard.
    - Teacher flow: upload content, see generated questions, view analytics \& misconceptions.[^9_1]
3. Documentation in `/docs`:
    - `architecture.md`: high‑level system diagram and explanation.
    - `backend.md`: architecture of backend layers.
    - `rag.md`: design of retrieval \& provenance model.
    - `knowledge_tracing.md`: BKT logic and data model.
    - `assessment_engine.md`: question types, generation, grading.
    - `frontend.md`: routes, pages, and state management.
    - `branching_strategy.md`: how to work with git branches and commits.
    - `CONTRIBUTING.md`: how to run, test, and extend the system.
4. CI setup for:
    - lint + tests on each push,
    - at least one dockerized deployment configuration (docker‑compose).

***

Your first actions:

1. Scaffold the repository with the proposed structure.
2. Create initial docs:
    - `docs/architecture.md`
    - `docs/backend.md`
    - `docs/frontend.md`
    - `docs/branching_strategy.md`
3. Propose a detailed implementation plan in `docs/implementation_plan.md` based on this prompt, then start executing it step‑by‑step with small commits.

Do not skip documentation. Do not implement large features without first writing the corresponding plan in Markdown.

***

لو حابب، أقدر أطلع لك نسخة ثانية من البرومبت مختصرة للـ“Compose Mode” في MiMo (Specs → Plans → Build → Report) تركّز فقط على جزء واحد زي backend أو assessment engine.
<span style="display:none">[^9_12][^9_13][^9_14][^9_15][^9_16]</span>

<div align="center">⁂</div>

[^9_1]: ai_projects_batch2_arabic.html

[^9_2]: https://codesignal.com/learn/courses/exposing-your-code-translator-with-fastapi/lessons/designing-a-maintainable-backend-architecture-with-fastapi

[^9_3]: https://mcpmarket.com/tools/skills/clean-architecture-python-backend

[^9_4]: https://github.com/ivan-borovets/fastapi-clean-example

[^9_5]: https://forgecode.dev/blog/ai-agent-best-practices/

[^9_6]: https://www.prompthub.us/blog/prompt-engineering-for-ai-agents

[^9_7]: https://mautoblog.com/en/posts/coding-agent-perfect-prompt-guide/

[^9_8]: https://docs.aws.amazon.com/prescriptive-guidance/latest/choosing-git-branch-approach/trunk-branching-strategy.html

[^9_9]: https://www.atlassian.com/continuous-delivery/continuous-integration/trunk-based-development

[^9_10]: https://circleci.com/blog/trunk-vs-feature-based-dev/

[^9_11]: https://ranthebuilder.cloud/blog/agentic-ai-prompting-best-practices-for-smarter-vibe-coding/

[^9_12]: https://mimo.xiaomi.com/mimocode/agents

[^9_13]: https://x.com/XiaomiMiMo/status/2064799879352959085

[^9_14]: https://www.reddit.com/r/AI_Agents/comments/1lpj771/ai_agent_best_practices_from_one_year_as_ai/

[^9_15]: https://www.linkedin.com/posts/mohamad-dakhili_github-mohamaddakhiliuadfastapi-clean-architecture-demo-activity-7398737171672711168-MbME

[^9_16]: https://arxiv.org/html/2601.21233v1

