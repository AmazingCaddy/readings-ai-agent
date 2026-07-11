#!/usr/bin/env python3
"""Deterministic Voyager-style toy embodied agent audit.

The experiment uses a tiny grid-world-like environment to test the shape of an
embodied lifelong-learning loop: curriculum tasks, executable skills,
environment feedback, execution errors, self-verification, skill reuse,
sandboxing, and stop conditions. It does not call a model and does not validate
Voyager or Minecraft behavior.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass(frozen=True)
class Task:
    task_id: str
    instruction: str
    goal_item: str
    goal_count: int


@dataclass(frozen=True)
class ActionResult:
    ok: bool
    message: str
    observation: dict[str, Any]


@dataclass
class Skill:
    name: str
    actions: list[str]
    verified: bool = False
    failures: int = 0


@dataclass
class TraceEvent:
    strategy: str
    event: str
    details: dict[str, Any]
    timestamp: str = field(default_factory=utc_now)


TASKS = [
    Task("TASK-1", "collect wood from the forest", "wood", 1),
    Task("TASK-2", "craft a pickaxe from gathered resources", "pickaxe", 1),
    Task("TASK-3", "mine stone in the cave", "stone", 1),
]


class ToyWorld:
    def __init__(self) -> None:
        self.location = "camp"
        self.inventory: dict[str, int] = {}
        self.side_effect_log: list[str] = []

    def snapshot(self) -> dict[str, Any]:
        return {"location": self.location, "inventory": dict(sorted(self.inventory.items()))}

    def add(self, item: str, count: int = 1) -> None:
        self.inventory[item] = self.inventory.get(item, 0) + count

    def consume(self, item: str, count: int) -> bool:
        if self.inventory.get(item, 0) < count:
            return False
        self.inventory[item] -= count
        if self.inventory[item] == 0:
            del self.inventory[item]
        return True

    def has(self, item: str, count: int) -> bool:
        return self.inventory.get(item, 0) >= count

    def step(self, action: str) -> ActionResult:
        if action.startswith("unsafe_"):
            return ActionResult(False, "sandbox_rejected_unsafe_action", self.snapshot())
        if action == "move_forest":
            self.location = "forest"
            return ActionResult(True, "moved_to_forest", self.snapshot())
        if action == "collect_wood":
            if self.location != "forest":
                return ActionResult(False, "wood_requires_forest", self.snapshot())
            self.add("wood", 1)
            return ActionResult(True, "collected_wood", self.snapshot())
        if action == "craft_planks":
            if not self.consume("wood", 1):
                return ActionResult(False, "planks_require_wood", self.snapshot())
            self.add("plank", 5)
            return ActionResult(True, "crafted_planks", self.snapshot())
        if action == "craft_sticks":
            if not self.consume("plank", 1):
                return ActionResult(False, "sticks_require_plank", self.snapshot())
            self.add("stick", 4)
            return ActionResult(True, "crafted_sticks", self.snapshot())
        if action == "craft_pickaxe":
            if not self.consume("plank", 3):
                return ActionResult(False, "pickaxe_requires_3_planks", self.snapshot())
            if not self.consume("stick", 2):
                self.add("plank", 3)
                return ActionResult(False, "pickaxe_requires_2_sticks", self.snapshot())
            self.add("pickaxe", 1)
            return ActionResult(True, "crafted_pickaxe", self.snapshot())
        if action == "move_cave":
            self.location = "cave"
            return ActionResult(True, "moved_to_cave", self.snapshot())
        if action == "mine_stone":
            if self.location != "cave":
                return ActionResult(False, "stone_requires_cave", self.snapshot())
            if not self.has("pickaxe", 1):
                return ActionResult(False, "stone_requires_pickaxe", self.snapshot())
            self.add("stone", 1)
            return ActionResult(True, "mined_stone", self.snapshot())
        return ActionResult(False, f"unknown_action:{action}", self.snapshot())


class ToyAgent:
    def __init__(self, strategy: str, step_budget: int = 18) -> None:
        self.strategy = strategy
        self.world = ToyWorld()
        self.step_budget = step_budget
        self.steps_used = 0
        self.trace: list[TraceEvent] = []
        self.skills: dict[str, Skill] = {
            "collect_wood": Skill("collect_wood", ["move_forest", "collect_wood"], strategy != "no_skill_library"),
            "craft_pickaxe": Skill("craft_pickaxe", ["craft_pickaxe"], False),
            "mine_stone": Skill("mine_stone", ["unsafe_spawn_stone", "move_cave", "mine_stone"], False),
        }

    def record(self, event: str, **details: Any) -> None:
        self.trace.append(TraceEvent(self.strategy, event, details))

    def execute_action(self, action: str) -> ActionResult:
        if self.steps_used >= self.step_budget:
            result = ActionResult(False, "stop_condition_step_budget_exhausted", self.world.snapshot())
            self.record("stop_condition", action=action, reason=result.message, step_budget=self.step_budget)
            return result
        self.steps_used += 1
        self.record("action", action=action, step=self.steps_used)
        result = self.world.step(action)
        self.record("environment_feedback", action=action, ok=result.ok, message=result.message, observation=result.observation)
        return result

    def verify_task(self, task: Task) -> bool:
        ok = self.world.has(task.goal_item, task.goal_count)
        self.record("self_verification", task_id=task.task_id, goal=task.goal_item, ok=ok, observation=self.world.snapshot())
        return ok

    def run_actions(self, task: Task, actions: list[str]) -> bool:
        for action in actions:
            result = self.execute_action(action)
            if not result.ok:
                return False
        return self.verify_task(task)

    def repair_skill(self, skill_name: str, failure_message: str) -> Skill | None:
        if self.strategy != "governed_curriculum_skill_library":
            return None
        if skill_name == "craft_pickaxe" and "requires" in failure_message:
            skill = Skill("craft_pickaxe", ["craft_planks", "craft_sticks", "craft_pickaxe"], False)
            self.record("skill_revised", skill=skill_name, reason=failure_message, actions=skill.actions)
            return skill
        if skill_name == "mine_stone" and failure_message == "sandbox_rejected_unsafe_action":
            skill = Skill("mine_stone", ["move_cave", "mine_stone"], False)
            self.record("skill_revised", skill=skill_name, reason=failure_message, actions=skill.actions)
            return skill
        return None

    def store_skill_if_verified(self, skill: Skill, task: Task, success: bool) -> None:
        if self.strategy == "governed_curriculum_skill_library" and success:
            skill.verified = True
            self.skills[skill.name] = skill
            self.record("skill_stored", skill=skill.name, verified=True, actions=skill.actions)
        elif self.strategy == "unverified_skill_library":
            skill.verified = False
            self.skills[skill.name] = skill
            self.record("skill_stored", skill=skill.name, verified=False, actions=skill.actions)

    def run_task(self, task: Task) -> dict[str, Any]:
        self.record("curriculum_task_started", task_id=task.task_id, instruction=task.instruction)
        skill_name = task.goal_item if task.goal_item != "wood" else "collect_wood"
        if task.goal_item == "pickaxe":
            skill_name = "craft_pickaxe"
        if task.goal_item == "stone":
            skill_name = "mine_stone"

        if self.strategy == "no_skill_library":
            scripted = {
                "TASK-1": ["move_forest", "collect_wood"],
                "TASK-2": ["craft_pickaxe"],
                "TASK-3": ["move_cave", "mine_stone"],
            }[task.task_id]
            success = self.run_actions(task, scripted)
            return self.make_task_result(task, success)

        skill = self.skills[skill_name]
        self.record("skill_selected", skill=skill.name, verified=skill.verified, actions=skill.actions)
        success = self.run_actions(task, skill.actions)
        if not success:
            last_failure = next(
                (event.details["message"] for event in reversed(self.trace) if event.event == "environment_feedback" and not event.details["ok"]),
                "verification_failed",
            )
            skill.failures += 1
            self.record("execution_error", skill=skill.name, message=last_failure, failures=skill.failures)
            revised = self.repair_skill(skill.name, last_failure)
            if revised is not None:
                success = self.run_actions(task, revised.actions)
                self.store_skill_if_verified(revised, task, success)
            else:
                self.store_skill_if_verified(skill, task, success)
        elif self.strategy == "governed_curriculum_skill_library":
            self.store_skill_if_verified(skill, task, success)
        return self.make_task_result(task, success)

    def make_task_result(self, task: Task, success: bool) -> dict[str, Any]:
        return {
            "task_id": task.task_id,
            "goal_item": task.goal_item,
            "success": success,
            "inventory": dict(sorted(self.world.inventory.items())),
            "steps_used": self.steps_used,
        }

    def run(self) -> dict[str, Any]:
        results = [self.run_task(task) for task in TASKS]
        verified_skill_count = sum(1 for skill in self.skills.values() if skill.verified)
        sandbox_rejections = sum(
            1
            for event in self.trace
            if event.event == "environment_feedback" and event.details["message"] == "sandbox_rejected_unsafe_action"
        )
        stop_events = sum(1 for event in self.trace if event.event == "stop_condition")
        return {
            "strategy": self.strategy,
            "successes": sum(1 for result in results if result["success"]),
            "total": len(results),
            "steps_used": self.steps_used,
            "verified_skill_count": verified_skill_count,
            "sandbox_rejections": sandbox_rejections,
            "stop_events": stop_events,
            "results": results,
            "skills": {name: skill.__dict__ for name, skill in sorted(self.skills.items())},
            "trace": [event.__dict__ for event in self.trace],
        }


def main() -> None:
    strategies = ["no_skill_library", "unverified_skill_library", "governed_curriculum_skill_library"]
    runs = [ToyAgent(strategy).run() for strategy in strategies]
    payload = {
        "status": "completed",
        "control": "deterministic_voyager_style_toy_environment",
        "real_model_validated": False,
        "real_voyager_validated": False,
        "real_minecraft_validated": False,
        "task_count": len(TASKS),
        "strategy_count": len(strategies),
        "summary": {
            run["strategy"]: {
                "successes": run["successes"],
                "total": run["total"],
                "steps_used": run["steps_used"],
                "verified_skill_count": run["verified_skill_count"],
                "sandbox_rejections": run["sandbox_rejections"],
                "stop_events": run["stop_events"],
            }
            for run in runs
        },
        "runs": runs,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
