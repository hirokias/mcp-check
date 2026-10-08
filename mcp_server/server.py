"""交通費データの集計関数を、MCPのツールとしてClaude Codeに公開するサーバー。

- 集計の計算は src/analysis.py(第2段階でTDDにより作成)の関数をそのまま呼び出す
- このファイルには計算ロジックを書かない(テスト済みの関数だけを公開する)
- 標準出力はMCPの通信に使われるため、print() を使ってはいけない
"""
import os
import sys
from pathlib import Path

# リポジトリのルートを import 対象に加え、src/analysis.py を読み込めるようにする
ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR", Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(ROOT))

from mcp.server.fastmcp import FastMCP  # noqa: E402
from src import analysis  # noqa: E402

# 分析対象のCSVファイル(.mcp.json の env で指定。未指定ならリポジトリ内の既定の場所)
CSV_PATH = Path(os.environ.get("EXPENSE_CSV", ROOT / "data" / "expenses.csv"))

mcp = FastMCP("expense-analysis")


def _load():
    """CSVファイルを読み込む(ツールを呼ぶたびに最新の内容を読む)"""
    return analysis.load_expenses(CSV_PATH)


@mcp.tool()
def total_by_department() -> dict[str, int]:
    """部署ごとの交通費の合計金額(円)を返す。"""
    return analysis.total_by_department(_load())


@mcp.tool()
def total_by_month() -> dict[str, int]:
    """月ごと(YYYY-MM)の交通費の合計金額(円)を返す。"""
    return analysis.total_by_month(_load())


@mcp.tool()
def total_by_transport(department: str | None = None) -> dict[str, int]:
    """交通手段ごとの合計金額(円)を返す。department を指定するとその部署だけを集計する。"""
    return analysis.total_by_transport(_load(), department=department)


if __name__ == "__main__":
    mcp.run()  # 標準入出力(stdio)で待ち受ける
