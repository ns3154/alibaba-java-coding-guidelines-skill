#!/usr/bin/env python3
"""校验本仓库是否保持 Codex skill 的基本结构。"""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    print(f"失败：{message}")
    sys.exit(1)


def main() -> None:
    skill = ROOT / "SKILL.md"
    reference = ROOT / "references" / "alibaba-java-rules.md"
    metadata = ROOT / "agents" / "openai.yaml"

    for path in (skill, reference, metadata):
        if not path.exists():
            fail(f"缺少文件 {path.relative_to(ROOT)}")

    skill_text = skill.read_text(encoding="utf-8")
    if not skill_text.startswith("---\n"):
        fail("SKILL.md 缺少 YAML frontmatter")
    if "name: alibaba-java-coding-guidelines" not in skill_text:
        fail("SKILL.md 的 skill 名称不正确")
    if "description:" not in skill_text:
        fail("SKILL.md 缺少 description")

    reference_text = reference.read_text(encoding="utf-8")
    required_sections = ["编程规约", "异常和日志", "MySQL 规约", "工程规约", "安全规约"]
    missing = [section for section in required_sections if section not in reference_text]
    if missing:
        fail("规则摘要缺少章节：" + "、".join(missing))

    print("通过：skill 结构和关键章节完整")


if __name__ == "__main__":
    main()
