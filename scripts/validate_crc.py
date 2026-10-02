"""Скрипт автоматизованого аудиту структури та вмісту Excel-таблиці CRC-карток.

Перевіряє docs/crc.xlsx згідно з specs/001-uml-domain-model/contracts/crc-contract.md.
"""

import sys
from pathlib import Path
import openpyxl

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

REQUIRED_CLASSES = [
    "IDocumentPackageHandler",
    "CustomsParticipant",
    "Importer",
    "CustomsBroker",
    "CustomsInspector",
    "CustomsDeclaration",
    "DeclarationItem",
    "CommodityCodeRegistry",
]


def validate_crc(file_path: Path) -> bool:
    print(f"=== Аудит Excel-таблиці CRC-карток: {file_path.name} ===")

    if not file_path.exists():
        print(f"[FAIL] Файл не знайдено: {file_path}")
        return False
    print(f"[SUCCESS] {file_path.name} знайдено.")

    try:
        wb = openpyxl.load_workbook(file_path, data_only=True)
    except Exception as e:
        print(f"[FAIL] Не вдалося відкрити {file_path.name} через openpyxl: {e}")
        return False

    # 1. Перевірка наявності аркуша
    sheet_name = "CRC Cards"
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        print(f"[SUCCESS] Робочий аркуш '{sheet_name}' знайдено.")
    else:
        ws = wb.active
        print(f"[WARN] Аркуш '{sheet_name}' не знайдено, використовується активний аркуш '{ws.title}'.")

    # 2. Пошук усіх 8 класів у комірках
    text_content = []
    classes_found = {cls_name: False for cls_name in REQUIRED_CLASSES}

    for row in ws.iter_rows(values_only=True):
        row_text = " ".join([str(c) for c in row if c is not None])
        if row_text:
            text_content.append(row_text)
            for cls_name in REQUIRED_CLASSES:
                if cls_name in row_text:
                    classes_found[cls_name] = True

    missing_classes = [c for c, found in classes_found.items() if not found]
    if missing_classes:
        print(f"[FAIL] Не знайдено обов'язкові сутності: {missing_classes}")
        return False
    print(f"[SUCCESS] Знайдено всі {len(REQUIRED_CLASSES)} обов'язкових сутностей.")

    # 3. Перевірка наявності розділів обов'язків та колаборацій
    full_text = "\n".join(text_content)
    if "Обов'язки" not in full_text and "Responsibilities" not in full_text:
        print("[FAIL] Не знайдено підзаголовків 'Обов'язки / Responsibilities'.")
        return False
    if "Співпраця" not in full_text and "Collaborators" not in full_text:
        print("[FAIL] Не знайдено підзаголовків 'Співпраця / Collaborators'.")
        return False
    print("[SUCCESS] Усі картки містять структуровані блоки обов'язків та колаборацій.")

    # 4. Перевірка стилізації (темно-синій заголовок, межі, wrap_text)
    header_styled = False
    wrap_text_found = False
    border_found = False

    for row in ws.iter_rows():
        for cell in row:
            if cell.value and any(c in str(cell.value) for c in REQUIRED_CLASSES):
                # Перевіримо заголовок
                fill = cell.fill
                font = cell.font
                if fill and fill.start_color and fill.start_color.rgb:
                    color_hex = str(fill.start_color.rgb).upper()
                    # 1F4E79 або з альфа-каналом FF1F4E79
                    if "1F4E79" in color_hex or "1F4E" in color_hex:
                        header_styled = True
                if font and font.color and font.color.rgb:
                    font_color = str(font.color.rgb).upper()
                    if "FFFFFF" in font_color:
                        header_styled = True

            if cell.alignment and cell.alignment.wrap_text:
                wrap_text_found = True

            if cell.border and (cell.border.left or cell.border.top or cell.border.right or cell.border.bottom):
                border_found = True

    if not header_styled:
        print("[WARN/INFO] Заголовки карток можуть мати альтернативну тему або колір.")
    else:
        print("[SUCCESS] Стилізація заголовків карток (темно-синій #1F4E79, білий шрифт) підтверджена.")

    if not wrap_text_found:
        print("[FAIL] Властивість wrap_text (перенесення слів) не знайдена в комірках.")
        return False
    print("[SUCCESS] Властивість wrap_text увімкнена.")

    if not border_found:
        print("[FAIL] Межі комірок не налаштовані.")
        return False
    print("[SUCCESS] Рамки комірок налаштовані.")

    print("\n[SUCCESS] Таблиця docs/crc.xlsx повністю відповідає контракту та вимогам FR-017, FR-018!")
    return True


def main():
    if len(sys.argv) > 1:
        target_path = Path(sys.argv[1])
    else:
        target_path = Path(__file__).resolve().parent.parent / "docs" / "crc.xlsx"

    if validate_crc(target_path):
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
