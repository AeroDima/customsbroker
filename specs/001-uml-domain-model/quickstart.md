# Інструкція швидкого запуску та валідації артефактів (Quickstart Validation Guide)

**Feature**: `001-uml-domain-model` | **Дата**: 2026-10-02  
**Статус**: Затверджено (Phase 1)

Цей посібник містить чіткі інструкції для автономної перевірки, рендерингу та тестування артефактів моделювання (UML-діаграм та таблиці CRC-карток) виключно за допомогою стандартного інтерфейсу командного рядка (CLI).

---

## 1. Попередні вимоги (Prerequisites)

Перед запуском перевірок переконайтеся у наявності таких інструментів у системі:

- **Node.js** (з утилітою `npx`): для валідації та візуалізації Mermaid-діаграм через `@mermaid-js/mermaid-cli`.
- **Python 3.11+** (з бібліотекою `openpyxl`): для генерації та аудиту таблиці `docs/crc.xlsx`.
- **PowerShell / Bash**: для запуску сценаріїв перевірки.

Перевірка готовності середовища:
```powershell
node --version
python --version
python -c "import openpyxl; print('openpyxl: OK')"
```

---

## 2. Сценарії валідації артефактів

### Сценарій 1: Генерація та аудит CRC-карток (`docs/crc.xlsx`)

**Мета**: Перевірити формування повноцінної Excel-таблиці з 8 сутностями згідно з [crc-contract.md](file:///F:/Projects/customsbroker/specs/001-uml-domain-model/contracts/crc-contract.md).

1. **Команда генерації**:
   ```powershell
   python scripts/generate_crc.py
   ```
   *Очікуваний результат*: Створено файл `docs/crc.xlsx` з 8 стилізованими картками.

2. **Команда автоматизованого аудиту**:
   ```powershell
   python scripts/validate_crc.py
   ```
   *Очікуваний результат*:
   ```text
   [SUCCESS] docs/crc.xlsx знайдено.
   [SUCCESS] Знайдено всі 8 обов'язкових сутностей.
   [SUCCESS] Усі картки містять непорожні обов'язки та колабораторів.
   [SUCCESS] Форматування та структура відповідають специфікації.
   ```

---

### Сценарій 2: Валідація синтаксису діаграми класів (`docs/class.mmd`)

**Мета**: Перевірити валідність синтаксису Mermaid та відповідність вимогам [class-diagram-contract.md](file:///F:/Projects/customsbroker/specs/001-uml-domain-model/contracts/class-diagram-contract.md).

**Команда**:
```powershell
npx -y @mermaid-js/mermaid-cli -i docs/class.mmd -o docs/class.svg
```
*Очікуваний результат*: Команда завершується з кодом 0, згенеровано валідний векторний файл `docs/class.svg`.

---

### Сценарій 3: Валідація діаграми послідовності (`docs/sequence.mmd`)

**Мета**: Перевірити валідність синтаксису Mermaid та зв'язок викликів із методами класів згідно з [sequence-diagram-contract.md](file:///F:/Projects/customsbroker/specs/001-uml-domain-model/contracts/sequence-diagram-contract.md).

**Команда**:
```powershell
npx -y @mermaid-js/mermaid-cli -i docs/sequence.mmd -o docs/sequence.svg
```
*Очікуваний результат*: Команда завершується з кодом 0, згенеровано `docs/sequence.svg`.

---

### Сценарій 4: Валідація діаграми станів (`docs/state.mmd`)

**Мета**: Перевірити валідність скінченного автомата згідно з [state-diagram-contract.md](file:///F:/Projects/customsbroker/specs/001-uml-domain-model/contracts/state-diagram-contract.md).

**Команда**:
```powershell
npx -y @mermaid-js/mermaid-cli -i docs/state.mmd -o docs/state.svg
```
*Очікуваний результат*: Команда завершується з кодом 0, згенеровано `docs/state.svg`.

---

### Сценарій 5: Валідація діаграми варіантів використання (`docs/usecase.puml`)

**Мета**: Перевірити наявність меж системи, 3 акторів, обов'язкових прецедентів та зв'язків згідно з [usecase-contract.md](file:///F:/Projects/customsbroker/specs/001-uml-domain-model/contracts/usecase-contract.md).

**Команда**:
```powershell
python scripts/validate_plantuml.py docs/usecase.puml
```
*Очікуваний результат*:
```text
[SUCCESS] docs/usecase.puml має коректне кодування UTF-8 без BOM.
[SUCCESS] Директиви @startuml та @enduml присутні.
[SUCCESS] Знайдено акторів: Importer, CustomsBroker, CustomsInspector.
[SUCCESS] Системна рамка та ключові прецеденти присутні.
```

---

### Сценарій 6: Наскрізна верифікація всіх критеріїв якості (SC-001 - SC-006)

**Мета**: Запустити єдиний майстер-тест, який перевіряє виконання всіх критеріїв успішності.

**Команда**:
```powershell
python scripts/verify_artifacts.py
```
*Очікуваний результат*:
```text
=== ПЕРЕВІРКА КРИТЕРІЇВ УСПІШНОСТІ (SC-001 - SC-006) ===
[PASS] SC-001: Усі 5 цільових файлів присутні в каталозі docs/
[PASS] SC-002: Усі UML-діаграми успішно компілюються парсерами
[PASS] SC-003: 4 типи зв'язків присутні на діаграмі класів (<|--, <|.., *--, ..>)
[PASS] SC-004: Методи діаграми послідовності та стани узгоджені з моделлю даних
[PASS] SC-005: docs/crc.xlsx містить 8 заповнених карток згідно з CRC-стандартом
[PASS] SC-006: Англійськомовний код та україномовні описи/документація
=== РЕЗУЛЬТАТ: УСІ КРИТЕРІЇ УСПІШНО ВИКОНАНО ===
```
