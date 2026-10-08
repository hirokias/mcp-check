"""【動作確認用の仮実装】MCPサーバーの接続確認のためだけに置くファイル。
演習本番では、受講者が第2段階でTDDにより作成する。
"""
import pandas as pd


def load_expenses(path):
    """CSVファイルを読み込む(BOM付き・BOMなしの両方に対応)"""
    return pd.read_csv(path, encoding="utf-8-sig")


def total_by_department(df):
    """部署ごとの合計金額"""
    return {k: int(v) for k, v in df.groupby("部署")["金額(円)"].sum().items()}


def total_by_month(df):
    """月ごと(YYYY-MM)の合計金額"""
    return {k: int(v) for k, v in df.groupby(df["利用日"].str[:7])["金額(円)"].sum().items()}


def total_by_transport(df, department=None):
    """交通手段ごとの合計金額(department を指定するとその部署だけ)"""
    if department:
        df = df[df["部署"] == department]
    return {k: int(v) for k, v in df.groupby("交通手段")["金額(円)"].sum().items()}
