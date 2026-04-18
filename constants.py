# Streamlit Cloud
STREAMLIT_CPU_CORES = 2
STREAMLIT_MEM_GB = 2.7
STREAMLIT_CRASH_USERS = 3000   # この人数を超えるとクラッシュへ向かう
STREAMLIT_MAX_RPS = 100        # 最大処理リクエスト/秒

# AWS / Azure オートスケーリング
AWS_SCALE_THRESHOLD_CPU = 70   # CPU使用率がこの%を超えたらスケールアウト
AWS_MIN_INSTANCES = 1
AWS_MAX_INSTANCES = 8
AWS_SCALE_DELAY_STEPS = 3      # スケールアウト発動までのステップ数

# シミュレーション
SIMULATION_STEPS = 30          # アニメーションの総ステップ数
SIMULATION_INTERVAL_SEC = 0.5  # 1ステップあたりの待機時間(秒)
SLIDER_MIN = 100
SLIDER_MAX = 12000
SLIDER_DEFAULT = 5000
SLIDER_STEP = 100
