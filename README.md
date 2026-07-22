# clinic-reservation-cloud

小規模クリニック向け 予約・問い合わせ管理クラウドシステム

## Overview（概要）

小規模クリニック向けの「予約・問い合わせ管理クラウドシステム」の実装リポジトリです。  
クラウドプラットフォーム実習Ⅱ（レポート5）で定義した要件に沿って、

- Docker コンテナ上で動作する Flask + SQLite 版（日本語 UI）
- 本番公開は **Render**（Web Service + PostgreSQL）を予定

として、患者・予約・問い合わせを Web ブラウザから一元管理できるように実装しています。

紙の予約帳や電話メモ、Excel に分散している予約・問い合わせ情報を Web アプリに集約し、  
受付業務の効率化と患者満足度の向上を目指します。

---

## Live App URL

| 環境 | URL |
|------|-----|
| ローカル（開発・デモ） | http://localhost:8000 |
| 本番（Render） | デプロイ後に Render が発行する URL（例: `https://clinic-management-system.onrender.com`） |

Render デプロイ手順: [`docs/RENDER_DEPLOY.md`](docs/RENDER_DEPLOY.md)  
システム構成: [`docs/SYSTEM_ARCHITECTURE.md`](docs/SYSTEM_ARCHITECTURE.md)

---

## ログイン情報

| 項目 | 値 |
|------|-----|
| メールアドレス | `admin@example.com`（環境変数 `ADMIN_EMAIL` で変更可） |
| パスワード | 環境変数 `ADMIN_PASSWORD` で設定（ローカル例: `Admin1234!`） |

---

## 機能（日本語 UI）

### 患者管理

- 患者一覧画面（氏名・電話番号、名前検索）
- 患者登録画面

### 予約管理

- 予約一覧（日時・患者名・診療科・担当医・状態、ステータス絞り込み）
- 予約登録／編集（画像アップロード対応）

### 問い合わせ管理

- 問い合わせ一覧（件名・連絡先・状態、ステータス絞り込み）
- 問い合わせ登録／編集（対応メモ）

### 認証

- メール / パスワードログイン
- 未ログイン時は `/login` へリダイレクト

---

## ローカルでの起動方法

### Docker（推奨）

```bash
cd flask-app
cp .env.example .env   # 必要に応じて編集
docker compose up --build
```

→ http://localhost:8000/login

### Python 直接実行

```bash
cd flask-app
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
FLASK_ENV=development python run.py
```

---

## 環境変数

| 変数 | 説明 | デフォルト |
|------|------|-----------|
| `FLASK_ENV` | `development` / `production` | `development` |
| `SECRET_KEY` | セッション暗号化キー | （開発用固定値） |
| `ADMIN_EMAIL` | 管理者メール | `admin@example.com` |
| `ADMIN_PASSWORD` | 管理者パスワード | `Admin1234!` |
| `DATABASE_URL` | PostgreSQL 接続 URL（本番） | SQLite（ローカル） |
| `PORT` | 待ち受けポート | `8000` |

---

## ディレクトリ構成

```
clinic-reservation-cloud/
├── render.yaml              # Render Blueprint 定義
├── docs/
│   ├── SYSTEM_ARCHITECTURE.md
│   ├── RENDER_DEPLOY.md
│   └── implementation.md
└── flask-app/
    ├── app/                 # Flask アプリケーション
    ├── templates/           # Jinja2 テンプレート
    ├── static/              # 静的ファイル・アップロード画像
    ├── config.py
    ├── run.py
    ├── Dockerfile
    └── docker-compose.yml
```

---

## 旧 OutSystems 版

以前の OutSystems Personal Edition 版:  
https://personal-p2heapy9-dev.outsystems.app/ClinicManagementSystem/Login
