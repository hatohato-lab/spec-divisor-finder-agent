# CLAUDE.md — spec-divisor-finder-agent

このリポジトリは「整数の非自明な約数を1つ返す（素数なら None）」エージェントと、その採点係（仕様アサーション）です。
出力が一意に決まらないため、返り値が本当に割り切るか・None なら本当に素数かを、オラクルが独立に再計算して検証します。

## 確認のしかた

- `python eval/oracle.py --selftest` … 採点係が正しいか（正例=PASS／既知バグ=FAIL）
- `python eval/oracle.py --candidate candidate` … エージェントの答え（`eval/corpus/candidate.py`）を採点
- `python eval/oracle.py` … お手本(reference.py)を採点

## いじるときの約束（評価駆動 / EDD）

- 先に eval（合否の基準）を満たすことを確認してから「完成」とする。雰囲気で done にしない。
- `eval/corpus/reference.py` と `broken_*.py` は採点係の検証用。むやみに変えない。
- Python 標準ライブラリのみ。秘密情報・個人情報・客先コードを入れない。

## ファイルの役割

- `.claude/agents/spec-divisor-finder-agent.md` … エージェント定義
- `eval/oracle.py` … 採点係（仕様アサーション）／`design/design.md` … 設計／`README.md` … 説明
