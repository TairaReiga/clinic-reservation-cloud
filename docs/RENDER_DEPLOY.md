# Render デプロイ手順（来週水曜用）

このドキュメントに沿えば、Render へワンクリックで本番公開できます。

## 事前準備（デプロイ前日まで）

- [ ] GitHub に最新コードを push 済み
- [ ] [Render](https://render.com/) アカウント作成（**クレジットカード不要**）
- [ ] 使うパスワードを決めておく（`ADMIN_PASSWORD` 用）

## デプロイ手順（約 10 分）

### 1. GitHub を Render に接続

1. [Render Dashboard](https://dashboard.render.com/) にログイン
2. 右上 **New +** → **Blueprint** を選択
3. GitHub アカウントを連携（初回のみ）
4. リポジトリ **`TairaReiga/clinic-reservation-cloud`** を選択
5. Blueprint 名はそのままで **Apply**

### 2. パスワードを設定（必須）

Blueprint 適用画面で **`ADMIN_PASSWORD`** に値を入力する。

| 環境変数 | 設定値 |
|---------|--------|
| `ADMIN_PASSWORD` | 任意の安全なパスワード（例: 自分で決めた12文字以上） |
| `ADMIN_EMAIL` | `admin@example.com`（そのままで OK） |

> `SECRET_KEY` と `DATABASE_URL` は Render が自動設定します。

### 3. デプロイ完了を待つ

- Web サービス + PostgreSQL が自動作成される
- 初回ビルドは **5〜10 分** かかる
- ログに `Deploy live` と出れば完了

### 4. URL を確認

Render Dashboard → **clinic-management-system** → 上部の URL を開く。

例: `https://clinic-management-system.onrender.com`

### 5. 動作確認チェックリスト

- [ ] `/login` が表示される
- [ ] ログインできる（`admin@example.com` + 設定したパスワード）
- [ ] 患者・予約・問い合わせ一覧が表示される
- [ ] 予約詳細 → 日時編集 → 保存できる
- [ ] ログアウト → 再ログインできる
- [ ] `/health` が `{"status":"ok"}` を返す

---

## ログイン情報（本番）

| 項目 | 値 |
|------|-----|
| URL | Render Dashboard に表示される URL |
| メール | `admin@example.com` |
| パスワード | デプロイ時に設定した `ADMIN_PASSWORD` |

---

## 無料プランの注意点

| 項目 | 内容 |
|------|------|
| 料金 | デプロイ直後は **$0** |
| スリープ | 15 分アクセスがないと停止 → 次のアクセスで **30〜60 秒** 起動 |
| PostgreSQL | **30 日後に期限切れ**（デモ・発表用途なら十分） |
| 画像アップロード | 無料 Web では再デプロイ時に消える場合あり |

発表・デモ（来週水曜）なら無料プランで問題ありません。  
継続運用する場合は DB を有料プラン（約 $7/月〜）にアップグレードしてください。

---

## うまくいかないとき

### ビルド失敗

Render Dashboard → **Logs** を確認。  
ローカルで再現する場合:

```bash
cd flask-app
docker compose up --build
```

### ログインできない

- `ADMIN_PASSWORD` が Render の Environment に設定されているか確認
- パスワード変更後は **Manual Deploy** で再デプロイ

### 502 / アプリが起動しない

- ログに `Listening at: http://0.0.0.0:XXXX` が出ているか確認
- `/health` に直接アクセスして 200 か確認

### データベース接続エラー

- `clinic-db` サービスが **Available** になっているか確認
- Web サービスの `DATABASE_URL` が clinic-db にリンクされているか確認

---

## デプロイ後に README を更新

公開 URL が確定したら README の Live App URL を更新:

```markdown
## Live App URL
https://clinic-management-system.onrender.com
```

（実際に Render が割り当てた URL に置き換える）
