# アーキテクチャ図生成プロンプト集

Mermaid（GitHub上でそのまま描画可能）と、AI画像生成ツール向けプロンプトを掲載しています。

---

## 1. Mermaid 図（GitHubで直接レンダリング可能）

### 1-1. Streamlit Cloud アーキテクチャ（単一サーバー構成）

```mermaid
graph TD
    U1["👩 User"] --> SC
    U2["👩 User"] --> SC
    U3["👩 User"] --> SC
    UN["・・・ ×12,000人"] --> SC

    SC["🖥️ Streamlit Cloud\n────────────────\nCPU: 2コア（固定）\nMemory: 2.7GB（固定）\nスケールアウト不可"]

    SC --> UI["UI表示"]
    SC --> SR["検索"]
    SC --> AI["AI処理"]
    SC --> DB[("SQLite")]

    SC --> CRASH["⚡ SYSTEM CRASH\n503 Service Unavailable\n大量アクセスによりサーバー停止"]

    style SC fill:#f9f9f9,stroke:#999
    style CRASH fill:#ff4b4b,color:#fff,stroke:#cc0000
```

---

### 1-2. AWS / Azure アーキテクチャ（ロードバランサー + オートスケーリング）

```mermaid
graph TD
    U1["👩 User"] --> LB
    U2["👩 User"] --> LB
    U3["👩 User"] --> LB
    UN["・・・ ×12,000人"] --> LB

    LB["🔀 ロードバランサー\nリクエストを自動で振り分け"]

    LB --> EC1["☁️ EC2-1\nUI表示 / 検索 / AI処理"]
    LB --> EC2["☁️ EC2-2\nUI表示 / 検索 / AI処理"]
    LB --> EC3["☁️ EC2-3\nUI表示 / 検索 / AI処理"]
    EC3 -. "負荷増加時に自動追加" .-> ECN["☁️ EC2-N\n（オートスケーリング）"]

    EC1 --> DB[("🗄️ Database")]
    EC2 --> DB
    EC3 --> DB
    ECN --> DB

    style LB fill:#fff3cd,stroke:#ffc107
    style EC1 fill:#ffe0e0,stroke:#cc0000
    style EC2 fill:#ffe0e0,stroke:#cc0000
    style EC3 fill:#ffe0e0,stroke:#cc0000
    style ECN fill:#ffe0e0,stroke:#cc0000,stroke-dasharray:5 5
    style DB fill:#f0f0f0,stroke:#999
```

---

### 1-3. Streamlit Cloud vs AWS / Azure 比較フロー

```mermaid
flowchart LR
    subgraph SC["Streamlit Cloud（スケールアウト不可）"]
        direction TB
        A["12,000人のアクセス"] --> B["1台のサーバーに集中"]
        B --> C["CPU / メモリが限界に"]
        C --> D["⚡ システムクラッシュ"]
    end

    subgraph AWS["AWS / Azure（オートスケーリング）"]
        direction TB
        E["12,000人のアクセス"] --> F["🔀 ロードバランサーで分散"]
        F --> G["EC2-1 / EC2-2 / EC2-3 ..."]
        G --> H["✅ 安定稼働を維持"]
    end

    style D fill:#ff4b4b,color:#fff
    style H fill:#28a745,color:#fff
    style SC fill:#fff5f5,stroke:#ffcccc
    style AWS fill:#f5fff5,stroke:#ccffcc
```

---

### 1-4. オートスケーリングのシーケンス

```mermaid
sequenceDiagram
    participant Users as 👩 Users（増加中）
    participant LB as 🔀 Load Balancer
    participant Monitor as 📊 監視（CloudWatch）
    participant AS as ⚙️ Auto Scaling
    participant EC2 as ☁️ EC2 Instances

    Users->>LB: リクエスト急増
    LB->>EC2: 既存インスタンスへ振り分け
    EC2->>Monitor: CPU使用率 > 70% を通知
    Monitor->>AS: スケールアウトトリガー
    AS->>EC2: 新インスタンスを起動
    EC2->>LB: 新インスタンスをプールに追加
    LB->>EC2: リクエストを再分散
    EC2-->>Users: 応答時間が安定
```

---

## 2. AI 画像生成プロンプト

ChatGPT（DALL-E）や Midjourney、Stable Diffusion などに貼り付けて使用してください。

### 2-1. Streamlit Cloud（過負荷・クラッシュ）

```
A technical architecture diagram showing a single-server system under heavy load.
12,000 user icons on the left all connected by red arrows to one server box labeled "Streamlit Cloud".
The server box shows CPU at 100% with a warning bar.
A large red explosion icon labeled "SYSTEM CRASH / 503 Service Unavailable" appears next to the server.
Clean, flat design with white background. Infographic style.
```

### 2-2. AWS / Azure（ロードバランサー + オートスケーリング）

```
A technical architecture diagram showing a scalable cloud system.
12,000 user icons on the left sending arrows to a central yellow box labeled "Load Balancer".
From the Load Balancer, arrows point to three pink server boxes labeled "EC2-1", "EC2-2", "EC2-3",
each containing icons for UI, Search, and AI processing.
A dashed arrow indicates a fourth server being added automatically (labeled "Auto Scaling").
All servers connect to a shared database icon at the bottom.
Green checkmark and "Stable" label. Clean flat infographic style, white background.
```

### 2-3. 左右比較図（Streamlit Cloud vs AWS / Azure）

```
A side-by-side technical comparison diagram.
Left side labeled "Streamlit Cloud": users sending requests to one server, which crashes with a red explosion icon.
Right side labeled "AWS / Azure": users sending requests to a load balancer, which distributes to multiple servers, all stable with green checkmarks.
Blue arrows for normal flow, red arrows for overload.
Clean flat design, white background, suitable for a presentation slide.
```

---

## 3. draw.io / Lucidchart 向け構成メモ

手動でダイアグラムツールを使う場合の構成要素メモです。

### Streamlit Cloud 構成
- **図形**: ユーザーアイコン × 3〜5個（+「×12,000」テキスト）
- **矢印**: ユーザー → サーバー（赤・太線）
- **サーバーボックス**: 1つ（CPU/メモリ仕様を記載）
- **内部レイヤー**: UI表示 / 検索 / AI処理 / SQLite
- **クラッシュ表示**: 赤背景の「⚡ SYSTEM CRASH」ボックス

### AWS / Azure 構成
- **図形**: ユーザーアイコン × 3〜5個（+「×12,000」テキスト）
- **ロードバランサー**: 黄色ボックス（中央配置）
- **EC2インスタンス**: 3〜4つ（並列配置、ピンク背景）
- **内部レイヤー**: UI表示 / 検索 / AI処理（各インスタンスに）
- **オートスケール表示**: 点線ボックスで追加インスタンスを表現
- **データベース**: 下部に共有DB（シリンダーアイコン）
