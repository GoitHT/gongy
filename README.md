# 情侣积分记录与奖励兑换系统 💕

一个温馨可爱的情侣积分管理系统，用于记录良好行为并兑换奖励。

## 功能特点

✨ **积分项目管理** - 自定义积分规则模板
📊 **积分记录** - 快速记录并累计积分
🎁 **奖励兑换** - 用积分兑换心仪奖励
📝 **历史记录** - 查看所有积分和兑换记录

## 技术栈

- 后端：Flask + SQLAlchemy
- 数据库：SQLite
- 前端：HTML + CSS + JavaScript

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 初始化数据库

```bash
python init_db.py
```

这会创建数据库并添加一些初始数据（积分项目和奖励）。

### 3. 运行应用

```bash
python app.py
```

### 4. 访问系统

打开浏览器访问：http://127.0.0.1:5000

## 项目结构

```
gong/
├── app.py              # Flask 主应用
├── models.py           # 数据库模型
├── init_db.py          # 数据库初始化脚本
├── requirements.txt    # 依赖包
├── instance/
│   └── points.db       # SQLite 数据库（运行后生成）
├── templates/          # HTML 模板
│   ├── base.html
│   ├── index.html
│   ├── items.html
│   ├── add_record.html
│   ├── rewards.html
│   └── exchanges.html
└── static/
    └── style.css       # 样式文件
```

## 使用说明

### 积分项目管理
1. 点击"积分项目管理"进入项目配置页面
2. 可以新增、编辑、删除积分项目
3. 每个项目包含名称、分值、说明和启用状态

### 记录积分
1. 点击"记录积分"
2. 从下拉列表选择积分项目
3. 系统自动读取分值并记录

### 兑换奖励
1. 点击"兑换奖励"查看可用奖励
2. 当积分足够时会显示"可兑换"
3. 点击兑换后会扣除相应积分

### 查看记录
- 首页显示当前总积分和所有积分记录
- "兑换记录"页面显示历史兑换信息

## 注意事项

- 数据库文件位于 `instance/points.db`
- 首次运行请先执行 `init_db.py` 初始化数据库
- 可以根据需要修改初始数据

## 部署到 Render（数据持久化）

如果你要部署到 Render，建议使用 Render 的 PostgreSQL，而不是 SQLite 文件。

原因：
- SQLite 是单文件数据库，Render Web Service 实例重启/重建后，本地文件可能丢失。
- PostgreSQL 是独立托管数据库，服务重启后数据仍然保留。

### 1. 在 Render 创建 PostgreSQL

1. 进入 Render 控制台，创建 PostgreSQL。
2. 记下连接串（Render 会自动提供 `DATABASE_URL`）。

### 2. 创建 Web Service 并配置环境变量

关键环境变量：
- `DATABASE_URL`：绑定你创建的 PostgreSQL。
- `SECRET_KEY`：建议设置为随机长字符串。

本项目的 `app.py` 已支持：
- 有 `DATABASE_URL` 时使用 PostgreSQL。
- 没有 `DATABASE_URL` 时回退到本地 SQLite（便于本地开发）。

### 3. 构建与启动命令

- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`

### 4. 初始化数据库结构和初始数据

首次部署后，在 Render Shell 执行：

```bash
python init_db.py
```

脚本会创建表并写入初始积分项目/奖励；如果已有数据会跳过，避免重复初始化。

## 许可

MIT License
