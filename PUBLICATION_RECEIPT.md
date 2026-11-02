# No.50 正式公開記録 — 2026-11-02

**GitHub・Zenodoの正式公開、公開ファイル4件の再取得とSHA256照合、Google Drive「論文一覧」のNo.50更新は完了。**

記録日時: 2026-11-02 20:49 JST

## 確定した書誌・公開先

| 項目 | 確定情報 |
| --- | --- |
| No. | 50 |
| Title | Finite-Length Switching and Limitations of Recursive Constructions in Binary Deletion Channels |
| Author | Ryutaro Yonezu — Independent Researcher |
| Date / Version | 2026-11-02 / v1.0 |
| Publication type | Preprint |
| Rights | All rights reserved |
| Mathematics | Finite-length results PASS (computer-assisted) |
| Independent AI audit | PASS for finite-length results（著者提示結果を継承） |
| Windows PowerShell reproduction | PASS for v0.2.1（2026-11-02の著者提示実機結果） |
| General conjecture | UNPROVEN |
| Failed construction | Counterexample verified |
| Novelty | INCONCLUSIVE |
| Peer review | Not human peer-reviewed |
| Publication status | Published |

- GitHub repository: https://github.com/yonezaemon1-hub/no50-binary-deletion-channel-switching
- GitHub Release v1.0: https://github.com/yonezaemon1-hub/no50-binary-deletion-channel-switching/releases/tag/v1.0
- Zenodo record: https://zenodo.org/records/23883910
- 発行済みVersion DOI: **10.5281/zenodo.23883910**
- DOI resolver: https://doi.org/10.5281/zenodo.23883910
- 全版共通DOI: 10.5281/zenodo.23883909（今回のVersion DOIとは区別）

GitHubは新規の公開リポジトリを作成した。他研究の既存リポジトリは変更していない。初回公開コミットおよびRelease v1.0の対象は `2428468e842262bf27a176b0455ba47f80c9dd84`。

Zenodoの公開画面で、Published November 2, 2026 / Version v1.0 / Preprint / Yonezu, Ryutaro / Independent Researcher / All rights reservedを確認した。GitHub Release URLを「Is supplemented by / Software / URL」として関連付け、repository URLも登録した。既定のCC BY 4.0は削除し、All rights reservedのカスタム権利表示を設定した。レガシー公開APIはカスタムライセンス名を返さないため、権利の確認根拠は公開画面である。

## 元資料・数学の凍結

- 指定元ZIP: `No50_v0.2.1_WINDOWS_FIX_AUDIT_HOLD_20261102.zip`
- 元ZIP SHA256: `0ac639cd64810cba079155362de35a6f436560a8bd9d6dd631b42905a4b5a115`
- 元ZIPのSHA256マニフェスト: **17/17 PASS**。
- 数学本文第1〜7節は原稿テキストがバイト単位で同一。該当本文SHA256: `b4377a7fb99ea3215aa073bc0e1ae095fe74234a7a9c45946ae9500222b8a4fe`。
- Python3本、証拠JSON3本、PowerShellスクリプト、参照資料、研究時系列と旧監査文書の**保護12ファイルはバイト単位で同一**。
- 変更は正式表題・版・公開用の状態・README・著者と権利の説明・監査結果の出所の追記に限定。元ZIP全体を再現ZIPの `frozen/` に同梱。
- 旧HOLD、旧題名、旧v0.2、監査未実施という文字列は過去の凍結資料と無改変の検証器出力に残る。現在の公開状況と混同しないよう、現行README・STATUS・公開メタデータに説明した。

## 公開前検証

| 項目 | 結果 |
| --- | --- |
| 公開パッケージのSHA256 | 28/28 PASS（マニフェスト自身を除く） |
| verify_no50.py | exit 0 / PASS |
| verify_envelope_n6_n8.py | exit 0 / PASS |
| independent_mask_audit.py | exit 0 / PASS |
| 3検証器の出力と凍結証拠JSON | 3/3 バイト一致 |
| n=4,5 | 616ペア×2区間 = 1,232の厳密Bernstein証明書 PASS |
| n=6,7,8 | 2,016 / 8,128 / 32,640ペア、260 / 1,190 / 5,835多項式、厳密切替2 / 3 / 3回 PASS |
| 独立削除マスク列挙 | n=6〜8の有理数12点で全ペアTV最適値一致 |
| 挿入反例 | 256操作すべてで同一qの最適性保存に失敗することを確認 PASS |
| PowerShell監査スクリプト | 無改変の既存スクリプトをLinux / PowerShell 7.6.9で実行しexit 0 |
| PDF / 原稿 | v1.0原稿からpandoc / XeLaTeXで5ページPDF生成。書誌・内容照合、全ページ表示確認 PASS |

PowerShellの最終公開版実行ログ:

```text
PASS: 28 SHA256 file hashes
ALL PASS: HASH + FINITE PROOFS + INDEPENDENT TV CHECK
```

PowerShell 7.6.9はMicrosoft公式PowerShellリポジトリの配布を使用し、配布元のSHA256と一致を確認した。これは**Linuxでの再実行**であり、Windows PowerShell 5.1でv1.0を再実行したという意味ではない。Windows実機PASSは著者から提供されたv0.2.1の成功結果として継承する。外部AI監査・Windows実行の完全な原ログは元ZIPには含まれていなかった。

## 正式公開ファイルのSHA256

| ファイル | Bytes | SHA256 |
| --- | ---: | --- |
| No50_v1.0_PREPRINT_20261102.pdf | 76723 | `d09096642d5664ea08f2f5724d13348273e50fe5aa675f5dc2a6a616a44cbede` |
| No50_v1.0_REPRODUCIBILITY_20261102.zip | 222276 | `a6eb674d73dd5788efe65dd25aad2f464362fe928bb97ff92a0615f2ecc6549f` |

| 再取得元 | PDF | 再現ZIP |
| --- | --- | --- |
| GitHub Release v1.0 | SHA256一致・バイト一致 PASS | SHA256一致・バイト一致 PASS |
| Zenodo | SHA256一致・バイト一致 PASS | SHA256一致・バイト一致 PASS |

公開済みのHTTPSダウンロードURLから実ファイル4件を再取得した。GitHub APIに記録されたasset digest・サイズも2件とも一致した。GitHubの公開コミット中の全29ファイルのGit blobもローカルバイトから計算した値と一致した。

- GitHub / No50_v1.0_PREPRINT_20261102.pdf: https://github.com/yonezaemon1-hub/no50-binary-deletion-channel-switching/releases/download/v1.0/No50_v1.0_PREPRINT_20261102.pdf
- GitHub / No50_v1.0_REPRODUCIBILITY_20261102.zip: https://github.com/yonezaemon1-hub/no50-binary-deletion-channel-switching/releases/download/v1.0/No50_v1.0_REPRODUCIBILITY_20261102.zip
- Zenodo / No50_v1.0_PREPRINT_20261102.pdf: https://zenodo.org/records/23883910/files/No50_v1.0_PREPRINT_20261102.pdf?download=1
- Zenodo / No50_v1.0_REPRODUCIBILITY_20261102.zip: https://zenodo.org/records/23883910/files/No50_v1.0_REPRODUCIBILITY_20261102.zip?download=1

## 主張範囲と失敗記録

- 証明済み: n=4〜8の有限長最適包絡線、最適距離多項式の切替1,1,2,3,3、同一qでの共通ビット挿入最適性保存を否定する反例、固定長の局所安定性。
- 未証明: 切替回数の無限増大、一般nで最適性を保存する再帰構成。
- 区別: 反証されたのは特定の同一q挿入保存の一般命題であり、無限切替予想そのものではない。
- 観測: 異なるq区間へ最適性が移動する個別例は、一般定理ではない。
- 研究経緯・FAIL判定・反例・修正過程は保存し、本文とREADMEの両方で説明した。

本文、README、Zenodo概要に以下の留保を維持した。

> Novelty has not been conclusively established. This preprint has not undergone human peer review. The conjectured unbounded growth in switching complexity remains unproved.

## Google Drive「論文一覧」

- URL: https://docs.google.com/spreadsheets/d/1nvdNpcfehV_TS7P8Dch2A7PrOgc7y20cADsYEZR6gFE/edit
- タブ: `シート1` / sheetId 0
- 更新範囲: **A50:S50（19セル）**。
- No.50、正式表題、著者、日付、Version、GitHub repository/Release、Zenodo DOI/record、数学有限長PASS、一般予想UNPROVEN、反例検証済み、新規性INCONCLUSIVE、人間査読未実施、Publishedを登録した。
- 19セルすべての値・数式が書込予定と一致し、リンク数式にエラーなし。
- 既存範囲 **A1:S49** の値・数式・書式・注記・data validation・chip情報を更新前後で比較し、不変。対象外タブは編集していない。
- 新規行は既存行と同様の上揃え・折り返しで登録した。

## 警告・未確認事項

要求された公開・公開ファイルの照合・一覧更新に未完了の操作はない。

1. Windows PowerShell 5.1でのv1.0実機再実行は本環境では未実施。v0.2.1の実機PASSは著者提示結果、v1.0の本環境再実行はLinux / PowerShell 7.6.9として明記した。
2. 独立AI監査PASSは著者提示の監査結果を継承。完全な外部監査原ログは未同梱。今回実行した同梱3検証器の再計算とは区別した。
3. Google Sheetsの画面表示は、ブラウザ側Googleアカウントがログアウト状態のため未確認。APIによる19セルの内容・数式・書式・エラーなしと既存行不変の検証は完了。表示上の収まりは未確認として残す。
4. 一般予想はUNPROVEN、新規性INCONCLUSIVE、人間査読未実施。有限結果の検証PASSをこれらの保証へ拡張していない。

Release ZIPとZenodoの正式PDF/ZIPは公開後に変更していない。ZIP内の公開準備時点の状態はそのまま凍結し、公開確認後の現行README・STATUS・本記録で公開完了を示す。
