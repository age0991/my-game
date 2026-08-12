# my-game

ブラウザゲーム「Metaverse Shadow Race」のリポジトリ。実装は `my-game.txt`(中身はHTML)。

## vault/ — ノート環境

`vault/` は Obsidian 形式のノート環境(Vault)。ゲームの設計メモ・アイデア・作業ログはコードではなくここに書く。

- Vaultのルートは `vault/`。エントリポイントは `vault/Home.md`
- 運用ルールとフォルダ構成は `vault/README.md` を参照
- ノートの読み書きには `.claude/skills/` の obsidian-skills(obsidian-markdown / obsidian-bases / json-canvas / obsidian-cli / defuddle)を使うこと
- ウィキリンク(`[[ノート名]]`)・frontmatter・コールアウトなど Obsidian Flavored Markdown で書く
- 新規ノートは `vault/templates/` のテンプレートに従い、`vault/Home.md` または関連ノートからリンクを張る
- デイリーノートは `vault/daily/YYYY-MM-DD.md`
