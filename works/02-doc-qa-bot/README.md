# 02 · Document Q&A bot · 文档问答机器人

**Maps to service package ② (enterprise knowledge-base bot) · 对应服务包 ②**

## Problem · 问题
Staff keep asking the same questions whose answers are already written down in handbooks and manuals.
员工反复询问的问题，答案其实已经写在手册和制度文件里。

## What it does · 功能
Upload a PDF, ask a question, get an answer that cites the page numbers it came from. If the answer is not in the document, the bot says so instead of guessing.
上传 PDF 后提问，回答会标注引用的页码；文档里没有答案时明确说明，而不是瞎猜。

## Stack · 技术
Python 3.11 · LangChain · vector store · Streamlit · LLM API (DeepSeek or Qwen)

## Run it · 运行
```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt  # add this file when the app is built
copy ..\..\.env.example ..\..\.env   # then fill in your key
streamlit run app.py
```

## Test results · 测试结果
_Fill in after testing._

- Document used: a public document (name + link) · 使用的公开文档
- 20 test questions in `tests/questions.csv` · 20 个测试问题
- Answered correctly: __ / 20 · 答对数
- Every answer shows its source page: yes / no · 每个回答带出处
- Out-of-document questions refused correctly: __ / __ · 文档外问题正确拒答数

## Demo · 演示
_2–3 minute screen recording (no face): link TBD · 2–3 分钟录屏（不露脸）_

## Notes · 备注
Only public or self-written documents are used. · 仅使用公开或自写文档。
