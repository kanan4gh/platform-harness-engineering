"""codex-template/.codex/hooks/check_tasklist_complete.py(Codex CLI版Stopフック)のユニットテスト。

Claude Code版との共通ロジック(検出・最新ディレクトリ選択)はtest_check_tasklist_complete.pyが
カバーするため、ここではCodex版の差分(cwd解決・連続ブロックガード)を中心に検証する。
"""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

HOOK_PATH = (
    Path(__file__).parents[2] / "codex-template" / ".codex" / "hooks" / "check_tasklist_complete.py"
)

spec = importlib.util.spec_from_file_location("codex_check_tasklist_complete", HOOK_PATH)
assert spec is not None and spec.loader is not None
hook = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hook)


def make_steering(tmp_path: Path, dirname: str, tasklist: str | None) -> Path:
    d = tmp_path / ".steering" / dirname
    d.mkdir(parents=True)
    if tasklist is not None:
        (d / "tasklist.md").write_text(tasklist, encoding="utf-8")
    return d


def write_tasklist(tmp_path: Path, dirname: str, content: str) -> None:
    (tmp_path / ".steering" / dirname / "tasklist.md").write_text(content, encoding="utf-8")


def test_check_incomplete_tasks_blocks(tmp_path: Path) -> None:
    make_steering(tmp_path, "20260712-foo", "- [x] done\n- [ ] not yet\n")
    result = hook.check({}, tmp_path)
    assert result is not None
    assert result["decision"] == "block"
    assert "not yet" in result["reason"]


def test_check_all_complete_returns_none(tmp_path: Path) -> None:
    make_steering(tmp_path, "20260712-foo", "- [x] done\n")
    assert hook.check({}, tmp_path) is None


def test_check_no_steering_dir_returns_none(tmp_path: Path) -> None:
    assert hook.check({}, tmp_path) is None


def test_check_ignores_non_dated_dirs(tmp_path: Path) -> None:
    make_steering(tmp_path, "example", "- [ ] サンプルタスク\n")
    assert hook.check({}, tmp_path) is None


def test_guard_fails_open_after_three_blocks_of_same_content(tmp_path: Path) -> None:
    make_steering(tmp_path, "20260712-foo", "- [ ] stuck task\n")
    for _ in range(3):
        assert hook.check({}, tmp_path) is not None
    # 同一内容への4回目はガードが働きブロックしない
    assert hook.check({}, tmp_path) is None


def test_guard_resets_when_tasklist_content_changes(tmp_path: Path) -> None:
    make_steering(tmp_path, "20260712-foo", "- [ ] task a\n- [ ] task b\n")
    for _ in range(3):
        assert hook.check({}, tmp_path) is not None
    assert hook.check({}, tmp_path) is None
    # 内容が変わればカウンタがリセットされ、再びブロックする
    write_tasklist(tmp_path, "20260712-foo", "- [x] task a\n- [ ] task b\n")
    assert hook.check({}, tmp_path) is not None


def test_guard_resets_when_all_complete(tmp_path: Path) -> None:
    make_steering(tmp_path, "20260712-foo", "- [ ] task\n")
    assert hook.check({}, tmp_path) is not None
    write_tasklist(tmp_path, "20260712-foo", "- [x] task\n")
    assert hook.check({}, tmp_path) is None
    # 完了で状態がリセットされるため、同一の未完了内容が再出現してもブロックできる
    write_tasklist(tmp_path, "20260712-foo", "- [ ] task\n")
    assert hook.check({}, tmp_path) is not None


def test_guard_state_is_stored_under_codex_dir(tmp_path: Path) -> None:
    make_steering(tmp_path, "20260712-foo", "- [ ] task\n")
    hook.check({}, tmp_path)
    assert (tmp_path / ".codex" / "hooks" / "state" / "stop_guard.json").is_file()


def test_no_state_file_created_when_all_complete(tmp_path: Path) -> None:
    # ブロック履歴のないクリーンな環境では状態ファイルを作らない
    make_steering(tmp_path, "20260712-foo", "- [x] done\n")
    assert hook.check({}, tmp_path) is None
    assert not (tmp_path / ".codex").exists()


def run_hook(stdin_text: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(HOOK_PATH)],
        input=stdin_text,
        capture_output=True,
        text=True,
        cwd=cwd,
    )


def test_main_resolves_project_root_from_cwd_field(tmp_path: Path) -> None:
    project = tmp_path / "project"
    project.mkdir()
    make_steering(project, "20260712-foo", "- [ ] not yet\n")
    # プロセスのcwdはtmp_pathだが、ペイロードのcwdフィールドが優先される
    proc = run_hook(json.dumps({"cwd": str(project)}), tmp_path)
    assert proc.returncode == 0
    out = json.loads(proc.stdout)
    assert out["decision"] == "block"


def test_main_no_output_when_complete(tmp_path: Path) -> None:
    make_steering(tmp_path, "20260712-foo", "- [x] done\n")
    proc = run_hook("{}", tmp_path)
    assert proc.returncode == 0
    assert proc.stdout == ""


def test_main_fail_open_on_invalid_stdin(tmp_path: Path) -> None:
    proc = run_hook("not json", tmp_path)
    assert proc.returncode == 0
    assert proc.stdout == ""
