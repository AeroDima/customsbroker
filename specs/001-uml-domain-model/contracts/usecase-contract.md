# Контракт інтерфейсу: Діаграма прецедентів (`docs/usecase.puml`)

**Feature**: `001-uml-domain-model` | **Цільовий артефакт**: `docs/usecase.puml`  
**Формат**: PlantUML (`.puml`) | **Кодування**: UTF-8 (без BOM)

---

## 1. Загальні вимоги до файлу

1. Файл повинен починатися з директиви `@startuml` та завершуватися директивою `@enduml`.
2. Діаграма повинна містити директиву `left to right direction` для ергономічного горизонтального розташування акторів та прецедентів.
3. Усі зовнішні дійові особи (актори) повинні знаходитися поза межами системної рамки.
4. Усі сценарії використання (прецеденти) повинні бути згруповані всередині рамки меж системи `rectangle "Система автоматизації діяльності митного брокера (CustomsBroker)"`.

---

## 2. Специфікація дійових осіб (Actors)

| Ідентифікатор актора | Відображення на діаграмі | Тип актора | Опис ролі |
|---|---|---|---|
| `Importer` | `actor "Імпортер\n(Importer)" as Importer` | Первинний бізнес-актор | Суб'єкт ЗЕД, ініціює подання документів та сплату |
| `CustomsBroker` | `actor "Митний брокер\n(CustomsBroker)" as CustomsBroker` | Внутрішній фахівець | Представник, декларант, складає декларацію, рахує збори |
| `CustomsInspector` | `actor "Митний інспектор\n(CustomsInspector)" as CustomsInspector` | Зовнішній регуляторний актор | Посадова особа митного органу, контролює та випускає вантаж |

---

## 3. Специфікація прецедентів (Use Cases)

| ID | Назва прецеденту в діаграмі | Аліас у PlantUML | Зв'язані актори |
|---|---|---|---|
| UC-1 | `Подати пакет документів на оформлення` | `UC_SubmitDocs` | `Importer` |
| UC-2 | `Перевірити пакет товаросупровідних документів` | `UC_VerifyDocs` | `CustomsBroker` |
| UC-3 | `Скласти митну декларацію` | `UC_DraftDeclaration` | `CustomsBroker` |
| UC-4 | `Класифікувати товар за УКТЗЕД` | `UC_ClassifyItem` | `CustomsBroker` |
| UC-5 | `Розрахувати суму митних платежів` | `UC_CalculateDuties` | `CustomsBroker` |
| UC-6 | `Застосувати пільгову ставку / преференцію` | `UC_ApplyPreference` | `CustomsBroker` |
| UC-7 | `Призначити та провести форму митного контролю` | `UC_AssignInspection` | `CustomsInspector` |
| UC-8 | `Сплатити мито та збори` | `UC_PayDuties` | `Importer`, `CustomsBroker` |
| UC-9 | `Прийняти рішення про випуск вантажу` | `UC_ReleaseCargo` | `CustomsInspector` |
| UC-10 | `Надати відмову у митному оформленні` | `UC_RejectCargo` | `CustomsInspector` |

---

## 4. Специфікація стереотипів та зв'язків між прецедентами

1. **`<<include>>` (Обов'язкове включення)**:
   - `(UC_DraftDeclaration) ..> (UC_ClassifyItem) : <<include>>` (складання декларації обов'язково потребує класифікації товарів за УКТЗЕД).
   - `(UC_DraftDeclaration) ..> (UC_CalculateDuties) : <<include>>` (складання декларації обов'язково включає нарахування платежів).
2. **`<<extend>>` (Умовне розширення)**:
   - `(UC_ApplyPreference) ..> (UC_CalculateDuties) : <<extend>>` (застосування преференції розширює розрахунок за наявності сертифіката походження).
   - `(UC_RejectCargo) ..> (UC_AssignInspection) : <<extend>>` (відмова формується у разі виявлення порушень під час контролю).
3. **Асоціації з акторами**:
   - `Importer --> UC_SubmitDocs`
   - `Importer --> UC_PayDuties`
   - `CustomsBroker --> UC_VerifyDocs`
   - `CustomsBroker --> UC_DraftDeclaration`
   - `CustomsBroker --> UC_PayDuties`
   - `CustomsInspector --> UC_AssignInspection`
   - `CustomsInspector --> UC_ReleaseCargo`
   - `CustomsInspector --> UC_RejectCargo`
