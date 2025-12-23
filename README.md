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

## 许可

MIT License
