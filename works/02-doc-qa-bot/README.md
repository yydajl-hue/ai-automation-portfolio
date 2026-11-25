# Document Q&A Bot · 企业知识库问答机器人

A bilingual RAG-powered document assistant that answers questions from uploaded PDFs with page-level citations.

基于 RAG（检索增强生成）技术的双语文档问答助手，支持上传 PDF、智能问答及原文页码引用。

## 1. Business Problems · 解决的业务问题

- Employees repeatedly ask the same questions about company documents.
- Searching long manuals and policies takes too much time.
- General AI chatbots may generate unsupported answers.

- 员工反复咨询相同的制度和业务问题。
- 人工查找说明书、规章制度和业务文档耗时较长。
- 普通 AI 聊天机器人可能生成缺乏原文依据的答案。

## 2. Features · 核心功能

- PDF upload and automatic document indexing.
- Semantic search using local embeddings.
- Chinese and English question answering.
- Cross-language query rewriting and retrieval.
- Page-level citations and source passages.
- Refusal when the document does not contain sufficient information.
- Fallback to original-query retrieval if query rewriting fails.

- PDF 上传与自动文档索引。
- 本地向量模型语义检索。
- 中英文文档问答。
- 跨语言查询改写与检索。
- 答案页码引用及原文片段展示。
- 文档依据不足时拒绝编造答案。
- 查询改写失败时自动回退。

## 3. Technology Stack · 技术栈

| Component / 组件 | Technology / 技术 |
|---|---|
| Programming language | Python 3.11 |
| Web interface | Streamlit |
| RAG framework | LangChain |
| LLM | DeepSeek API |
| Embeddings | Ollama + bge-m3 |
| Vector store | InMemoryVectorStore |
| PDF parsing | PyPDFLoader |

## 4. Architecture · 系统架构

PDF Upload → Text Extraction → Chunking → Embeddings → Vector Store

User Question → Query Rewriting (when applicable) → Retrieval → DeepSeek → Answer with Citations

PDF 上传 → 文本解析 → 文本切分 → 向量化 → 向量库

用户提问 → 按需查询改写 → 文档检索 → 大模型生成 → 带引用的答案

## 5. Test Results · 测试结果

Evaluation document: Land Management Law of the People's Republic of China (2020 sample PDF).

测试文档：《中华人民共和国土地管理法》项目测试 PDF。

| Metric / 指标 | Baseline / 优化前 | Optimized / 优化后 |
|---|---:|---:|
| Overall test pass rate | 19/20 (95%) | 20/20 (100%) |
| Chinese questions | 18/18 | 18/18 |
| English questions | 1/2 | 2/2 |
| In-document questions | 15/16 | 16/16 |
| Out-of-document refusal | 4/4 | 4/4 |
| Expected citation page matches | 15/16 | 16/16 |

The evaluation checks answer keywords, expected citation pages and refusal behavior. Results are specific to this 20-question test set and do not guarantee equivalent performance on unseen documents.

评测依据包括答案关键词、预期引用页码和文档外问题拒答表现。以上结果仅适用于本次20道题的测试集，不代表所有实际场景的准确率。

Test files / 测试文件：

- `tests/questions.csv`
- `docs/eval-results-baseline.csv`
- `docs/eval-results.csv`

## 6. Getting Started · 快速开始

1. Install Python 3.11 and Ollama.
2. Install the dependencies from `requirements.txt`.
3. Run `ollama pull bge-m3`.
4. Configure the repository root `.env` file using `.env.example`.
5. Start the application using `python -m streamlit run app.py`.
6. Open http://localhost:8501 and upload a PDF.

请确保 Ollama 服务正常运行，并配置有效的 DeepSeek API Key。不要将 API Key 提交到 GitHub。

## 7. Use Cases · 适用场景

- Employee onboarding and internal policies / 员工入职与内部制度
- Product manuals and technical documentation / 产品手册与技术文档
- Customer support knowledge bases / 客服知识库
- Manufacturing operating procedures / 制造业操作规程
- Frequently asked questions / 常见问题自动解答

## 8. Limitations · 当前限制

- Scanned PDFs require OCR preprocessing.
- The current vector store is designed for lightweight document collections.
- DeepSeek API access is required for answer generation.
- Local embeddings do not mean fully offline processing: retrieved passages are sent to the configured LLM API.
- Sensitive business documents require appropriate authorization and data protection.

- 扫描版 PDF 需要提前进行 OCR 处理。
- 当前向量库适用于轻量级文档场景。
- 答案生成依赖 DeepSeek API。
- 向量化在本地运行，但检索片段会发送给大模型 API，并非完全离线。
- 企业敏感文档需要获得授权并采取相应的数据保护措施。

## 9. Demo · 演示视频

Screen recording: Coming soon.

项目录屏演示：待上传。