# 毎日のナレッジベース更新ルーティン (Routine に登録済みのプロンプト)

毎日のナレッジベース更新タスクです。以下を順番に実行してください。

## 背景

Google Drive のフォルダ「Claudeナレッジベース」(folder id: `1qxqokf5dpvDu9bTIJoalbURy_98kR0qO`) に、
Obsidian 風ナレッジベースのマスターデータ `kb_data_YYYY-MM-DD.json` と閲覧用の
`ナレッジベース_YYYY-MM-DD.xlsx` が保存されています。データスキーマと変換スクリプトは
GitHub リポジトリ `eiji1221/my-game` の `knowledge-base/build_kb.py` にあります
(ブランチ `claude/spreadsheet-obsidian-features-k4emsj` が存在すればそれを、無ければ `main` を使用)。

## 手順

1. Drive フォルダ内で日付が最新の `kb_data_*.json` を探して読み込む
   (search_files で `parentId = '1qxqokf5dpvDu9bTIJoalbURy_98kR0qO' and title contains 'kb_data'`、
   read_file_content で取得)。
2. Gmail で過去24時間のメールを検索する (search_threads, query: `newer_than:1d`)。
3. claude-code-remote の `list_sessions` (mine: true) で過去24時間に更新された Claude セッションを取得する。
4. 既存ノートの `ref` (Gmail スレッド ID / セッション ID) と重複しないものだけを新規ノートとして追加する。
   - 各ノート: 1行要約、既存タグ語彙を優先したタグ付け、最低1つのハブへのリンク、
     内容が関連する既存ノートへの相互リンク (同じ話題・同じ送信元・因果関係など)。
   - ID は `M-YYYYMMDD-NN` / `C-YYYYMMDD-NN` 形式でその日の連番。
   - 同じ新トピックのノートが3件以上集まったら新しいハブノート (`H-名前`) を作ってよい。
5. `updated` を今日の日付に更新し、`kb_data_<今日の日付>.json` として Drive フォルダにアップロードする
   (create_file, contentMimeType: application/json, disableConversionToGoogleType: true)。
6. リポジトリの `build_kb.py` で Excel ブックを生成し
   (`python3 knowledge-base/build_kb.py <json> <xlsx>`)、
   `ナレッジベース_<今日の日付>.xlsx` として Drive フォルダにアップロードする
   (contentMimeType: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,
   disableConversionToGoogleType: true)。
7. 完了したら追加ノート数・追加リンク数・新規タグを簡潔に報告して終了する。

## 重要な制約

- リポジトリ `eiji1221/my-game` は**パブリック**。メールの内容・要約・送信者などの個人データを
  絶対にリポジトリへコミットしないこと。個人データは Drive のみに保存する。
- タグは既存語彙を再利用し、別タグの部分文字列になるタグ名を新設しない
  (例: 「転職」がある場合に「転職活動」タグは作らない)。
- 数式の再計算環境 (LibreOffice) が使えない場合は、build_kb.py 実行後に Python で
  リンク数・タグ件数の整合を検証すればよい。xlsx は Google スプレッドシートで開いた時点で計算される。
- 新しいメールやセッションが1件もない日は、その旨だけ報告して終了する (ファイルは作らない)。
