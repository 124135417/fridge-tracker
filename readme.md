
---

## 📦 Fridge Tracker（冰箱食物管理 & 电子墨水屏 Top10）

一个用于管理冰箱中食物存放时间，并生成「最久未食用 Top10」的项目。
后端负责数据与排序、渲染 PNG；前端提供一个静态网页用于操作；未来硬件端（ESP32 + E-Paper）将通过 HTTP 拉取 PNG 显示。

---

## ✨ 功能概览

### 已完成（当前阶段）

* 维护食物清单（JSON 数据源）
* 自动计算存放天数（today - date_in）
* 排序并取 Top10
* 使用 Pillow 渲染为电子墨水屏友好的 PNG（两列布局）
* FastAPI 提供 HTTP 接口：

  * 返回 PNG
  * 提供静态网页（HTML）进行查看/操作（static）

### 计划中（未完成）

* ESP32 端：HTTP 拉取 `/top10.png` 并显示到墨水屏
* 低功耗刷新策略（每天刷新一次）
* 数据层从 JSON 升级为 SQLite（可选）

---

## 🧱 项目结构


```text
fridge-tracker/
├── backend/
│   ├── fonts/                # 中文字体（Pillow 渲染用）
│   ├── data.py               # 早期假数据（可保留用于快速测试）
│   ├── ranking.py            # Top10 排序逻辑
│   ├── render.py             # 生成 top10.png（Pillow）
│   ├── storage.py            # 读写 JSON 数据（items.json）
│   ├── server.py             # FastAPI 应用（API + 静态页面）
│   └── __pycache__/
│
├── data/
│   └── items.json             # 当前数据源（实际存储）
│
├── output/
│   └── top10.png              # 生成的图片输出
│
├── static/
│   └── index.html             # 静态网页（管理/查看/刷新）
│
├── LICENSE
└── README.md
```


---

## 🧠 设计思路（分层解耦）

本项目采用“**后端生成图片，前端/硬件只负责展示**”的方式，降低嵌入式难度。

* `storage.py`：数据层（目前是 JSON，可替换为 SQLite）
* `ranking.py`：业务逻辑（计算 days + 排序 + Top10）
* `render.py`：展示层（把 Top10 画成 PNG）
* `server.py`：接口层（提供 API & 静态网页）
* `static/index.html`：操作/展示界面（浏览器端）

> 硬件端未来只需要 GET 一张图片，不参与业务计算。

---

## 🗃 数据格式（items.json）

`data/items.json` 结构示例：

```json
{
  "items": [
    {
      "id": "uuid-here",
      "name": "鸡蛋",
      "date_in": "2025-12-01"
    }
  ]
}
```

字段说明：

* `id`：唯一标识（推荐 UUID）
* `name`：食物名称（中文即可）
* `date_in`：放入冰箱日期（ISO 格式 `YYYY-MM-DD`）

---

## 🖼 图片输出（top10.png）

* 默认尺寸：`400 x 300`
* 两列布局：每列 5 个条目
* 内容为：序号 + 食物名 + 天数（右对齐）

---

## 🌐 HTTP 接口（FastAPI）

### 1）健康检查

`GET /`

返回示例：

```json
{"ok": true, "try": ["/top10.png", "/docs"]}
```

### 2）获取 Top10 图片

`GET /top10.png`

逻辑：

* 读取 `items.json`
* 计算 Top10
* 生成 `output/top10.png`
* 返回 `image/png`

### 3）API 文档

`GET /docs`

FastAPI 自动生成 Swagger 文档页面。

---

## 🖥 静态网页（static/index.html）

静态页面用于：

* 在浏览器中查看当前 Top10
* 进行简单的数据操作（例如添加/刷新等）
* 作为“软硬件对接前”的可视化控制台

访问方式（两种常见方式）：

### ✅ 方式 A：FastAPI 直接挂载 static（推荐）


* 打开：

  ```
  http://127.0.0.1:8000/
  ```

页面里一般会通过 `<img src="/top10.png">` 来显示最新图片。

### ✅ 方式 B：单独用浏览器打开 HTML

也可以直接打开本地文件：

* `static/index.html`

但这种方式遇到跨域/请求问题时不如方式 A 稳定。

> 建议最终统一用方式 A：由 FastAPI 提供静态页面。

---

## 🚀 本地运行

### 1️⃣ 安装依赖

```bash
pip install fastapi uvicorn pillow
```

### 2️⃣ 启动服务

在项目根目录进入后端目录：

```bash
cd backend
uvicorn server:app --reload
```

### 3️⃣ 打开浏览器

* 静态页面（如果 / 返回 HTML）：

  ```
  http://127.0.0.1:8000/
  ```
* 图片接口：

  ```
  http://127.0.0.1:8000/top10.png
  ```
* API 文档：

  ```
  http://127.0.0.1:8000/docs
  ```

---

## 🔌 硬件对接计划（未完成）

目标：

* ESP32 连 Wi-Fi
* 访问 `http://<PC_IP>:8000/top10.png`
* 拉取 PNG
* 解码并绘制到 E-Paper

注意：

* 需要保证 ESP32 能访问运行 FastAPI 的那台机器
* 将来可能需要：

  * PC 固定局域网 IP / 或路由器端口映射
  * 或把服务部署到云端

---

## ✅ 当前状态 Checklist

* [x] JSON 数据源（items.json）
* [x] Top10 排序逻辑（ranking）
* [x] PNG 渲染（render）
* [x] FastAPI 输出 PNG（/top10.png）
* [x] 静态网页展示（static/index.html）
* [ ] ESP32 拉取 PNG 并上屏
* [ ] 低功耗刷新策略
* [ ] SQLite（可选升级）

