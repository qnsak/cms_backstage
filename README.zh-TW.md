# Async DDD Headless Markdown CMS

📘 語言：
- English（README.md）
- 台灣繁體中文（README.zh-TW.md）

一個極簡且專業的 **Headless CMS 起手式專案**，技術組合：

- FastAPI（Async）
- SQLAlchemy Async ORM
- SQLite（開發）＋可延伸至 PostgreSQL
- DDD 分層架構（Domain / Application / Infrastructure / Interfaces）
- Alembic migrations（資料庫版本管理）
- Draft → Publish 文章生命週期
- Tag 標籤管理（禁止刪除仍被引用的 Tag）
- Python 3.12 全面型別標註（Type Hints）

## 快速啟動（Docker）

```bash
make up
make migrate
make seed
```

開啟 API 文件：
- http://localhost:8000/docs

## 指令清單

```bash
make
```

## 設定

請複製 `.env.example` 成 `.env`，並透過環境變數設定敏感資訊。

## 資安

可選擇性啟用 rate limit（請調整為合適值）：
- `RATE_LIMIT_ENABLED=true`
- `RATE_LIMIT_REQUESTS=100`
- `RATE_LIMIT_WINDOW_SECONDS=60`

## 測試規劃

本專案採用符合 DDD 分層的測試策略：

- Domain：快速 unit test，包含無資料庫的純邏輯測試（例如 slug 驗證）。
- Interfaces：API flow 測試（fixture-driven）＋ response shape 的 contract 測試。
- Infrastructure：需要時再用的整合測試（repo/db 行為）。

常用指令：

```bash
make test
make test-report
make test-report-local
```

測試報告輸出在 `reports/`：
- `reports/junit.xml`
- `reports/pytest.html`
- `reports/coverage.xml`
- `reports/coverage-html/`

更完整的測試導讀請見 `docs/TESTING.md`。

## 授權
MIT
