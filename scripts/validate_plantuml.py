"""Скрипт синтаксичної та структурної валідації діаграми варіантів використання PlantUML.

Перевіряє docs/usecase.puml згідно з specs/001-uml-domain-model/contracts/usecase-contract.md.
"""

import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

REQUIRED_ACTORS = ["Importer", "CustomsBroker", "CustomsInspector"]

REQUIRED_USECASES = [
    "UC_SubmitDocs",
    "UC_VerifyDocs",
    "UC_DraftDeclaration",
    "UC_ClassifyItem",
    "UC_CalculateDuties",
    "UC_ApplyPreference",
    "UC_AssignInspection",
    "UC_PayDuties",
    "UC_ReleaseCargo",
    "UC_RejectCargo",
]

REQUIRED_INCLUDES = [
    ("UC_DraftDeclaration", "UC_ClassifyItem"),
    ("UC_DraftDeclaration", "UC_CalculateDuties"),
]

REQUIRED_EXTENDS = [
    ("UC_ApplyPreference", "UC_CalculateDuties"),
    ("UC_RejectCargo", "UC_AssignInspection"),
]


def validate_plantuml(file_path: Path) -> bool:
    print(f"=== Валідація PlantUML діаграми: {file_path.name} ===")

    if not file_path.exists():
        print(f"[FAIL] Файл не знайдено: {file_path}")
        return False

    raw_bytes = file_path.read_bytes()
    if raw_bytes.startswith(b"\xef\xbb\xbf"):
        print("[FAIL] Файл містить UTF-8 BOM. Вимагається UTF-8 без BOM.")
        return False
    print("[SUCCESS] Файл має коректне кодування UTF-8 без BOM.")

    try:
        content = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as e:
        print(f"[FAIL] Помилка декодування UTF-8: {e}")
        return False

    lines = [line.strip() for line in content.splitlines() if line.strip()]

    # 1. Перевірка @startuml та @enduml
    has_start = any(line.startswith("@startuml") for line in lines)
    has_end = any(line.startswith("@enduml") for line in lines)
    if not (has_start and has_end):
        print("[FAIL] Відсутні директиви @startuml або @enduml.")
        return False
    print("[SUCCESS] Директиви @startuml та @enduml присутні.")

    # 2. Перевірка left to right direction
    if "left to right direction" in content:
        print("[SUCCESS] Директива 'left to right direction' присутня.")
    else:
        print("[WARN] Рекомендована директива 'left to right direction' відсутня.")

    # 3. Перевірка системної рамки
    if re.search(r'rectangle\s+["\'].*CustomsBroker.*["\']', content, re.IGNORECASE):
        print("[SUCCESS] Системна рамка rectangle для CustomsBroker знайдена.")
    else:
        print("[FAIL] Не знайдено рамку rectangle для меж системи CustomsBroker.")
        return False

    # 4. Перевірка 3 акторів
    actors_ok = True
    for actor in REQUIRED_ACTORS:
        pattern = rf"actor\s+.*as\s+{actor}\b|actor\s+{actor}\b"
        if re.search(pattern, content):
            print(f"[SUCCESS] Знайдено актора: {actor}")
        else:
            print(f"[FAIL] Відсутній обов'язковий актор: {actor}")
            actors_ok = False
    if not actors_ok:
        return False

    # 5. Перевірка 10 прецедентів
    uc_ok = True
    for uc in REQUIRED_USECASES:
        pattern = rf"usecase\s+.*as\s+{uc}\b|\({uc}\)"
        if re.search(pattern, content) or f"as {uc}" in content or f"({uc})" in content:
            print(f"[SUCCESS] Знайдено прецедент: {uc}")
        else:
            print(f"[FAIL] Відсутній прецедент: {uc}")
            uc_ok = False
    if not uc_ok:
        return False

    # 6. Перевіркастереотипів <<include>> та <<extend>>
    includes_found = len(re.findall(r"<<include>>", content, re.IGNORECASE))
    extends_found = len(re.findall(r"<<extend>>", content, re.IGNORECASE))
    print(f"[INFO] Знайдено зв'язків <<include>>: {includes_found}, <<extend>>: {extends_found}")

    if includes_found < 2:
        print("[FAIL] Очікується щонайменше 2 зв'язки <<include>>.")
        return False
    if extends_found < 2:
        print("[FAIL] Очікується щонайменше 2 зв'язки <<extend>>.")
        return False

    for source, target in REQUIRED_INCLUDES:
        pattern = rf"\({source}\)\s*\.\.>\s*\({target}\)\s*:\s*<<include>>"
        if not re.search(pattern, content, re.IGNORECASE):
            print(f"[FAIL] Не знайдено обов'язковий include зв'язок: ({source}) ..> ({target}) : <<include>>")
            return False
    print("[SUCCESS] Обов'язкові зв'язки <<include>> підтверджено.")

    for source, target in REQUIRED_EXTENDS:
        pattern = rf"\({source}\)\s*\.\.>\s*\({target}\)\s*:\s*<<extend>>"
        if not re.search(pattern, content, re.IGNORECASE):
            print(f"[FAIL] Не знайдено обов'язковий extend зв'язок: ({source}) ..> ({target}) : <<extend>>")
            return False
    print("[SUCCESS] Обов'язкові зв'язки <<extend>> підтверджено.")

    # 7. Перевірка асоціацій акторів
    actor_associations = [
        ("Importer", "UC_SubmitDocs"),
        ("Importer", "UC_PayDuties"),
        ("CustomsBroker", "UC_VerifyDocs"),
        ("CustomsBroker", "UC_DraftDeclaration"),
        ("CustomsBroker", "UC_PayDuties"),
        ("CustomsInspector", "UC_AssignInspection"),
        ("CustomsInspector", "UC_ReleaseCargo"),
        ("CustomsInspector", "UC_RejectCargo"),
    ]
    for act, uc in actor_associations:
        pattern = rf"{act}\s*(-->|--)\s*\(?{uc}\)?"
        if not re.search(pattern, content):
            print(f"[FAIL] Не знайдено асоціацію між актором {act} та прецедентом {uc}")
            return False
    print("[SUCCESS] Усі асоціативні зв'язки між акторами та прецедентами валідні.")

    print("\n[SUCCESS] Діаграма варіантів використання повністю валідна та відповідає контракту!")
    return True


def main():
    if len(sys.argv) > 1:
        target_path = Path(sys.argv[1])
    else:
        target_path = Path(__file__).resolve().parent.parent / "docs" / "usecase.puml"

    if validate_plantuml(target_path):
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
