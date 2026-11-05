import json
from pathlib import Path


def load_config(path):
    """读配置，返回 dict；文件不存在或格式错会抛异常，让调用方处理"""
    p = Path(path)
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def get_config(path, default=None):
    """读配置，出错时返回默认值，不抛异常（适合给新手/健壮程序用）"""
    try:
        return load_config(path)
    except (FileNotFoundError, json.JSONDecodeError, OSError) as e:
        print(f"[配置读取失败] {e}，使用默认配置")
        return default


def save_config(path, cfg):
    """写回配置，中文不转义、缩进 2"""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)