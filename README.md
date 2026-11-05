# 日志工具：Logger + 配置读取

一套写给本项目的日志工具：把日志同时输出到控制台和文件，可按级别过滤；
配套一个配置读取工具，从 `config.json` 读取配置，供 Logger 和项目其它脚本共用。

## 目录结构

```
log_manager/
├── logger.py        # Logger 类：控制台 + 文件双输出，级别过滤
├── config_tools.py  # 配置读取/写回工具（json）
├── config.json      # 日志配置
├── main.py          # 演示：读配置 → 创建 Logger → 写日志
└── logs/            # 日志文件输出目录（首次运行自动创建）
```

## 环境要求

- Python 3.10 及以上（开发环境 3.14.7）
- 只用标准库（`json`、`pathlib`、`datetime`），不需要 pip 安装任何东西

## 快速开始

```bash
cd log_manager
python main.py
```

运行后：
- 控制台按配置的级别打印日志
- 日志同时追加写入 `config.json` 中 `log_file` 指定的文件
- 退出码 0 表示正常

## 配置说明（config.json）

| 字段 | 类型 | 含义 | 缺省值 |
|---|---|---|---|
| `app_name` | string | 日志里显示的程序名 | `"app"` |
| `log_level` | string | 输出阈值：`DEBUG`/`INFO`/`WARN`/`ERROR` | `"INFO"` |
| `log_file` | string | 日志文件路径，支持子目录如 `logs` | 不写文件 |
| `console` | bool | 是否输出到控制台 | `true` |
| `file` | bool | 是否写文件（需同时给出 `log_file`） | `true` |

示例：

```json
{
  "app_name": "log-analyzer",
  "log_level": "DEBUG",
  "log_file": "logs/app.log",
  "console": true,
  "file": true
}
```

## 日志格式

```
时间 [级别] 程序名: 消息
2026-10-22 14:28:35 [INFO] log-analyzer: 程序启动完成
```

## 级别过滤规则

级别数字：`DEBUG=10 < INFO=20 < WARN=30 < ERROR=40`。数字越小越详细。
只有 **消息级别数字 ≥ 配置级别数字** 才输出。

| 配置 `log_level` | 输出 |
|---|---|
| `DEBUG` | 全部，含 debug |
| `INFO` | INFO / WARN / ERROR |
| `WARN` | WARN / ERROR |
| `ERROR` | 仅 ERROR |

大小写不敏感：配置写 `"info"` 与 `"INFO"` 等价。
配置级别名拼错（如 `"INF"`）：**退回 `INFO`，并在控制台打印一条警告**，不崩溃。

## 配置读取工具 API（config_tools.py）

| 函数 | 行为 |
|---|---|
| `load_config(path)` | 严格读取：文件不存在、格式错误时**抛异常**，让调用方决定怎么处理 |
| `get_config(path, default=None)` | 宽容读取：任何错误都**返回 `default`** 并打印失败原因，不抛异常 |
| `save_config(path, cfg)` | 把 dict 写回 JSON：中文不转义（`ensure_ascii=False`）、缩进 2 空格 |

`main.py` 用 `get_config`（宽容模式）；需要严格校验的脚本用 `load_config`。

## 出错行为

| 场景 | 行为 |
|---|---|
| 配置文件不存在 | 用全默认配置启动，控制台打印一条提示，不崩溃 |
| 配置文件 JSON 格式错误 | 用全默认配置启动，打印可读的错误信息，不崩溃 |
| 日志文件目录不存在 | 自动创建（含中间目录） |
| 日志文件已存在 | 追加写入，**不清空**历史日志 |
| 写日志文件失败（权限/占用） | 控制台照常输出，打印一条失败提示，程序继续运行 |
| `console`/`file` 都为 false | 合法配置，日志不输出到任何地方（不报错） |

## 验收自检

1. 正常运行：控制台与文件内容一致
2. 配置级别改 `ERROR`：只出现 ERROR
3. 连续运行两次：文件日志累加，不清空
4. 删除 `../../w2/logs` 目录：运行后自动重建
5. 删除 `config.json`：程序用默认配置运行，不崩溃
6. `config.json` 写坏（多一个逗号）：打印可读错误，程序用默认配置继续
7. 配置写 `"log_level": "INF"`：打印警告并退回 INFO，正常输出
8. 把 `log_file` 指向无写权限的目录：控制台正常输出，程序不崩溃

## 已知限制

- 单进程使用，未处理多进程同时写同一日志文件
- 日志文件无限追加，不做轮转/大小控制
- 仅支持 5 个配置字段，新增字段需改代码
- 不拦截程序崩溃时的未捕获异常（没有自动记录 `traceback`）

## 更新记录

| 日期 | 变更 |
|---|---|
| 2026-10-22 | 初版：Logger 双输出 + 配置读取工具 |
