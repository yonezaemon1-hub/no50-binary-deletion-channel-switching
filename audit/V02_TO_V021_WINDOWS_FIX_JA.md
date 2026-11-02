# No.50 v0.2 → v0.2.1 修正記録（Windows監査停止）

- 目的: Windows PowerShell 5.1でJSONの厳密バイト照合が停止した原因の修正。
- 実機ログ: 16件の配布SHA256はPASS、最初のPython検証本体もPASS、続くJSON比較でFAIL-CLOSED。
- 原因: Python `Path.write_text()` はWindowsでは `\n` を `\r\n` に変換し得る。配布JSONはLFで固定されているため内容が一致してもバイト不一致になる。
- 修正: `code/verify_no50.py`, `code/verify_envelope_n6_n8.py`, `code/independent_mask_audit.py` の出力部を `Path.write_bytes(...encode("utf-8"))` に変更し、OSに依存しないUTF-8 LFで書き出す。
- 不変: `paper/` (PDF、Markdown)、`evidence/` (3 JSON)、数学の計算・判定アルゴリズム、参照資料、監査での失敗記録。
- README・STATUS・SHA256SUMSは変更点を記録するため更新。
- 保護: SHA256の検査順序・FAIL-CLOSEDは変更せず、配布証拠を上書きしない。
- Linux再展開試験: 同梱3検証器を `-I -B` で再実行し、既存3 JSONと**バイト一致**することを検査。
- Windows PowerShell 5.1のv0.2.1実機実行は未確認。成功扱いにしない。
- 数学的な新規性・査読状況は変更なし。NOVELTY INCONCLUSIVE / AUDIT_HOLD。
