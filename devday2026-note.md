## タイトル案

OpenAI DevDay 2026の主要発表を実務者向けに整理する　dots、GPT-6.1 Sol、プラグイン基盤と日本での確認事項

## 本文

## 要点

- OpenAIは現地時間2026年9月29日（日本時間9月30日に報道）、サンフランシスコのFort Mason Centerで開発者会議DevDay 2026を開催した。発表は20件超と報じられている。
- 中心は、常時稼働のエージェント「dots」、低価格モデル「GPT-6.1 Sol」、速度を買う「Ultrafast」、月額$500の「Pro 500」、ChatGPT内にアプリを組み込む「Plugin Extensions」。テーマは、質問に答えるチャットから、仕事を任せられるエージェントへの拡張である（本稿の整理）。
- 実務者が見るべき点は、提供地域とデータ所在、データ保持の設計、エージェントの権限管理の3つ。dotsは、EEA・英国・スイスが対象外と説明されている。日本での提供可否、日本語対応、円建て価格は、公式に明記が確認できていない。

## 全体像

- 主要数字：ChatGPTの週間ユーザー12億人（Altman氏の発表と報じられた）。OpenAIのまとめは、APIの初回トークンまでの時間が45%短縮、ツール呼び出しとワークフローが30%以上高速化としている（測定条件は未記載）。

## モデルと速度

- GPT-6.1 Sol：GPT-6 Astraに近い知能を、Astraの約5分の1の標準価格で提供するとOpenAIは説明する。100万トークンあたり入力$2、出力$10（Astraは$10と$50）で、9月22日公開のGPT-6 Solと単価は同じ。強化点はコーディング、コンピューター操作、専門業務。API、ChatGPT Work、Codex（Plus、Pro、Business、Enterprise、Edu）で9月29日から提供とされ、通常のChat（Free/Go含む）は後日。ただし公式コミュニティの一覧は提供状況を「Coming soon」と表記しており、利用前に要確認。
- Solの性能：OpenAIの主張では、AutomationBenchでClaude Opus 5.5を2.2pt上回り、コストは約3分の1。第三者機関Artificial Analysisの指数（報道経由）は、Solが約52、Astraが約53、Opus 5.5が58。一次確認は未了。
- Ultrafast：知能ではなく速度を上げる有料ティア。Codexで最大8倍、APIで最大6倍。API料金は標準の6倍（272Kトークン以下で入力$60、出力$300）。9月29日からAstra向けに提供、Sol版は「近日」。ChatGPT個人プランではPro 500のみ対象。米国外の推論レジデンシー（処理地域の固定）が必須のワークスペースでは使えない。最大値であり、作業全体が8倍速く終わる保証ではない。

## エージェントと開発基盤

- Agents API：Codexの実行基盤をOpenAIがホストするマネージド型で、セッション管理、コンテキスト圧縮、障害復旧をOpenAIが担う。パブリックベータの開始は9月10日（公式changelog。9月11日とする報道もある）。DevDayでOpenAIホスト型ブラウザによるコンピューター操作が加わり、サイトごとにユーザー承認が必要。並列サブエージェントに対応。追加のAPI料金はなく、トークンとツール・コンテナ分のみ課金。DevDay前の情報では米国データレジデンシーのみ、ZDR（入出力を保存しない設定）非対応で、現状は未確認。
- Decisions API：GPT-6 Lunaで入力の分類・振り分けを行う限定プレビュー。
- Amazon Bedrock Managed Agents：AWSがプレビュー提供。リージョンは米国東部と米国西部で、東京は含まれない。
- Private Intelligence：ZDR with Private Safety Processingは、プロンプトと応答をOpenAIが保持せず、暗号化した記録を顧客管理のストレージに置き、OpenAI職員が中身を見ずに自動安全審査を行う。ZDR承認済みの組織がプロジェクト単位で有効化する。8月にプレビュー告知済みで、DevDayで再提示された。機密計算を使うPrivate Inferenceは今秋プレビュー予定。

## ChatGPT・Codex

- dots：専用のクラウドPCとブラウザを持ち、接続したアプリを使って、チャットを閉じた後も作業を続ける。9月29日から順次提供。公式ドキュメント上の対象は、Pro 100/200/500（EEA・英国・スイスを除く）、Business Premium、Enterprise（既定でオフ、管理者が有効化）。Pro 200以上のみとする報道もあり、対象は要確認。Custom Rulesで実行前の確認を設定でき、パスワード変更などは常に人の承認が必要。ローンチ後1か月は拡張枠が付く。追加dotの料金は未公表。GPT-6 Astra搭載と報じられている。
- Pro 500：月額$500。Plusの25倍の利用枠、Astra Ultrafast、dot 1体を含む。同時に再開したPro 200は、新規契約の利用枠が20倍から10倍に縮小（既存契約者は10月29日まで旧枠）で、批判が報じられている。
- Space・Pages・Meetings：Spaceは人とdotsが共通の文脈で作業する場、Pagesは人とエージェントが共同編集する文書。Pro、Business、Enterpriseが対象と報じられている。Meetingsプラグイン（macOSベータ）は、ボット参加なしで会議を記録し、メモを作る。
- Codex：Codex Cloudは、ノートPCを閉じてもクラウド上の隔離環境でタスクが続き、デスクトップ・Web・モバイルから再開できる。Codex Security Cloudは脆弱性の検出と修正案を作るが、公式ドキュメントはresearch preview、ライブブログはGAと表記が割れる。SlackとTeamsで@ChatGPTを呼ぶ連携（Business、Enterprise、Edu）は、実行前に承認カードが出る。

## プラグイン・配布

- Plugin Extensions：プラグインを、ChatGPTとCodexのサイドバー、会話横のパネル、ファイルビューアなどに標準機能のように組み込める。拡張は9種類で、TypeScriptとPythonのSDKを提供。デモはFigma、Adobe、Canva。作成・発見・審査の仕組みも改善された。
- Sign in with ChatGPT：第三者アプリにChatGPTアカウントでサインインし、Plus/Proの契約枠をそのアプリ内で使える（APIキー不要）。ローンチパートナーは16社と報じられている。商用利用はドキュメント上、限定トライアル。
- OpenAI Marketplace（ベータ）：適格なエンタープライズ顧客が、契約コミットメントの一部を、OpenAIモデル上に構築されたパートナー製品の購入に充てられる。初期パートナーは32社。初期は製品探索と関心表明が中心で、購入はできない。対象プランは報道で割れる（Enterpriseのみ、Business・Enterprise・Healthcare・Educationなど）。

## 市場の受け止め

- 10月予定だった上位モデル「GPT-6.1 Astra」の見送りが、直前に報じられた。CBS NewsやEngadgetなどは、社内の安全評価が基準に届かなかったためと伝えている。OpenAI公式の詳細説明は確認できていない。
- 批評として、常駐エージェントは記憶と作業履歴を抱えるためロックインが強まること、Ultrafastの高コストが挙がっている。Every共同創業者は実機のdotsを試し、現時点では勧められないと評した（単独の報道）。

## 実務者への示唆（編集者の見解を含む）

- 提供地域とデータ所在を導入前に個別確認する。根拠：Ultrafastは米国外の推論レジデンシー必須ワークスペースで使えず、Agents APIはDevDay前時点で米国データレジデンシーのみ、Bedrock Managed Agentsは米国東西のみ。日本を含む既存のデータレジデンシー提供が新機能に及ぶかは未記載。
- データ保持と暗号鍵の設計で比較する。根拠：Private Intelligenceは、OpenAIが保持せず、顧客管理のストレージと暗号鍵（EKM）を使う設計。推測：規制産業では、この設計が採用の前提条件になりうる。
- エージェントの権限と承認は限定業務から試す。根拠：dotsのCustom Rules、人の承認が必須の操作、Enterpriseでの既定オフ。見解：当面は限定業務での試用が妥当。

## 留意点

- 日本：dotsの日本での提供可否、日本語対応、円建て価格は公式に明記が確認できていない。Pro 500はGizmodo Japanが日本でも契約可能と報じている（単独報道）。
- 出典：OpenAI公式のまとめページは調査環境から取得できず、公式コミュニティ投稿、公式ドキュメント、報道の照合が中心。ベンチマークと速度の数値は独立検証ではない。
- 既存APIの非推奨・移行に関する新規発表は確認できなかった。
- 内容は2026年9月30日時点。提供範囲と価格は変わりうるため、公式ページで最終確認をすること。

## 参考リンク

- https://community.openai.com/t/devday-2026-announcements-and-developer-resources/1402006
- https://learn.chatgpt.com/docs/dots
- https://developers.openai.com/api/docs/models/gpt-6.1-sol
- https://aws.amazon.com/about-aws/whats-new/2026/09/bedrock-managed-agents-preview/
- https://every.to/vibe-check/vibe-check-openai-devday-2026
- https://www.cnbc.com/2026/09/29/openai-devday-2026-live-updates.html

## 投稿メモ（記事本文には含めない）

- ハッシュタグ案：#OpenAI #DevDay2026 #ChatGPT #Codex #AIエージェント
- 代替タイトル：OpenAI DevDay 2026　20件超の発表を実務者向けに要約
- 投稿前の確認：公式のまとめページ（openai.com/index/devday-2026-recap/）を開き、dotsの対象プラン、GPT-6.1 Solの提供状況、Ultrafast Sol版の時期が更新されていないかを確認する。
