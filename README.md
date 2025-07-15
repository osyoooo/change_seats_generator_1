# 🎯 席替えジェネレーター

Streamlit を使って簡単に「教室の机配置 → CSV 取り込み → 条件付き席替え」を実現するアプリです。  
以下の条件を考慮して自動で座席を割り当てます：

- ✅ 前列優先（前から順に埋まる）
- ✅ 「視力」配慮 → 前列優先配置
- ✅ 「身長」配慮 → 後列優先配置
- ✅ 分離ペアの自動回避（CSV or 画面入力）

---

## 📦 必要ファイル

├── seat_generator_app.py
└── sample_students_with_separation.csv

yaml
コピーする
編集する

---

## 🚀 セットアップ手順

1. このリポジトリをクローン  
```bash
git clone https://github.com/your-username/seat-generator.git
cd seat-generator
必要なライブラリをインストール

bash
コピーする
編集する
pip install streamlit pandas
アプリを起動

bash
コピーする
編集する
streamlit run seat_generator_app.py
📄 CSVファイルの形式
以下の形式のCSVをアップロードしてください：

出席番号	性別	配慮事項	分離相手
1	M	視力/身長	5
2	F	聴力	
3	M		7

配慮事項 は / 区切りで複数指定可能（例：視力/身長）

分離相手 は隣接を避けたい生徒の出席番号

✅ サンプルCSVダウンロード
📎 sample_students_with_separation.csv

🧠 アプリの機能概要
🪑 教室レイアウトを自由に設定（行数 × 列数）

📄 CSVで生徒情報を一括管理

👁‍🗨 視力/身長に応じた座席優先配置

🚫 分離ペアは自動で隣接回避

🎯 座席表を画面に可視化（絵文字つき）

💡 今後の拡張アイデア
📤 CSV/PDFで出力保存

🔁 複数パターン同時生成

🤖 AIによる自動最適化（履歴活用）

🎭 グループワーク／行事用配置
