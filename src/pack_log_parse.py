#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""打包机上位机日志解析。

行格式：
    <ts> <LEVEL> [<channel>] ch=... seq=... task=... belt=... scan=... ...
"""
import re
import sys
from collections import defaultdict

LOG_CHANNEL = "JT-Automatic-Package"

LINE_RE = re.compile(
    r"^(?P<ts>\S+)\s+(?P<level>[A-Z]+)\s+\[(?P<ch>[^\]]+)\]\s+(?P<kv>.+)$")
KV_RE = re.compile(r"(\w+)=([^\s]+)")


def parse_line(line):
    m = LINE_RE.match(line.strip())
    if not m:
        return None
    if m.group("ch") != LOG_CHANNEL:
        return None
    rec = {"ts": m.group("ts"), "level": m.group("level")}
    for k, v in KV_RE.findall(m.group("kv")):
        rec[k] = v
    return rec


def summarize(records):
    stats = defaultdict(lambda: {"tasks": set(), "retry": 0, "fail": 0})
    for r in records:
        dev = stats[r.get("ch", "?")]
        dev["tasks"].add(r.get("task"))
        if r.get("scan") == "RETRY":
            dev["retry"] += 1
        elif r.get("scan") == "FAIL":
            dev["fail"] += 1
    return stats


def main(path):
    with open(path, encoding="utf-8") as fh:
        records = [parse_line(l) for l in fh]
    records = [r for r in records if r]
    for dev, s in sorted(summarize(records).items()):
        print("%-18s tasks=%d retry=%d fail=%d" %
              (dev, len(s["tasks"]), s["retry"], s["fail"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "logs/packer-agent-20261031.log"))
