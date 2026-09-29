"""矿场核心逻辑：矿脉、巷道、通风和支护。"""

import json


def new_game():
    return {
        "veins": {},
        "reserve": 100,
        "explosive": 20,
        "ventilation": True,
        "work_hours": 0,
        "safety": 100,
        "shift_id": 0,
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    state = json.loads(text)
    state["shift_id"] += 1
    return state


def mine_vein(state, vein_id, amount):
    state["veins"][vein_id] = amount
    state["reserve"] -= amount
    return True


def work(state, hours):
    state["work_hours"] += hours
    return True


def reserve_volume(state, vein_id):
    return state["veins"][vein_id] + 1


def blast(state, amount):
    state["explosive"] -= amount
    return True


def cancel_blast(state, amount):
    return True


def support(state):
    return True


def accident(state):
    state["safety"] -= 10
    state["safety"] -= 10
    return state["safety"]


def main():
    print("矿场 - 命令: mine/work/reserve/blast/cancel/support/accident/quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw or raw == "quit":
            break
        print("ok")


if __name__ == "__main__":
    main()
