"""Fix all repository files to use _to_str for UUID comparisons."""
import re

files_and_patterns = [
    ("app/infrastructure/db/repositories/content_repo.py", [
        (r"\.id == id\)", ".id == _to_str(id))"),
        (r"\.lesson_id == lesson_id\)", ".lesson_id == _to_str(lesson_id))"),
        (r"\.concept_id == concept_id\)", ".concept_id == _to_str(concept_id))"),
        (r"\.skill_id == skill_id\)", ".skill_id == _to_str(skill_id))"),
        (r"\.source_id == source_id\)", ".source_id == _to_str(source_id))"),
    ]),
    ("app/infrastructure/db/repositories/question_repo.py", [
        (r"\.id == id\)", ".id == _to_str(id))"),
        (r"\.lesson_id == lesson_id\)", ".lesson_id == _to_str(lesson_id))"),
        (r"\.concept_id == concept_id\)", ".concept_id == _to_str(concept_id))"),
        (r"\.skill_id == skill_id\)", ".skill_id == _to_str(skill_id))"),
    ]),
    ("app/infrastructure/db/repositories/gap_repo.py", [
        (r"\.id == id\)", ".id == _to_str(id))"),
        (r"\.skill_id == skill_id\)", ".skill_id == _to_str(skill_id))"),
    ]),
]

for filepath, replacements in files_and_patterns:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Add _to_str import if not present
    if "_to_str" not in content:
        content = "from uuid import UUID\n\n\ndef _to_str(val) -> str:\n    return str(val) if isinstance(val, UUID) else val\n\n" + content

    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Fixed {filepath}")
