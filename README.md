# プレゼン練習アプリ

## 開発環境の起動方法

1.  Docker Desktopをインストール・起動してください。
2.  ターミナルで以下のコマンドを実行します。

```bash
docker-compose up --build
```

3.  ブラウザで以下のURLにアクセスしてください。
    -   フロントエンド: `http://localhost:5173`
    -   バックエンド (API): `http://localhost:8000`

## Tailwind CSSの初期設定

### 1. Tailwind CSS CLIのインストール（推奨方法）

```bash
cd frontend
npm install -D tailwindcss
npx tailwindcss init
```

### 2. tailwind.config.jsの設定

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{html,js,ts,jsx,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### 3. CSSファイルにTailwindディレクティブを追加

`src/index.css`の先頭に以下を追加：

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### 4. 動作確認

Viteサーバーを再起動後、コンポーネントでTailwindクラス（例：`className="bg-blue-500 text-white"`）が適用されることを確認してください。

**注意**: Viteを使用している場合、PostCSSやAutoprefixerは不要です。Viteが自動的に処理します。

## Git SSH鍵の生成方法

1. ターミナルで以下のコマンドを実行し、SSH鍵（公開鍵と秘密鍵）を生成します。

    ```bash
    ssh-keygen -t ed25519 -C "your_email@example.com"
    ```

    ※ 途中で保存場所やパスフレーズを聞かれた場合は、必要に応じて入力してください。

2. 公開鍵の内容をクリップボードにコピーします。

    ```bash
    cat ~/.ssh/id_ed25519.pub
    ```

3. GitHub等のリモートリポジトリサービスの「SSH Keys」設定画面で、公開鍵を登録してください。

## SSH鍵設定の確認方法

1. ターミナルで以下のコマンドを実行します。

    ```bash
    ssh -T git@github.com
    ```

2. 初回接続時は「Are you sure you want to continue connecting (yes/no/[fingerprint])?」と表示される場合があります。その場合は `yes` と入力してください。

3. 「Hi ユーザー名! You've successfully authenticated...」のようなメッセージが表示されれば、SSH鍵の設定は成功です。

## リモートリポジトリ接続確認方法

1. ターミナルで以下のコマンドを実行します。

    ```bash
    git remote add origin リポジトリURL
    git remote -v
    ```

    登録されているリモートリポジトリのURLが表示されます。

2. 実際にリモートリポジトリへ接続できるか確認するには、以下のコマンドを実行します。

    ```bash
    git ls-remote
    ```

    エラーが出なければ、リモートリポジトリに正常に接続できています。