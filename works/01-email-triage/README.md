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
_Fill in after testing._

- Test set: 20 synthetic emails in `sample-data/` · 20 封自造测试邮件
- Runs without error: __ / 20 · 无报错次数
- Classified correctly: __ / 20 · 分类正确数
- Failure handling demonstrated: retry + alert (screenshot in `docs/`) · 失败重试与提醒截图

## Demo · 演示
_2–3 minute screen recording (no face): link TBD · 2–3 分钟录屏（不露脸）_

## Notes · 备注
All data is synthetic. · 所有数据均为自造。
