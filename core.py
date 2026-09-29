"""矿场核心逻辑：矿脉、巷道、通风和支护。"""

import json
import random

MAX_EXPLOSIVE = 20
MAX_RESERVE = 100
SEED = 20260929


def new_game():
    random.seed(SEED)
    return {
        "veins": {},
        "reserve": MAX_RESERVE,
        "explosive": MAX_EXPLOSIVE,
        "ventilation": True,
        "collapsed": False,
        "supported": True,
        "work_hours": 0,
        "safety": 100,
        "shift_id": 0,
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    if not text or not text.strip():
        raise ValueError("空存档数据")
    state = json.loads(text)
    if not isinstance(state, dict) or "shift_id" not in state:
        raise ValueError("存档数据非法")
    return state


def mine_vein(state, vein_id, amount):
    if not vein_id or vein_id in state["veins"]:
        return False
    if amount <= 0 or amount > state["reserve"]:
        return False
    state["veins"][vein_id] = amount
    state["reserve"] -= amount
    return True


def work(state, hours):
    if hours <= 0:
        return False
    if state.get("collapsed") or not state.get("ventilation"):
        return False
    if not state.get("supported", True):
        return False
    state["work_hours"] += hours
    return True


def reserve_volume(state, vein_id):
    return state["veins"].get(vein_id, 0)


def blast(state, amount):
    if amount <= 0 or amount > state["explosive"]:
        return False
    state["explosive"] -= amount
    return True


def cancel_blast(state, amount):
    if amount <= 0:
        return False
    state["explosive"] = min(MAX_EXPLOSIVE, state["explosive"] + amount)
    return True


def support(state):
    if not state.get("supported", True):
        return False
    state["supported"] = True
    return True


def accident(state):
    state["safety"] = max(0, state["safety"] - 10)
    return state["safety"]


def _run_command(state, parts):
    cmd = parts[0]
    try:
        if cmd == "mine" and len(parts) == 3:
            return mine_vein(state, parts[1], int(parts[2]))
        if cmd == "work" and len(parts) == 2:
            return work(state, int(parts[1]))
        if cmd == "reserve" and len(parts) == 2:
            print("储量:", reserve_volume(state, parts[1]))
            return True
        if cmd == "blast" and len(parts) == 2:
            return blast(state, int(parts[1]))
        if cmd == "cancel" and len(parts) == 2:
            return cancel_blast(state, int(parts[1]))
        if cmd == "support" and len(parts) == 1:
            return support(state)
        if cmd == "accident" and len(parts) == 1:
            accident(state)
            return True
        if cmd == "save" and len(parts) == 1:
            print(save_state(state))
            return True
    except ValueError:
        return False
    return False


def main():
    state = new_game()
    print("矿场 - 命令: mine/work/reserve/blast/cancel/support/accident/save/quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw:
            print("空命令，已忽略")
            continue
        if raw == "quit":
            break
        parts = raw.split()
        if _run_command(state, parts):
            print("ok")
        else:
            print("非法命令或参数:", raw)


if __name__ == "__main__":
    main()
