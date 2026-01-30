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

## 授權
MIT
