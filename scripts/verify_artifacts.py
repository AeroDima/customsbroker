"""Майстер-скрипт верифікації артефактів моделювання предметної області.

Перевіряє виконання критеріїв успішності SC-001 - SC-006 згідно зі специфікацією:
- SC-001: Наявність усіх 5 цільових файлів у каталозі docs/ та кодування UTF-8 без BOM.
- SC-002: Синтаксична валідність діаграм Mermaid (через mmdc) та PlantUML.
- SC-003: Наявність 4 обов'язкових типів зв'язків у діаграмі класів.
- SC-004: Узгодженість викликів методів та станів із діаграмою класів.
- SC-005: Аудит структури та наповненості Excel-таблиці CRC-карток.
- SC-006: Дотримання двомовного стандарту (англійські ідентифікатори, українські описи).
"""

import os
import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"

EXPECTED_FILES = [
    "usecase.puml",
    "class.mmd",
    "sequence.mmd",
    "state.mmd",
    "crc.xlsx",
]

TEXT_DIAGRAM_FILES = [
    "usecase.puml",
    "class.mmd",
    "sequence.mmd",
    "state.mmd",
]

MERMAID_FILES = [
    "class.mmd",
    "sequence.mmd",
    "state.mmd",
]


def check_sc001_presence_and_encoding():
    """SC-001: Перевірка наявності всіх 5 файлів та кодування UTF-8 без BOM."""
    print("\n--- [SC-001] Перевірка наявності файлів та кодування UTF-8 ---")
    all_ok = True

    for filename in EXPECTED_FILES:
        filepath = DOCS_DIR / filename
        if not filepath.exists():
            print(f"  [FAIL] Файл відсутній: docs/{filename}")
            all_ok = False
            continue

        print(f"  [OK] Знайдено: docs/{filename}")

        if filename in TEXT_DIAGRAM_FILES:
            raw_data = filepath.read_bytes()
            if raw_data.startswith(b"\xef\xbb\xbf"):
                print(f"  [FAIL] Файл docs/{filename} містить UTF-8 BOM!")
                all_ok = False
            else:
                try:
                    raw_data.decode("utf-8")
                    print(f"  [OK] docs/{filename} має коректне кодування UTF-8 (без BOM)")
                except UnicodeDecodeError as e:
                    print(f"  [FAIL] docs/{filename} не є валідним UTF-8: {e}")
                    all_ok = False

    return all_ok


def check_sc002_diagram_syntax():
    """SC-002: Перевірка компіляції/синтаксису Mermaid через CLI та PlantUML."""
    print("\n--- [SC-002] Синтаксична валідація діаграм ---")
    all_ok = True

    # 1. Mermaid діаграми через mmdc
    for filename in MERMAID_FILES:
        filepath = DOCS_DIR / filename
        if not filepath.exists():
            print(f"  [SKIP] docs/{filename} не знайдено, пропуск валідації Mermaid")
            all_ok = False
            continue

        temp_out = DOCS_DIR / f"{filepath.stem}_temp.svg"
        cmd = [
            "npx",
            "-y",
            "@mermaid-js/mermaid-cli",
            "-i",
            str(filepath),
            "-o",
            str(temp_out),
        ]
        try:
            res = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                check=False,
            )
            if res.returncode == 0 and temp_out.exists():
                print(f"  [OK] Mermaid CLI успішно скомпілював docs/{filename}")
                if temp_out.exists():
                    temp_out.unlink()
            else:
                print(f"  [FAIL] Помилка компіляції docs/{filename} через Mermaid CLI:")
                print(res.stderr or res.stdout)
                all_ok = False
                if temp_out.exists():
                    temp_out.unlink()
        except Exception as ex:
            print(f"  [FAIL] Виняток під час запуску Mermaid CLI для docs/{filename}: {ex}")
            all_ok = False
            if temp_out.exists():
                temp_out.unlink()

    # 2. PlantUML валідація через скрипт validate_plantuml.py якщо він існує
    validator_script = PROJECT_ROOT / "scripts" / "validate_plantuml.py"
    usecase_file = DOCS_DIR / "usecase.puml"
    if validator_script.exists() and usecase_file.exists():
        cmd = [sys.executable, str(validator_script), str(usecase_file)]
        res = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if res.returncode == 0:
            print("  [OK] docs/usecase.puml пройшов структурну валідацію")
        else:
            print(f"  [FAIL] docs/usecase.puml не пройшов валідацію:\n{res.stdout}\n{res.stderr}")
            all_ok = False
    elif not usecase_file.exists():
        print("  [SKIP] docs/usecase.puml відсутній")
        all_ok = False

    return all_ok


def check_sc003_class_relationships():
    """SC-003: Перевірка 4 обов'язкових типів зв'язків у docs/class.mmd."""
    print("\n--- [SC-003] Перевірка 4 типів зв'язків у docs/class.mmd ---")
    class_file = DOCS_DIR / "class.mmd"
    if not class_file.exists():
        print("  [FAIL] docs/class.mmd відсутній")
        return False

    content = class_file.read_text(encoding="utf-8")
    req_rels = {
        "Наслідування (<|--)": r"<\|--",
        "Реалізація інтерфейсу (<|..)": r"<\|\.\.",
        "Строга композиція (*--)": r"\*--",
        "Залежність (..>)": r"\.\.>",
    }

    all_found = True
    for name, pattern in req_rels.items():
        if re.search(pattern, content):
            print(f"  [OK] Знайдено тип зв'язку: {name}")
        else:
            print(f"  [FAIL] Не знайдено обов'язковий тип зв'язку: {name}")
            all_found = False

    return all_found


def check_sc004_behavior_consistency():
    """SC-004: Узгодженість викликів методів та станів із моделлю даних."""
    print("\n--- [SC-004] Перевірка узгодженості методів та станів ---")
    seq_file = DOCS_DIR / "sequence.mmd"
    state_file = DOCS_DIR / "state.mmd"
    class_file = DOCS_DIR / "class.mmd"

    if not seq_file.exists() or not state_file.exists() or not class_file.exists():
        print("  [FAIL] Відсутні необхідні файли діаграм для аналізу узгодженості")
        return False

    seq_content = seq_file.read_text(encoding="utf-8")
    class_content = class_file.read_text(encoding="utf-8")
    state_content = state_file.read_text(encoding="utf-8")

    # Перевірка ключових методів із контракту sequence у діаграмі класів
    contract_methods = [
        "submitDocuments",
        "processDocumentPackage",
        "createDeclaration",
        "validateCodeFormat",
        "getTariffRate",
        "calculateDuties",
        "submitDeclaration",
        "verifyDocuments",
        "assignInspection",
        "markDutiesPaid",
        "updateStatus",
        "releaseCargo",
    ]

    all_ok = True
    for m in contract_methods:
        if m in seq_content and m in class_content:
            print(f"  [OK] Метод '{m}' узгоджено між sequence.mmd та class.mmd")
        else:
            print(f"  [FAIL] Метод '{m}' відсутній в одній із діаграм (seq/class)")
            all_ok = False

    # Перевірка обов'язкових станів
    req_states = [
        "DocumentsReceived",
        "DeclarationDrafting",
        "DeclarationVerified",
        "InspectionAssigned",
        "DutiesCalculatedAndPaid",
        "CargoReleased",
        "Rejected",
    ]
    for s in req_states:
        if s in state_content:
            print(f"  [OK] Стан '{s}' знайдено в docs/state.mmd")
        else:
            print(f"  [FAIL] Стан '{s}' відсутній в docs/state.mmd")
            all_ok = False

    return all_ok


def check_sc005_crc_cards():
    """SC-005: Аудит вмісту та структури таблиці CRC-карток docs/crc.xlsx."""
    print("\n--- [SC-005] Перевірка таблиці CRC-карток docs/crc.xlsx ---")
    validator_script = PROJECT_ROOT / "scripts" / "validate_crc.py"
    crc_file = DOCS_DIR / "crc.xlsx"

    if not crc_file.exists():
        print("  [FAIL] docs/crc.xlsx відсутній")
        return False

    if validator_script.exists():
        res = subprocess.run(
            [sys.executable, str(validator_script), str(crc_file)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        print(res.stdout)
        if res.returncode == 0:
            print("  [OK] docs/crc.xlsx успішно пройшов аудит")
            return True
        else:
            print(f"  [FAIL] docs/crc.xlsx не пройшов перевірку:\n{res.stderr}")
            return False
    else:
        print("  [SKIP] scripts/validate_crc.py ще не створено")
        return False


def check_sc006_bilingual_compliance():
    """SC-006: Дотримання двомовного стандарту (англійський код, український текст)."""
    print("\n--- [SC-006] Перевірка дотримання двомовного стандарту ---")
    # Перевіримо наявність українського тексту та англійських назв у діаграмах
    all_ok = True
    for f in ["usecase.puml", "class.mmd", "sequence.mmd", "state.mmd"]:
        fp = DOCS_DIR / f
        if not fp.exists():
            continue
        text = fp.read_text(encoding="utf-8")
        has_ukr = bool(re.search(r"[а-яіїєґА-ЯІЇЄҐ]", text))
        has_eng = bool(re.search(r"[a-zA-Z]", text))
        if has_ukr and has_eng:
            print(f"  [OK] docs/{f} містить як англійські терміни/ідентифікатори, так і україномовні описи")
        else:
            print(f"  [WARN/FAIL] docs/{f}: Ukrainian={has_ukr}, English={has_eng}")
            all_ok = False

    return all_ok


def main():
    print("================================================================")
    print("  МАЙСТЕР-ВЕРИФІКАЦІЯ АРТЕФАКТІВ МОДЕЛЮВАННЯ (SC-001 - SC-006)")
    print("================================================================")

    sc001 = check_sc001_presence_and_encoding()
    sc002 = check_sc002_diagram_syntax()
    sc003 = check_sc003_class_relationships()
    sc004 = check_sc004_behavior_consistency()
    sc005 = check_sc005_crc_cards()
    sc006 = check_sc006_bilingual_compliance()

    print("\n================================================================")
    print("                    ПІДСУМОК ВЕРИФІКАЦІЇ                        ")
    print("================================================================")
    results = [
        ("SC-001 (Наявність файлів та UTF-8 без BOM)", sc001),
        ("SC-002 (Синтаксична валідність діаграм)", sc002),
        ("SC-003 (4 типи зв'язків у діаграмі класів)", sc003),
        ("SC-004 (Узгодженість викликів методів та станів)", sc004),
        ("SC-005 (8 заповнених CRC-карток у docs/crc.xlsx)", sc005),
        ("SC-006 (Двомовний стандарт коду та описів)", sc006),
    ]

    total_pass = True
    for name, status in results:
        status_str = "[PASS]" if status else "[FAIL]"
        print(f"  {status_str} {name}")
        if not status:
            total_pass = False

    print("================================================================")
    if total_pass:
        print("  РЕЗУЛЬТАТ: УСІ КРИТЕРІЇ УСПІШНО ВИКОНАНО!")
        print("================================================================")
        return 0
    else:
        print("  РЕЗУЛЬТАТ: ВИЯВЛЕНО НЕВИКОНАНІ КРИТЕРІЇ АБО ВІДСУТНІ АРТЕФАКТИ.")
        print("================================================================")
        return 1


if __name__ == "__main__":
    sys.exit(main())
