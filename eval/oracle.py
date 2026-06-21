#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
oracle.py — 仕様（アサーション）オラクル。

出力が一意に決まらない処理を、保存した正解と比べるのではなく
**出力が満たすべき仕様**を機械的に検証して判定する。候補 find_divisor(n) について、
テスト範囲の各 n で:
  - d を返したら : 1 < d < n かつ n % d == 0（本当に非自明な約数か）。
  - None を返したら: n は本当に素数か（オラクルが独立に試し割りで確認）。
を確かめる。正解値は保存しない。どんな約数を返しても仕様を満たせば PASS。

使い方:
  python oracle.py                  # reference.py（正例）を採点
  python oracle.py --candidate NAME # NAME.py を採点
  python oracle.py --selftest       # オラクル自身を検証（正例→PASS / 既知バグ→FAIL）
終了コード: PASS（または selftest 期待どおり）で 0、それ以外 1。
"""
import argparse
import importlib.util
import sys
from pathlib import Path

# Windows コンソール(cp932)でも日本語・記号を出せるよう出力を UTF-8 に統一。
# Linux/Mac は元から UTF-8 なので無害。これが無いと Windows で print が落ちる。
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

EVAL = Path(__file__).resolve().parent
CORPUS = EVAL / "corpus"
LO, HI = 2, 5000   # テスト範囲


def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def smallest_factor(n):
    i = 2
    while i * i <= n:
        if n % i == 0:
            return i
        i += 1
    return n


def load(path):
    spec = importlib.util.spec_from_file_location("cand_" + path.stem, str(path))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    if not hasattr(m, "find_divisor"):
        raise AttributeError(f"{path.name} に find_divisor(n) が無い")
    return m.find_divisor


def evaluate(find_divisor):
    for n in range(LO, HI + 1):
        d = find_divisor(n)
        if d is None:
            if not is_prime(n):
                return ("FAIL", f"n={n}: None を返したが実際は合成数（約数 {smallest_factor(n)} がある）")
        else:
            if not (isinstance(d, int) and not isinstance(d, bool) and 1 < d < n and n % d == 0):
                return ("FAIL", f"n={n}: 返り値 {d!r} が非自明な約数でない（要 1<d<n かつ n%d==0）")
    return ("PASS", f"n={LO}..{HI} すべてで仕様を満たす（約数なら割り切れ・None なら真に素数）")


def grade(path):
    try:
        fn = load(path)
    except Exception as e:
        return ("FAIL", f"読込失敗: {e}")
    try:
        return evaluate(fn)
    except Exception as e:
        return ("FAIL", f"実行エラー: {type(e).__name__}: {e}")


def table(rows, title):
    print(f"\n### {title}")
    print("| 対象 | 判定 | 詳細 |")
    print("|---|---|---|")
    for n, v, d in rows:
        print(f"| {n} | {v} | {d} |")


def selftest():
    print("# オラクル自己検証 — 仕様（アサーション）約数発見")
    rv, rd = grade(CORPUS / "reference.py")
    table([("reference", rv, rd)], "① 正しい約数発見 reference（PASS であるべき）")
    controls = [
        ("broken_const2.py", "常に 2 を返す → 多くの n で割り切れない/境界"),
        ("broken_trivial.py", "n 自身を返す → 自明な約数（1<d<n 違反）"),
        ("broken_falseprime.py", "平方数を素数と誤判定 → None なのに合成数"),
    ]
    brows, caught = [], True
    for f, why in controls:
        v, d = grade(CORPUS / f)
        ok = (v == "FAIL")
        caught = caught and ok
        brows.append((f, v, ("検出OK " if ok else "検出NG ") + d))
    table(brows, "② 壊れた実装（FAIL であるべき）")
    valid = (rv == "PASS") and caught
    print(f"\n## オラクル判定: {'PASS（バグを捕まえ正例を通す＝信頼できる）' if valid else 'FAIL（オラクル自体に欠陥）'}")
    return valid


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate", default="reference")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(0 if selftest() else 1)
    v, d = grade(CORPUS / f"{a.candidate}.py")
    table([(f"{a.candidate}.py", v, d)], "採点（仕様アサーション）")
    sys.exit(0 if v == "PASS" else 1)


if __name__ == "__main__":
    main()
