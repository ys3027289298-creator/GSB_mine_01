"""矿场核心逻辑：矿脉、巷道、通风和支护。"""

import json
import random

SEED = 45
random.seed(SEED)

MAX_RESERVE = 100
MAX_EXPLOSIVE = 20
ACCIDENT_COST = 10

REQUIRED_KEYS = (
    "veins",
    "reserve",
    "explosive",
    "ventilation",
    "collapsed",
    "supported",
    "work_hours",
    "safety",
    "shift_id",
    "pending_blast",
)


def new_game():
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
        "pending_blast": 0,
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    if not text or not text.strip():
        raise ValueError("存档数据为空")
    state = json.loads(text)
    if not isinstance(state, dict):
        raise ValueError("存档格式非法")
    missing = [key for key in REQUIRED_KEYS if key not in state]
    if missing:
        raise ValueError("存档缺少字段: " + ",".join(missing))
    return state


def _is_positive_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def mine_vein(state, vein_id, amount):
    if not vein_id or not _is_positive_number(amount):
        return False
    if vein_id in state["veins"]:
        return False
    if amount > state["reserve"]:
        return False
    state["veins"][vein_id] = amount
    state["reserve"] -= amount
    return True


def work(state, hours):
    if not _is_positive_number(hours):
        return False
    if state.get("collapsed"):
        return False
    if not state.get("ventilation"):
        return False
    if not state.get("supported"):
        return False
    state["work_hours"] += hours
    return True


def reserve_volume(state, vein_id):
    return state["veins"].get(vein_id, 0)


def blast(state, amount):
    if not _is_positive_number(amount):
        return False
    if amount > state["explosive"]:
        return False
    state["explosive"] -= amount
    state["pending_blast"] += amount
    return True


def cancel_blast(state, amount):
    if not _is_positive_number(amount):
        return False
    refund = min(amount, state["pending_blast"])
    if refund <= 0:
        return False
    state["pending_blast"] -= refund
    state["explosive"] = min(MAX_EXPLOSIVE, state["explosive"] + refund)
    return True


def support(state):
    return bool(state.get("supported"))


def accident(state):
    state["safety"] = max(0, state["safety"] - ACCIDENT_COST)
    return state["safety"]


def _parse_number(raw):
    try:
        value = float(raw)
    except (TypeError, ValueError):
        return None
    return int(value) if value.is_integer() else value


def main():
    state = new_game()
    print("矿场 - 命令: mine/work/reserve/blast/cancel/support/accident/save/quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw:
            print("空指令，请输入命令")
            continue
        parts = raw.split()
        cmd, args = parts[0], parts[1:]
        if cmd == "quit":
            break
        elif cmd == "mine" and len(args) == 2:
            amount = _parse_number(args[1])
            ok = amount is not None and mine_vein(state, args[0], amount)
            print("ok" if ok else "fail")
        elif cmd == "work" and len(args) == 1:
            hours = _parse_number(args[0])
            ok = hours is not None and work(state, hours)
            print("ok" if ok else "fail")
        elif cmd == "reserve" and len(args) == 1:
            print(reserve_volume(state, args[0]))
        elif cmd == "blast" and len(args) == 1:
            amount = _parse_number(args[0])
            ok = amount is not None and blast(state, amount)
            print("ok" if ok else "fail")
        elif cmd == "cancel" and len(args) == 1:
            amount = _parse_number(args[0])
            ok = amount is not None and cancel_blast(state, amount)
            print("ok" if ok else "fail")
        elif cmd == "support" and not args:
            print("ok" if support(state) else "fail")
        elif cmd == "accident" and not args:
            print(accident(state))
        elif cmd == "save" and not args:
            print(save_state(state))
        else:
            print("未知命令或参数错误:", raw)


if __name__ == "__main__":
    main()
