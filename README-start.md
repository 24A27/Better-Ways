# 🎤 Better Ways - 音声分析ツール 起動ガイド

このプロジェクトは**音声ファイルをアップロードして話し方を分析するWebアプリケーション**です。

## 📋 必要な環境

### システム要件
- **Docker Desktop** (推奨)
- **Git** (リポジトリのクローン用)
- **macOS / Windows / Linux**
- **ブラウザ** (Chrome, Firefox, Safari, Edge)

### APIキー（必須）
以下のいずれかまたは両方のAPIキーが必要です：
- **OpenAI API Key** - 音声認識（Whisper）とテキスト分析（GPT-4o）
- **Google API Key** - テキスト分析（Gemini）用

## 🚀 セットアップ手順

### 0. リポジトリのクローン（初回のみ）
```bash
# GitHubからプロジェクトをクローン
git clone [リポジトリURL]

# プロジェクトディレクトリに移動
cd betterWays
```

### 1. プロジェクトの準備
```bash
# ファイル構成確認
ls -la
# 以下のファイルがあることを確認：
# - docker-compose.yml
# - .env.example
# - backend/
# - frontend/
```

### 2. 環境変数の設定
```bash
# .envファイルを作成
cp .env.example .env

# .envファイルを編集
nano .env
# または
code .env
```

**.envファイルの設定例:**
```env
# 使用するLLMプロバイダーを指定 ('google' or 'openai')
LLM_PROVIDER=openai

# Google Gemini API Key（Googleを使用する場合）
GOOGLE_API_KEY=your_google_api_key_here

# OpenAI API Key（音声認識とGPT分析用）
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. APIキーの取得方法

#### OpenAI API Key
1. [OpenAI Platform](https://platform.openai.com/) にアクセス
2. アカウント作成・ログイン
3. 「API Keys」→「Create new secret key」
4. 生成されたキーを`.env`ファイルに設定

#### Google API Key
1. [Google AI Studio](https://aistudio.google.com/) にアクセス
2. Googleアカウントでログイン
3. 「Get API Key」をクリック
4. 生成されたキーを`.env`ファイルに設定

### 4. アプリケーションの起動
```bash
# Docker Desktopが起動していることを確認

# アプリケーションをビルド・起動（初回または更新時）
docker-compose up --build

# またはバックグラウンド起動
docker-compose up --build -d
```

**🎉 これで起動完了！**
- **フロントエンド**: http://localhost:5173
- **バックエンドAPI**: http://localhost:8000/health

## 🔄 日常的な起動・停止

### 2回目以降の起動
```bash
# 通常の起動（ビルド不要）
docker-compose up

# バックグラウンド起動
docker-compose up -d
```

### 停止
```bash
# 停止
docker-compose down

# 完全停止（ボリュームも削除）
docker-compose down --volumes
```

## 💻 ローカル開発環境（オプション）

### VSCodeでの開発体験を向上させたい場合
```bash
# フロントエンドの依存関係をローカルにインストール
cd frontend
npm install

# バックエンドの依存関係をローカルにインストール
cd ../backend
pip install -r requirements.txt
```

**メリット:**
- VSCodeでコード補完が正常に動作
- エラー表示がリアルタイムで表示  
- IntelliSenseが使える
- より高速なデバッグが可能

**注意:** ローカル環境は開発体験向上のためのオプションです。アプリケーションの実行は引き続きDockerを使用してください。

### 5. 動作確認
ブラウザで以下のURLにアクセス：
- **フロントエンド**: http://localhost:5173
- **バックエンドAPI**: http://localhost:8000/health

## 🎯 使用方法

### 基本的な使い方
1. **プロバイダー選択**: OpenAI または Google Gemini を選択
2. **ファイルアップロード**: 音声ファイル（MP3, WAV, M4A）を選択
3. **分析開始**: 「🚀 分析開始」ボタンをクリック
4. **結果確認**: 文字起こし、分析結果、フィードバックを確認

### 分析結果の内容
- **📝 文字起こし**: 音声の完全なテキスト化
- **📊 基本情報**: 録音時間、単語数、話速（WPM）
- **💡 フィードバック**: 話の構成、論理性、改善点
- **🔍 フィラー語検出**: 「えー」「あー」などの検出

## 🛠️ トラブルシューティング

### よくある問題と解決方法

#### 1. Dockerが起動しない
```bash
# Docker Desktopが起動していることを確認
docker --version

# Dockerサービスを再起動
# macOS: Docker Desktopアプリを再起動
# Windows: Docker Desktopアプリを再起動
```

#### 2. APIキーエラー
```bash
# APIキーが正しく設定されているか確認
cat .env

# 環境変数が読み込まれているか確認
docker-compose exec backend python -c "import os; print('OPENAI:', 'SET' if os.getenv('OPENAI_API_KEY') else 'NOT SET')"
```

#### 3. ポートエラー
```bash
# ポートが使用中の場合、他のアプリケーションを停止
# または docker-compose.yml でポート番号を変更

# 現在使用中のポートを確認
lsof -i :5173
lsof -i :8000
```

#### 4. ファイルアップロードエラー
- **ファイル形式**: MP3, WAV, M4A のみサポート
- **ファイルサイズ**: 25MB以下推奨
- **音声品質**: クリアな音声ほど正確な分析が可能

### ログ確認
```bash
# 全体のログ確認
docker-compose logs

# バックエンドのみ
docker-compose logs backend

# フロントエンドのみ
docker-compose logs frontend

# リアルタイムログ
docker-compose logs -f
```

## 🔄 運用コマンド

### 基本コマンド
```bash
# 起動
docker-compose up -d

# 停止
docker-compose down

# 再起動
docker-compose restart

# 強制再ビルド
docker-compose up --build --force-recreate

# ログ確認
docker-compose logs -f

# 状態確認
docker-compose ps
```

### 開発用コマンド
```bash
# 特定のサービスのみ再起動
docker-compose restart backend
docker-compose restart frontend

# コンテナ内部にアクセス
docker-compose exec backend bash
docker-compose exec frontend sh

# データベース/キャッシュクリア
docker-compose down --volumes
```

## 💡 使用上の注意

### セキュリティ
- **APIキーの保護**: `.env`ファイルを他人に共有しない
- **Gitリポジトリ**: `.env`ファイルはGitにコミットしない

### 料金について
- **OpenAI**: 使用量に応じた従量課金
- **Google Gemini**: 無料枠あり、その後従量課金
- **使用量管理**: 長時間の音声ファイルは料金が高くなる可能性

### パフォーマンス
- **推奨ファイルサイズ**: 5分以内の音声
- **同時実行**: 大量のファイルを一度に処理しない
- **ネットワーク**: 安定したインターネット接続が必要

## 📚 機能詳細

### サポートする音声形式
- **MP3**: 最も一般的な形式
- **WAV**: 高品質、ファイルサイズ大
- **M4A**: Apple製品でよく使用

### 分析項目
- **文字起こし精度**: 日本語・英語対応
- **話速計算**: WPM（Words Per Minute）
- **フィラー語検出**: 15種類以上のパターン
- **内容分析**: 論理構成、説得力、改善提案

### プロバイダー比較
| 項目 | OpenAI | Google Gemini |
|------|--------|---------------|
| 音声認識 | Whisper（高精度） | 未対応※ |
| テキスト分析 | GPT-4o | Gemini 1.5 |
| 料金 | 従量課金 | 無料枠あり |
| 応答速度 | 速い | 非常に速い |

※現在Googleプロバイダーでも音声認識はOpenAI Whisperを使用

## 🆘 サポート

### 問題が解決しない場合
1. **ログ確認**: `docker-compose logs`でエラー内容を確認
2. **再起動**: `docker-compose down && docker-compose up --build`
3. **環境確認**: Docker Desktop、APIキーの設定を再確認
4. **ファイル確認**: 音声ファイルの形式・サイズを確認

### システム要件の再確認
- Docker Desktop: 最新版
- Git: 最新版
- メモリ: 4GB以上推奨
- ストレージ: 2GB以上の空き容量
- ネットワーク: 安定したインターネット接続

---

## 🎉 完了！

これで音声分析ツールが使用できます。
**URL**: http://localhost:5173 でアクセスして、音声ファイルをアップロードしてお試しください！

**開発・カスタマイズが必要な場合は、フロントエンド（React）とバックエンド（FastAPI）のコードを確認してください。**
