# JT-Automatic-Package · 自动打包机上位机日志解析

分拣场地打包机上位机的运行日志与解析脚本。用于还原单件包裹在打包工位的
称重、量方与贴标结果。

## 目录

| 路径 | 说明 |
| --- | --- |
| `logs/packer-agent-20261031.log` | 打包机上位机日志摘录 |
| `src/pack_log_parse.py` | 行格式解析与统计 |

## 服务标识

`JT-Automatic-Package`

出现位置：

- `logs/packer-agent-20261031.log`：每行的通道字段 `[JT-Automatic-Package]`
- `src/pack_log_parse.py`：`LOG_CHANNEL` 常量、`parse_line` 的通道校验
- `README.md`：标题与本节

## 使用

```bash
python src/pack_log_parse.py logs/packer-agent-20261031.log
```

输出每台设备的任务数、失败数与平均量方耗时。

## 字段说明

| 字段 | 说明 |
| --- | --- |
| `ch` | 设备通道，`packer-agent-<工位号>` |
| `task` | 打包任务号，`PKG-<日期>-<流水>` |
| `scan` | 扫码结果，`OK` / `RETRY` / `FAIL` |
| `weight` / `dims` | 称重与量方结果 |
| `operator` / `operator_id` | 工位操作员姓名与工号（脱敏） |

## 已知问题

- 老固件的行首时间戳为本地时间且不带时区，与新版 `Z` 结尾格式混存。
- `RETRY` 行不带 `weight`，统计时需按任务号回填首次成功值。

## 维护

场地设备组 · 工单 `EQ-1180`
