# cc-statusline

Claude Code のカスタムステータスラインです。

https://nyosegawa.com/posts/claude-code-statusline-rate-limits/ こちらを参考にしました

## 表示例

```
🤖 Opus 4.6 | 💭 ctx ● 4% | ⏱️ 5h ● 42% (2h33m) | 📅 7d ● 12% (6d22h) | 📂 my-repo | 🌿 feature/branch | 🟢 PR #123
```

| アイコン | 項目 | 説明 |
|---------|------|------|
| 🤖 | モデル名 | 使用中の Claude モデル |
| 💭 | ctx | コンテキストウィンドウ使用率 |
| ⏱️ | 5h | 5時間レートリミット使用率 + リセットまでの残り時間 |
| 📅 | 7d | 7日レートリミット使用率 + リセットまでの残り時間 |
| 📂 | リポジトリ | 現在の Git リポジトリ名 |
| 🌿 | ブランチ | 現在のブランチ名 |
| 🟢/🟣/🔴 | PR | 紐づく PR 番号と状態 (OPEN/MERGED/CLOSED) |

使用率の `●` は 0%→100% で緑→黄→赤のグラデーションで表示されます。

## 必要なもの

- Python 3.7+
- `git`
- [`gh`](https://cli.github.com/) (PR 表示に必要)
:
## Setup
~/.claude/settings.jsonに`statusline`を追加

```
"statusLine": {
  "type": "command",
  "command": "/path/to/statusline.py"
}
```


