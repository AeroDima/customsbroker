# Контракт інтерфейсу: Діаграма класів (`docs/class.mmd`)

**Feature**: `001-uml-domain-model` | **Цільовий артефакт**: `docs/class.mmd`  
**Формат**: Mermaid (`classDiagram`) | **Кодування**: UTF-8 (без BOM)

---

## 1. Загальні вимоги до синтаксису Mermaid

1. Файл починається з ключового слова `classDiagram`.
2. Кожен клас оголошується у явному блоці `class ClassName { ... }`.
3. Для модифікаторів доступу використовуються стандартні позначення:
   - `+` public
   - `-` private
   - `#` protected
4. Стереотипи типів позначаються через:
   - `<<interface>>` для інтерфейсів.
   - `<<abstract>>` для абстрактних класів.
5. Для методів із модифікатором `final` використовується суфікс `$` або чіткий коментар/примітка у Mermaid. Для абстрактних методів використовується суфікс `*`.
6. Обов'язкова присутність конструкторів для створення екземплярів (FR-006).

---

## 2. Перелік сутностей та їх обов'язкові сигнатури

### 2.1. `IDocumentPackageHandler`
- Стереотип: `<<interface>>`
- Методи:
  - `+processDocumentPackage(DocumentPackage pkg) boolean`

### 2.2. `CustomsParticipant`
- Стереотип: `<<abstract>>`
- Поля:
  - `#String id`
  - `#String name`
  - `#String contactEmail`
- Конструктор:
  - `+CustomsParticipant(String id, String name, String contactEmail)`
- Методи:
  - `+getParticipantInfo() String$` (final метод, FR-007)
  - `+processDocumentPackage(DocumentPackage pkg)* boolean` (abstract)
  - `+getId() String`
  - `+getName() String`
  - `+getContactEmail() String`

### 2.3. `Importer`
- Базовий клас: `CustomsParticipant`
- Поля:
  - `-String taxId`
  - `-String companyAddress`
- Конструктор:
  - `+Importer(String id, String name, String contactEmail, String taxId, String companyAddress)`
- Методи:
  - `+processDocumentPackage(DocumentPackage pkg) boolean`
  - `+submitDocuments(CustomsBroker broker, DocumentPackage pkg) void`
  - `+getTaxId() String`
  - `+getCompanyAddress() String`

### 2.4. `CustomsBroker`
- Базовий клас: `CustomsParticipant`
- Поля:
  - `-String licenseNumber`
  - `-double brokerageFeeRate`
- Конструктор:
  - `+CustomsBroker(String id, String name, String contactEmail, String licenseNumber, double brokerageFeeRate)`
- Методи:
  - `+processDocumentPackage(DocumentPackage pkg) boolean`
  - `+createDeclaration(Importer importer, DocumentPackage pkg) CustomsDeclaration`
  - `+classifyItem(CommodityCodeRegistry registry, DeclarationItem item) boolean`
  - `+submitDeclaration(CustomsInspector inspector, CustomsDeclaration declaration) void`
  - `+getLicenseNumber() String`
  - `+getBrokerageFeeRate() double`

### 2.5. `CustomsInspector`
- Базовий клас: `CustomsParticipant`
- Поля:
  - `-String badgeNumber`
  - `-String customsPostCode`
- Конструктор:
  - `+CustomsInspector(String id, String name, String contactEmail, String badgeNumber, String customsPostCode)`
- Методи:
  - `+processDocumentPackage(DocumentPackage pkg) boolean`
  - `+assignInspection(CustomsDeclaration declaration) String`
  - `+verifyDocuments(CustomsDeclaration declaration) boolean`
  - `+releaseCargo(CustomsDeclaration declaration) boolean`
  - `+getBadgeNumber() String`
  - `+getCustomsPostCode() String`

### 2.6. `CustomsDeclaration`
- Поля:
  - `-String declarationNumber`
  - `-String importerId`
  - `-String brokerId`
  - `-String status`
  - `-List~DeclarationItem~ items`
  - `-double totalCustomsValue`
  - `-double totalCalculatedDuty`
  - `-boolean dutyPaid`
- Конструктор:
  - `+CustomsDeclaration(String declarationNumber, String importerId, String brokerId)`
- Методи:
  - `+addItem(DeclarationItem item) void`
  - `+getItems() List~DeclarationItem~`
  - `+calculateDuties(double rate) double` (перевантажений метод 1, FR-009)
  - `+calculateDuties(double rate, double preferentialDiscount) double` (перевантажений метод 2, FR-009)
  - `+validateCommodityCodes(CommodityCodeRegistry registry) boolean`
  - `+markDutiesPaid() void`
  - `+updateStatus(String newStatus) void`
  - `+getStatus() String`
  - `+getTotalCustomsValue() double`
  - `+getTotalCalculatedDuty() double`
  - `+isDutyPaid() boolean`

### 2.7. `DeclarationItem`
- Поля:
  - `-int itemNumber`
  - `-String description`
  - `-String commodityCode`
  - `-double invoiceValue`
  - `-double netWeightKg`
  - `-String originCountry`
- Конструктор:
  - `+DeclarationItem(int itemNumber, String description, String commodityCode, double invoiceValue, double netWeightKg, String originCountry)`
- Методи:
  - `+getItemDetails() String`
  - `+getItemNumber() int`
  - `+getDescription() String`
  - `+getCommodityCode() String`
  - `+getInvoiceValue() double`
  - `+getNetWeightKg() double`
  - `+getOriginCountry() String`

### 2.8. `CommodityCodeRegistry`
- Поля:
  - `-Map~String, Double~ tariffRates`
  - `-Map~String, List~String~~ requiredPermits`
- Конструктор:
  - `+CommodityCodeRegistry()`
- Методи:
  - `+getTariffRate(String code) double`
  - `+validateCodeFormat(String code) boolean`
  - `+getRequiredPermits(String code) List~String~`

### 2.9. `DocumentPackage` (допоміжна сутність)
- Поля:
  - `-String packageId`
  - `-String invoiceNumber`
  - `-String contractNumber`
  - `-boolean hasPackingList`
  - `-boolean hasCertificateOfOrigin`
- Конструктор:
  - `+DocumentPackage(String packageId, String invoiceNumber, String contractNumber)`
- Методи:
  - `+isValidPackage() boolean`
  - `+getPackageId() String`
  - `+getInvoiceNumber() String`
  - `+getContractNumber() String`

---

## 3. Специфікація обов'язкових зв'язків (FR-010)

У файлі `docs/class.mmd` мають бути строго присутні 4 типи зв'язків з відповідним синтаксисом:
1. **Наслідування (`<|--`)**:
   - `CustomsParticipant <|-- Importer`
   - `CustomsParticipant <|-- CustomsBroker`
   - `CustomsParticipant <|-- CustomsInspector`
2. **Реалізація інтерфейсу (`<|..`)**:
   - `IDocumentPackageHandler <|.. CustomsParticipant`
3. **Строга композиція (`*--`)**:
   - `CustomsDeclaration *-- DeclarationItem`
4. **Залежність (`..>`)**:
   - `CustomsDeclaration ..> CommodityCodeRegistry`
   - `CustomsBroker ..> DocumentPackage`
   - `Importer ..> DocumentPackage`
   - `CustomsParticipant ..> DocumentPackage`
