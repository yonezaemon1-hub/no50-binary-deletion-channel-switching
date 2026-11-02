# No.50 v0.2 独立監査依頼書（反証優先）

**依頼対象**: `paper/No50_v0.2_AUDIT_MANUSCRIPT_EN.md`、同PDF、v0.2検証器3本、evidence JSON、研究時系列。未公開。依頼は厳密性・引用・新規性・主張境界の評価であり、形式だけの同意を求めない。

## 最優先：v0.1監査指摘4点の再監査

1. Prop 2の旧論理穴: 各qで全最適ペアの**距離多項式集合がsingleton**、4検査点間で互いに素か。`verify_no50.py` のassertが期待どおりか。
2. Prop 3の表現: 失敗は**同じqでの最適性保存**に限定され、異なるqへの最適区間移動を否定していないか。`1011001/1100101` に共通0を先頭追加した例を別方式でチェック。
3. n=6〜8の新しい**全区間**分類: 列挙数 260/1190/5835、多項式係数ごとの支配、n=8例外6本、Bernstein区間不等式、交点の隔離・導関数符号、一意な根・切替回数の推論に穴がないか。特に**候補以外が交点区間に入り込まないか**を独立にチェック。
4. 文書修正: 題名を控えめに修正、616×2=1232検査、出力上書き問題、独立TV計算の不足が改善されているか。

## 強制反例検査

- n4,5 で式(3)を下回るペアがあれば **PROOF FAIL**。
- n6,7,8 でTable 1の包絡線を下回るペア・削除確率が一つでもあれば **PROOF FAIL**。
- Table 2の根の有理隔離区間や唯一性が誤りなら **PROOF FAIL**。
- 長さ8の全32,640ペアにおける q=4/5 の最適値が報告と違えば **COMPUTATION FAIL**。
- 256挿入操作の最良値や最適操作数が違えば **COUNTEREXAMPLE FAIL**。
- 本文が `limsup S(n)=infinity` を証明済み/反証済みと主張しているなら **OVERCLAIM FAIL**。
- OpenAI #122ほか直接同じ結果が存在するなら、**NOVELTY ESTABLISHED/FAIL** として具体的文献・命題番号を示してほしい。

## 最小手順

1. `SHA256SUMS.txt` の全配布ファイルを検算。可能ならWindows PowerShell 5.1の `run_audit_windows.ps1` も実行。
2. 3本のPythonを再実行。`evidence` とのバイト一致検査。
3. 可能ならSciPy/SymPy等の別手法で根の数と包絡線を独立確認。今回の同梱「独立」コードは整数qサンプルの完全全ペアTV照合であり、全区間の数学的独立監査を代替しない。
4. 参考文献[1]〜[3]の原文を確認。関連する finite deletion-channel / k-deck / binomial equivalence の新規性について最終判定を保留してよい。
5. `MODEL / PROOF / COMPUTATION / REFERENCES / NOVELTY / OVERCLAIM / FINAL` の7項目を `PASS / PARTIAL / FAIL / INCONCLUSIVE` で報告。

## 変更してはいけない主張境界

**無限切替は未証明。失敗は一般の無限切替予想の反証ではない。局所安定補題と既知のsubsequence-deck技術の新規性は主張しない。**

**監査中・公開HOLD。**
