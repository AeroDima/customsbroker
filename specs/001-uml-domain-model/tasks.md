---
description: "План декомпозиції завдань для моделювання предметної області (UML та CRC)"
---

# Tasks: Моделювання предметної області системи митного брокера (UML та CRC)

**Input**: Документи проєкту з `specs/001-uml-domain-model/`  
**Prerequisites**: [plan.md](file:///F:/Projects/customsbroker/specs/001-uml-domain-model/plan.md), [spec.md](file:///F:/Projects/customsbroker/specs/001-uml-domain-model/spec.md), [research.md](file:///F:/Projects/customsbroker/specs/001-uml-domain-model/research.md), [data-model.md](file:///F:/Projects/customsbroker/specs/001-uml-domain-model/data-model.md), [contracts/](file:///F:/Projects/customsbroker/specs/001-uml-domain-model/contracts/), [quickstart.md](file:///F:/Projects/customsbroker/specs/001-uml-domain-model/quickstart.md)  
**Tests**: Валідація синтаксису діаграм через Mermaid CLI (`mmdc`), перевірка синтаксису PlantUML (`scripts/validate_plantuml.py`), аудит Excel CRC-карток (`scripts/validate_crc.py`) та майстер-скрипт верифікації критеріїв успішності SC-001 - SC-006 (`scripts/verify_artifacts.py`).  
**Organization**: Завдання згруповано за користувацькими історіями (User Stories) для забезпечення автономної реалізації та незалежного тестування кожної історії.

## Format: `[ID] [P?] [Story] Description with file path`

- **[P]**: Може виконуватися паралельно (різні файли, відсутність залежностей від незавершених задач)
- **[Story]**: Позначка належності до користувацької історії ([US1], [US2], [US3], [US4])
- Кожен опис містить точний шлях до цільового файлу

## Path Conventions

- `docs/` — цільові артефакти моделювання (`usecase.puml`, `class.mmd`, `sequence.mmd`, `state.mmd`, `crc.xlsx`)
- `scripts/` — допоміжні скрипти генерації, автоматизації та тестування артефактів
- `specs/001-uml-domain-model/` — специфікація, контракти та супровідні документи проєкту

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Ініціалізація структури каталогів проєкту та базових інструментів середовища

- [X] T001 Створити структуру каталогів `docs/` та `scripts/` відповідно до плану архітектури
- [X] T002 Перевірити наявність та ініціалізувати залежності середовища (Node.js/npx, Python 3.11, openpyxl) у корені репозиторію
- [X] T003 [P] Налаштувати правила виключення для тимчасових файлів рендерингу діаграм (`*.svg`, `*.png`) та кешу Python (`__pycache__/`) у файлі `.gitignore`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Базова інфраструктура тестування та валідації, що БЛОКУЄ реалізацію користувацьких історій

**⚠️ CRITICAL**: Усі користувацькі історії спираються на ці скрипти валідації та стандартизацію кодування UTF-8

- [X] T004 Розробити каркас майстер-скрипту валідації `scripts/verify_artifacts.py` з перевіркою наявності файлів (SC-001) та кодування UTF-8 без BOM
- [X] T005 [P] Реалізувати утиліту перевірки синтаксичної валідності Mermaid діаграм через Mermaid CLI (`mmdc`) у `scripts/verify_artifacts.py`

**Checkpoint**: Базова інфраструктура готова — виконання користувацьких історій може розпочинатися

---

## Phase 3: User Story 1 - Моделювання сценаріїв використання митного оформлення (Priority: P1) 🎯 MVP

**Goal**: Розробка формалізованої діаграми варіантів використання (`docs/usecase.puml`) у форматі PlantUML, яка охоплює 3 акторів (`Importer`, `CustomsBroker`, `CustomsInspector`), межі системи та 10 ключових прецедентів зі зв'язками `<<include>>` та `<<extend>>`.

**Independent Test**: Успішне проходження перевірки `python scripts/validate_plantuml.py docs/usecase.puml`, що підтверджує валідність синтаксису PlantUML, наявність усіх 3 акторів, системної рамки та обов'язкових прецедентів.

### Tests for User Story 1

- [X] T006 [P] [US1] Створити скрипт синтаксичної та структурної валідації діаграми PlantUML у `scripts/validate_plantuml.py` згідно з контрактом `specs/001-uml-domain-model/contracts/usecase-contract.md`

### Implementation for User Story 1

- [X] T007 [US1] Оголосити зовнішніх акторів (`Importer`, `CustomsBroker`, `CustomsInspector`) та системну рамку `rectangle` у `docs/usecase.puml`
- [X] T008 [US1] Реалізувати 10 прецедентів (UC-1 - UC-10) та їхні асоціативні зв'язки з акторами у `docs/usecase.puml`
- [X] T009 [US1] Додати обов'язкові стереотипи `<<include>>` (для класифікації та нарахування мита) та `<<extend>>` (для преференцій та відмови) у `docs/usecase.puml`
- [X] T010 [US1] Виконати синтаксичну верифікацію діаграми прецедентів за допомогою `scripts/validate_plantuml.py`

**Checkpoint**: Діаграма прецедентів повністю функціональна, відповідає контракту та валідується автономно (MVP готовий)

---

## Phase 4: User Story 2 - Структурне моделювання об'єктної моделі предметної області (Priority: P2)

**Goal**: Побудова діаграми класів у форматі Mermaid (`docs/class.mmd`) для 8 сутностей предметної області (+ `DocumentPackage`), з відображенням поліморфізму, `final` методу `getParticipantInfo()`, перевантажених методів `calculateDuties` та 4 типів об'єктних зв'язків згідно з принципами SOLID.

**Independent Test**: Успішна компіляція діаграми класів за допомогою команди `npx -y @mermaid-js/mermaid-cli -i docs/class.mmd -o docs/class.svg` та підтвердження наявності всіх класів, атрибутів, методів і 4 типів зв'язків.

### Implementation for User Story 2

- [X] T011 [P] [US2] Оголосити інтерфейс `IDocumentPackageHandler` та абстрактний клас `CustomsParticipant` із захищеними полями, конструктором та `final` методом `getParticipantInfo()$` у `docs/class.mmd`
- [X] T012 [P] [US2] Оголосити класи учасників `Importer`, `CustomsBroker` та `CustomsInspector` з унікальними полями, конструкторами та перевизначеним `processDocumentPackage()` у `docs/class.mmd`
- [X] T013 [P] [US2] Оголосити сутності `CustomsDeclaration` (з перевантаженими методами `calculateDuties`), `DeclarationItem`, `CommodityCodeRegistry` та допоміжну `DocumentPackage` у `docs/class.mmd`
- [X] T014 [US2] Реалізувати 4 обов'язкові типи зв'язків: наслідування (`<|--`), реалізація (`<|..`), строга композиція (`*--`) та залежність (`..>`) у `docs/class.mmd`
- [X] T015 [US2] Виконати синтаксичну компіляцію та генерацію векторного файлу `docs/class.svg` за допомогою Mermaid CLI для валідації `docs/class.mmd`

**Checkpoint**: Діаграма класів повністю сформована, відповідає всім сигнатурам контрактів та успішно візуалізується

---

## Phase 5: User Story 3 - Моделювання динамічної поведінки та життєвого циклу системи (Priority: P3)

**Goal**: Створення узгоджених діаграми послідовності (`docs/sequence.mmd`) з викликами публічних методів об'єктів та діаграми станів (`docs/state.mmd`) з повним життєвим циклом декларації від подання документів до випуску або відмови.

**Independent Test**: Компіляція обох файлів у SVG через Mermaid CLI (`docs/sequence.svg`, `docs/state.svg`) та верифікація 100% узгодженості викликів методів із діаграмою класів `docs/class.mmd`.

### Implementation for User Story 3

- [X] T016 [P] [US3] Оголосити учасників (lifelines), автонумерацію та наскрізний потік викликів публічних методів (1-18) у `docs/sequence.mmd` згідно з контрактом `specs/001-uml-domain-model/contracts/sequence-diagram-contract.md`
- [X] T017 [P] [US3] Оголосити початковий стан `[*]`, робочі стани життєвого циклу декларації та термінальні стани завершення у `docs/state.mmd` згідно з контрактом `specs/001-uml-domain-model/contracts/state-diagram-contract.md`
- [X] T018 [US3] Додати блоки альтернатив `alt`/`else` та активації у `docs/sequence.mmd`, а також переходи у стан відмови `Rejected` із виходом у кінцевий стан `[*]` у `docs/state.mmd`
- [X] T019 [US3] Виконати синтаксичну компіляцію `docs/sequence.mmd` та `docs/state.mmd` за допомогою Mermaid CLI з генерацією файлів `docs/sequence.svg` та `docs/state.svg`

**Checkpoint**: Поведінкова динаміка та кінцевий автомат життєвого циклу повністю узгоджені зі структурною моделлю класів

---

## Phase 6: User Story 4 - Розподіл обов'язків та колаборацій через CRC-картки (Priority: P4)

**Goal**: Автономна генерація електронної таблиці `docs/crc.xlsx` на базі Python та `openpyxl`, що містить 8 карток сутностей із чітким розподілом обов'язків (SRP), колабораторами та корпоративною стилізацією.

**Independent Test**: Виконання скрипта генерації `python scripts/generate_crc.py` та успішне проходження аудиту `python scripts/validate_crc.py` з перевіркою наявності 8 заповнених карток та коректності стилізації.

### Tests for User Story 4

- [X] T020 [P] [US4] Створити скрипт автоматизованого аудиту структури та вмісту Excel-таблиці CRC-карток у `scripts/validate_crc.py` згідно з контрактом `specs/001-uml-domain-model/contracts/crc-contract.md`

### Implementation for User Story 4

- [X] T021 [US4] Реалізувати генератор `scripts/generate_crc.py` із наповненням даними обов'язків та колабораторів для всіх 8 класів згідно з контрактом
- [X] T022 [US4] Налаштувати візуальне оформлення у `scripts/generate_crc.py`: темно-сині заголовки (`#1F4E79`), білий жирний текст, тонкі рамки, перенесення рядків та автопідбір ширини стовпчиків
- [X] T023 [US4] Згенерувати цільовий файл `docs/crc.xlsx` запуском `scripts/generate_crc.py` та верифікувати його скриптом `scripts/validate_crc.py`

**Checkpoint**: Таблиця `docs/crc.xlsx` створена, стилізована та повністю відповідає вимогам FR-017 та FR-018

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Наскрізна інтеграція, верифікація критеріїв успішності SC-001 - SC-006 та фіналізація документації

- [X] T024 [P] Завершити розробку майстер-скрипту `scripts/verify_artifacts.py` з інтеграцією всіх валідаторів та перевірок SC-001 - SC-006
- [X] T025 Провести повну наскрізну верифікацію всіх артефактів за інструкцією `specs/001-uml-domain-model/quickstart.md` за допомогою команди `python scripts/verify_artifacts.py`
- [X] T026 [P] Оновити документацію та інструкції з перегляду діаграм у `README.md` з дотриманням принципу двомовності (Конституція, Розділ VI)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Не має залежностей — може розпочинатися негайно
- **Foundational (Phase 2)**: Залежить від завершення Setup — БЛОКУЄ реалізацію всіх користувацьких історій
- **User Stories (Phase 3+)**: Залежать від завершення Foundational Phase
  - Користувацькі історії можуть виконуватися послідовно (P1 → P2 → P3 → P4) або паралельно різними розробниками
- **Polish (Phase 7)**: Залежить від виконання всіх бажаних користувацьких історій

### User Story Dependencies

- **User Story 1 (P1)**: Може розпочинатися після Phase 2 — не залежить від інших історій
- **User Story 2 (P2)**: Може розпочинатися після Phase 2 — незалежна, формує модель класів
- **User Story 3 (P3)**: Може розпочинатися після Phase 2 — використовує публічні методи класів із US2 для ліній життя
- **User Story 4 (P4)**: Може розпочинатися після Phase 2 — використовує класи із US2 для переліку обов'язків та колаборацій

### Within Each User Story

- Тести та валідатори (якщо передбачені) створюються до або паралельно з артефактами
- Базові оголошення створюються перед додаванням складних зв'язків
- Артефакт валідується та візуалізується перед переходом до наступного етапу

### Parallel Opportunities

- Завдання фази Setup (T003) може виконуватися паралельно з T001 та T002
- Завдання фази Foundational (T005) може розроблятися паралельно з T004
- Усі тести та валідатори (T006, T020) позначені тегом `[P]` і можуть розроблятися паралельно
- Створення блоків діаграми класів (T011, T012, T013) може відбуватися паралельно
- Створення діаграми послідовності (T016) та діаграми станів (T017) може відбуватися паралельно
- Після завершення Phase 2 усі чотири User Stories можуть виконуватися паралельно різними виконавцями

---

## Parallel Example: User Story 1

```bash
# Розробка валідатора та структури діаграми прецедентів:
Task: "Створити скрипт синтаксичної та структурної валідації діаграми PlantUML у scripts/validate_plantuml.py"
Task: "Оголосити зовнішніх акторів (Importer, CustomsBroker, CustomsInspector) та системну рамку rectangle у docs/usecase.puml"
```

## Parallel Example: User Story 2

```bash
# Паралельне проектування компонентів діаграми класів:
Task: "Оголосити інтерфейс IDocumentPackageHandler та абстрактний клас CustomsParticipant у docs/class.mmd"
Task: "Оголосити класи учасників Importer, CustomsBroker та CustomsInspector у docs/class.mmd"
Task: "Оголосити сутності CustomsDeclaration, DeclarationItem, CommodityCodeRegistry та DocumentPackage у docs/class.mmd"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Виконати Phase 1: Setup (створення каталогів `docs/`, `scripts/`)
2. Виконати Phase 2: Foundational (каркас валідації `scripts/verify_artifacts.py`)
3. Виконати Phase 3: User Story 1 (`docs/usecase.puml` + `scripts/validate_plantuml.py`)
4. **ЗУПИНИТИСЯ ТА ПЕРЕВІРИТИ**: Провести незалежну перевірку діаграми прецедентів
5. Отримати початковий робочий інкремент (MVP)

### Incremental Delivery

1. Setup + Foundation → Готовність інфраструктури розробки
2. User Story 1 → Формалізація прецедентів та меж системи (MVP)
3. User Story 2 → Формалізація об'єктної структури класів та типів зв'язків
4. User Story 3 → Формалізація динаміки викликів та станів життєвого циклу
5. User Story 4 → Формалізація відповідальностей та колаборацій через Excel CRC
6. Polish → Наскрізний запуск `scripts/verify_artifacts.py` з підтвердженням виконання SC-001 - SC-006

### Parallel Team Strategy

За наявності кількох розробників:
- Команда спільно виконує Setup + Foundational (Phase 1 та Phase 2)
- Після проходження чекпойнту:
  - Розробник A: User Story 1 (`docs/usecase.puml`)
  - Розробник B: User Story 2 (`docs/class.mmd`)
  - Розробник C: User Story 3 (`docs/sequence.mmd`, `docs/state.mmd`)
  - Розробник D: User Story 4 (`scripts/generate_crc.py`, `docs/crc.xlsx`)
- Усі історії інтегруються у фінальній фазі через єдиний валідатор `scripts/verify_artifacts.py`

---

## Notes

- Позначка `[P]` = різні файли, відсутність взаємних блокувань
- Мітка `[Story]` гарантує простежуваність (traceability) завдань до вимог у `spec.md`
- Кожна користувацька історія є самостійним завершеним інкрементом, що може тестуватися автономно
- Усі програмні ідентифікатори та сигнатури методів оформлюються англійською мовою, а тексти прецедентів, описів та коментарів — українською (Конституція, Розділ VI)
- Запобігати: нечітким задачам без зазначення шляхів, модифікаціям одного файлу в паралельних задачах, порушенням кодування UTF-8
