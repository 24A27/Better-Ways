// Express + Gemini(OpenAI) APIサンプル
// 必要なパッケージ: express, axios, dotenv
// .envにAPIキーを記載してください

const express = require('express');
const axios = require('axios');
require('dotenv').config();

const app = express();
const PORT = 8000;

// Google Gemini API呼び出し関数
async function callGemini(role, prompt) {
  const apiKey = process.env.GOOGLE_API_KEY;
  if (!apiKey) return { error: 'Google Gemini APIキーがありません' };
  try {
    const url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=' + apiKey;
    const sysPrompt = role ? `You are a ${role}.` : '';
    const res = await axios.post(url, {
      contents: [
        { role: 'user', parts: [{ text: sysPrompt }, { text: prompt }] }
      ]
    });
    return { response: res.data.candidates[0].content.parts[0].text };
  } catch (e) {
    return { error: e.message };
  }
}

// OpenAI API呼び出し関数
async function callOpenAI(role, prompt) {
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) return { error: 'OpenAI APIキーがありません' };
  try {
    const res = await axios.post('https://api.openai.com/v1/chat/completions', {
      model: 'gpt-4o',
      messages: [
        { role: 'system', content: `You are a ${role}.` },
        { role: 'user', content: prompt }
      ]
    }, {
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
      }
    });
    return { response: res.data.choices[0].message.content };
  } catch (e) {
    return { error: e.message };
  }
}

// GET /ai/:llm/:role/:prompt
app.get('/ai/:llm/:role/:prompt', async (req, res) => {
  const { llm, role, prompt } = req.params;
  if (llm === 'gemini') {
    const result = await callGemini(role, prompt);
    res.json({ llm, role, prompt, ...result });
  } else if (llm === 'openai') {
    const result = await callOpenAI(role, prompt);
    res.json({ llm, role, prompt, ...result });
  } else {
    res.status(400).json({ error: 'llmはopenaiまたはgeminiのみ対応' });
  }
});

app.get('/', (req, res) => {
  res.send('Express LLM API is running!');
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
