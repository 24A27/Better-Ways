import { useState } from 'react'
import './App.css'

interface AnalysisResult {
  transcript: string;
  content_feedback: string;
  total_words: number;
  duration_seconds: number;
  average_wpm: number;
  filler_count: number;
  filler_words: string[];
  used_provider: string;
}

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string>('');
  const [llmProvider, setLlmProvider] = useState<'openai' | 'google'>('openai');

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setError('');
      setAnalysisResult(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('ファイルを選択してください');
      return;
    }

    setIsAnalyzing(true);
    setError('');

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('provider', llmProvider);

      const response = await fetch('http://localhost:8000/api/analyze-speech', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result: AnalysisResult = await response.json();
      setAnalysisResult(result);
    } catch (err) {
      setError(`分析中にエラーが発生しました: ${err instanceof Error ? err.message : '不明なエラー'}`);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const formatDuration = (seconds: number) => {
    const minutes = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${minutes}分${secs}秒`;
  };

  return (
    <div className="container">
      <header>
        <h1>🎤 Better Ways - 話し方分析ツール</h1>
        <p>音声ファイルをアップロードして、話の内容と話し方を分析します</p>
      </header>

      <div className="upload-section">
        <div className="provider-selection">
          <h3>🤖 LLMプロバイダー選択</h3>
          <div className="provider-options">
            <label className="provider-option">
              <input
                type="radio"
                name="provider"
                value="openai"
                checked={llmProvider === 'openai'}
                onChange={(e) => setLlmProvider(e.target.value as 'openai' | 'google')}
              />
              <span>OpenAI (GPT-4o)</span>
            </label>
            <label className="provider-option">
              <input
                type="radio"
                name="provider"
                value="google"
                checked={llmProvider === 'google'}
                onChange={(e) => setLlmProvider(e.target.value as 'openai' | 'google')}
              />
              <span>Google Gemini</span>
            </label>
          </div>
        </div>

        <div className="file-input-wrapper">
          <input
            type="file"
            accept="audio/*"
            onChange={handleFileSelect}
            disabled={isAnalyzing}
            id="audio-file"
          />
          <label htmlFor="audio-file" className="file-input-label">
            📁 音声ファイルを選択
          </label>
        </div>
        
        {selectedFile && (
          <div className="selected-file">
            <p>選択されたファイル: <strong>{selectedFile.name}</strong></p>
            <button 
              onClick={handleUpload} 
              disabled={isAnalyzing}
              className="analyze-button"
            >
              {isAnalyzing ? '分析中...' : '🚀 分析開始'}
            </button>
          </div>
        )}
      </div>

      {error && (
        <div className="error">
          ❌ {error}
        </div>
      )}

      {analysisResult && (
        <div className="results">
          <h2>📊 分析結果</h2>
          
          <div className="result-section">
            <h3>🎯 基本情報</h3>
            <div className="stats-grid">
              <div className="stat-item">
                <span className="stat-label">使用プロバイダー:</span>
                <span className="stat-value">{analysisResult.used_provider === 'openai' ? 'OpenAI (GPT-4o)' : 'Google Gemini'}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">録音時間:</span>
                <span className="stat-value">{formatDuration(analysisResult.duration_seconds)}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">総単語数:</span>
                <span className="stat-value">{analysisResult.total_words}語</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">平均話速:</span>
                <span className="stat-value">{analysisResult.average_wpm} WPM</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">フィラー語数:</span>
                <span className="stat-value">{analysisResult.filler_count}回</span>
              </div>
            </div>
          </div>

          <div className="result-section">
            <h3>📝 文字起こし</h3>
            <div className="transcript">
              {analysisResult.transcript}
            </div>
          </div>

          <div className="result-section">
            <h3>💡 内容の評価・フィードバック</h3>
            <div className="feedback">
              {analysisResult.content_feedback}
            </div>
          </div>

          {analysisResult.filler_words.length > 0 && (
            <div className="result-section">
              <h3>🔍 検出されたフィラー語</h3>
              <div className="filler-words">
                {analysisResult.filler_words.map((word, index) => (
                  <span key={index} className="filler-word">{word}</span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default App
