# Implementation details(実装の詳細)

## Data model(データモデル)
- Patient（患者）
  - Id (UUID)
  - Name (Text)
  - Phone (Text)
- Reservation（予約）
  - Id (UUID)
  - Patient (Foreign key -> Patient)
  - DateTime (DateTime)
  - Department (Text)
  - Doctor (Text)
  - Status (Enum: Scheduled / Visited / Canceled)
- Inquiry（問い合わせ）
  - Id (UUID)
  - DateTime (DateTime)
  - Subject (Text)
  - PatientNameOrContact (Text)
  - Status (Enum: New / In Progress / Resolved)
  - Notes (Long Text)

## Screens(画面構成)
- Patients
 - 既存患者の一覧表示（Name, Phone）
 - フォームから新規患者を追加（Name, Phone）
 - 
- Reservations
 - 予約一覧を表示（Patient, DateTime, Department, Doctor, Status）
 - ステータスでの絞り込み（Any / Canceled / Scheduled / Visited）
 - 予約の新規作成・編集用ポップアップフォームを開く
   
- Reservation edit（予約編集ポップアップ）
 - 1件分の予約詳細を表示（DateTime, Department, Doctor, Patient, Status）
 - 各項目を更新し、ステータス（Scheduled / Visited / Canceled）を変更可能

- Inquiries
 - 問い合わせ一覧を表示（DateTime, Subject, PatientNameOrContact, Status）
 - ステータスでの絞り込み（Any / New / In Progress / Resolved）
 - 問い合わせの新規作成・編集用ポップアップフォームを開く

- Inquiry edit（問い合わせ編集ポップアップ）
 - 問い合わせの新規作成・編集（DateTime, Subject, PatientNameOrContact, Status, Notes）

## Reservation save flow ,pseudo code(予約保存処理の流れ)
1. ユーザーが予約フォームに（patient, datetime, department, doctor, status）を入力する。
2. Save 実行時：
 - 新規予約の場合：新しい Reservation レコードを作成する。
 - 編集の場合：既存の Reservation レコードを読み込み、各フィールドを更新する。
3. 更新内容をデータベースに保存（コミット）する。
4. 保存後、Reservations 一覧画面にリダイレクトする。
