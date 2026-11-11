# 01 · Email / form triage · 邮件与表单自动处理

**Maps to service package ① (business process automation) · 对应服务包 ①**

## Problem · 问题
A small business receives many enquiry emails or web-form submissions. Someone has to read each one, decide what it is, copy the key facts into a spreadsheet and tell the right person.
小企业每天收到大量咨询邮件或表单，需要人工阅读、分类、抄进表格、再通知负责人。

## What it does · 功能
Trigger (mailbox or form) → LLM classifies and summarises → row written to an online spreadsheet → notification sent. Failed runs retry automatically and raise an alert.
触发（邮箱或表单）→ 大模型分类与摘要 → 写入在线表格 → 发送通知；失败自动重试并提醒。

## Stack · 技术
n8n (community edition, self-hosted) · LLM API (DeepSeek or Qwen) · online spreadsheet

## Run it · 运行
1. `docker compose up -d` from the repository root, then open http://localhost:5678.
2. Import `workflow/email-triage.json` (export your finished workflow into this folder).
3. Add your own credentials in n8n (mail, spreadsheet, LLM). Credentials are never exported with the workflow.

## Test results · 测试结果

- Test set: 20 synthetic enquiries in `sample-data/test-enquiries.csv` (10 Chinese, 10 English; 4 per category) · 20 条自造测试咨询（中英各 10 条）
- Runs without error: 20 / 20 · 无报错次数
- Classified correctly: 20 / 20 (100%) · 分类正确数
- Spam correctly marked as no reply needed: 4 / 4 · 垃圾信息正确标记为无需回复
- Model: DeepSeek, temperature 0, JSON output · 模型：DeepSeek，温度 0，JSON 输出
- Failure handling: 3 retries on the LLM call + error-alert email workflow (screenshot in `docs/`) · 失败重试与报错提醒
- Full results: `docs/test-results.csv`

## Demo · 演示
_2–3 minute screen recording (no face): link TBD · 2–3 分钟录屏（不露脸）_

## Notes · 备注
All data is synthetic. · 所有数据均为自造。
