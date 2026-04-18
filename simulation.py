import math
from constants import (
    STREAMLIT_CRASH_USERS,
    AWS_SCALE_THRESHOLD_CPU,
    AWS_MAX_INSTANCES,
    AWS_SCALE_DELAY_STEPS,
)


def ramp_up(target: int, step: int, total: int) -> int:
    """sigmoid曲線でアクセス数を徐々に増加させる"""
    # sigmoid: 0→1 を step/total で進める。中間点(total*0.4)で急増
    x = (step / total - 0.4) * 10
    ratio = 1 / (1 + math.exp(-x))
    return int(target * ratio)


def compute_streamlit_state(users: int) -> dict:
    """
    Streamlit Cloud の状態を計算する。

    Returns:
        dict with keys:
            cpu (float): CPU使用率 %
            memory (float): メモリ使用率 %
            response_time (float): 応答時間 秒
            current_users (int): 現在のアクセス数
            is_crashed (bool): クラッシュ状態か
    """
    # CPU: 3000人で100%到達
    cpu = min(users / (STREAMLIT_CRASH_USERS * 0.03), 100.0)

    # メモリ: 4000人で100%到達
    memory = min(users / (STREAMLIT_CRASH_USERS * 0.04), 100.0)

    # 応答時間: 指数的に悪化（1000人で約2秒、2000人で約8秒）
    response_time = 0.2 + (users / 1000) ** 2 * 0.2

    # クラッシュ判定
    is_crashed = users >= STREAMLIT_CRASH_USERS

    if is_crashed:
        cpu = 100.0
        memory = 100.0
        response_time = float("inf")

    return {
        "cpu": cpu,
        "memory": memory,
        "response_time": response_time,
        "current_users": users,
        "is_crashed": is_crashed,
    }


def compute_aws_state(users: int, current_instances: int, scale_cooldown: int) -> tuple:
    """
    AWS / Azure の状態を計算する。オートスケーリングも処理。

    Args:
        users: 現在のアクセス数
        current_instances: 現在のインスタンス数
        scale_cooldown: スケールアウトまでの残りステップ数（0のとき発動可能）

    Returns:
        (state_dict, new_instances, new_scale_cooldown)
        state_dict keys:
            cpu_per_instance (float): 1台あたりのCPU使用率 %
            response_time (float): 応答時間 秒
            current_users (int): 現在のアクセス数
            instances (int): 稼働インスタンス数
            scale_event (str | None): スケールアウトイベントメッセージ
    """
    new_instances = current_instances
    new_cooldown = max(scale_cooldown - 1, 0)
    scale_event = None

    # 1台あたりのCPU使用率
    cpu_per_instance = min(users / (current_instances * 30), 100.0)

    # スケールアウト判定
    if (
        cpu_per_instance > AWS_SCALE_THRESHOLD_CPU
        and new_instances < AWS_MAX_INSTANCES
        and new_cooldown == 0
    ):
        new_instances = min(current_instances + 1, AWS_MAX_INSTANCES)
        new_cooldown = AWS_SCALE_DELAY_STEPS
        scale_event = f"{current_instances}台 → {new_instances}台 にスケールアウト"
        # 再計算
        cpu_per_instance = min(users / (new_instances * 30), 100.0)

    # 応答時間: 台数増加に比例して安定
    response_time = 0.2 + (users / (new_instances * 3000)) * 0.8
    response_time = min(response_time, 5.0)  # 最大5秒

    return (
        {
            "cpu_per_instance": cpu_per_instance,
            "response_time": response_time,
            "current_users": users,
            "instances": new_instances,
            "scale_event": scale_event,
        },
        new_instances,
        new_cooldown,
    )


if __name__ == "__main__":
    # 動作確認
    print("=== ramp_up ===")
    for s in [0, 5, 10, 15, 20, 25, 30]:
        print(f"  step={s}: {ramp_up(12000, s, 30):,}人")

    print("\n=== Streamlit Cloud ===")
    for u in [500, 1000, 2000, 3000, 5000]:
        state = compute_streamlit_state(u)
        print(f"  {u:,}人: CPU={state['cpu']:.0f}% RT={state['response_time']:.1f}s crashed={state['is_crashed']}")

    print("\n=== AWS / Azure ===")
    instances = 1
    cooldown = 0
    for u in [500, 1000, 3000, 6000, 12000]:
        state, instances, cooldown = compute_aws_state(u, instances, cooldown)
        print(f"  {u:,}人: {instances}台 CPU/台={state['cpu_per_instance']:.0f}% RT={state['response_time']:.2f}s")
