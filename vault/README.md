# Vault — Obsidianぽいノート環境

このフォルダは、GitHub上に構築した Obsidian 形式のノート環境(Vault)です。
Obsidian アプリは必須ではなく、Claude Code + [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) のスキル(`.claude/skills/` にインストール済み)で読み書きします。もちろん、このフォルダを Obsidian アプリで Vault として開くこともできます。

## フォルダ構成

```
vault/
├── Home.md          # トップページ(インデックス)。ここから辿る
├── notes/           # 恒久ノート(ゲーム設計、アイデア、調査メモなど)
├── daily/           # デイリーノート(YYYY-MM-DD.md)
├── templates/       # 新規ノート用テンプレート
├── bases/           # Obsidian Bases (.base) — ノートのデータベースビュー
├── canvas/          # JSON Canvas (.canvas) — 図・マップ
└── attachments/     # 画像などの添付ファイル
```

## 書き方のルール

- ノートは Obsidian Flavored Markdown で書く
  - ノート間リンクは `[[ノート名]]`(ウィキリンク)
  - 外部URLは `[テキスト](url)`
  - 強調ボックスは `> [!note]` などのコールアウト
- 各ノートの先頭に frontmatter(properties)を付ける: `tags`, `status`, `created` など
- 新しいノートは `templates/` のテンプレートをベースに `notes/` へ作成する
- デイリーノートは `daily/YYYY-MM-DD.md`

## Claude Code での使い方の例

- 「今日のデイリーノートを作って」
- 「敵AIについてのノートを作って、[[Metaverse Shadow Race]] からリンクして」
- 「notes/ の一覧を Bases で status ごとに見たい」
- 「このWebページを要約して notes/ にクリップして」(defuddle スキル)
