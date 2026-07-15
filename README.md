#clinic-reservation-cloud ￼
小規模クリニック向け 予約・問い合わせ管理クラウドシステム

##Overview（概要） ￼
OutSystems Personal Edition 上に構築した、小規模クリニック向けの予約・問い合わせ管理クラウドシステム。
患者の予約情報と問い合わせ情報を、1つのクラウドアプリ上で一元管理することを目的としている。

##Live App URL ￼
Clinic Management app（OutSystems）:
https://personal-p2heapy9-dev.outsystems.app/ClinicManagementSystem/Login

ログインには以下のサンプルユーザーを使用する：
- Log in as Matthew Shelton（Admin）
- Log in as Jesse Hernandez（Clinic Staff）

##Features（機能） ￼
- 患者管理（Patient management）
 - 患者一覧（Patients画面）：氏名・電話番号の一覧表示
 - シンプルなフォームからの新規患者登録（Name, Phone）

- 予約管理（Reservation management）
 - 予約一覧：予約日時（DateTime）、患者（Patient）、診療科（Department）、担当医（Doctor）、ステータス（Status）の一覧表示
 - ステータスによる絞り込み（Any / Canceled / Scheduled / Visited）
 - 新規予約登録フォーム（New Reservation）：患者・日時・診療科・担当医・ステータスを入力して予約を作成／編集

- 問い合わせ管理（Inquiry management）
 - 問い合わせ一覧：受付日時（DateTime）、件名（Subject）、患者名または連絡先（PatientNameOrContact）、ステータス（Status）の一覧表示
 - ステータスによる絞り込み（Any / New / In Progress / Resolved）
 - 新規問い合わせ登録フォーム（New Inquiry）：日時・件名・患者／連絡先・ステータス・メモ（Notes）を入力して問い合わせを作成／編集
