# No.50 v1.0 公開用パッケージ

正式表題: *Finite-Length Switching and Limitations of Recursive Constructions in Binary Deletion Channels*

著者: Ryutaro Yonezu — Independent Researcher / 2026-11-02 / v1.0 / Preprint / All rights reserved。

現時点のファイルは公開準備版。公開完了は公開ページと別紙の公開記録で確認する。

有限長 n=4,5,6,7,8 の最適距離多項式の切替回数は各1,1,2,3,3。全区間を厳密有理数で検証する計算機支援証明。

無限切替の証明は失敗し、一般予想はUNPROVEN。同じ削除確率で最適性を保存する共通1ビット挿入は256操作の反例で否定。ただし無限切替予想自体の反証ではない。別の削除確率区間へ最適性が移る具体例は観測だが、一般定理ではない。

有限長結果の独立AI監査PASS、および2026-11-02のv0.2.1 Windows PowerShell実機PASSは、著者の公開指示で提示された結果を継承。完全な外部監査・Windows実行ログは元ZIPに含まれていない。本環境の再実行は別途ログへ記録する。

新規性INCONCLUSIVE、人間査読未実施。数学本文第1〜7節、3本のPython、証拠JSON3本、PowerShellスクリプトは凍結。旧版の記録は `frozen/` と `audit/` にそのまま保存。旧HOLD表示は当時の履歴であり、現行状況は英語READMEとSTATUS.txtを参照。

Windowsでは展開先から `powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_audit_windows.ps1` を実行。詳細は `README.md`。
