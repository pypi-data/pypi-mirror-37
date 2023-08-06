import asyncio
from copy import deepcopy
from typing import Dict, List

from toposort import toposort

from .request import Action
from .internal import recur


class Plan:
    def __init__(self, dependency_graph, execution_plan, object_plan):
        self.dependency_graph = dependency_graph
        self.execution_plan = execution_plan
        self.object_plan = object_plan

    def as_obj(self):
        def _fix(node):
            if isinstance(node, set):
                return list(node)
            return node

        a = {
            "dependencies": recur(_fix, self.dependency_graph),
            "plan": recur(_fix, self.execution_plan),
        }
        return a


class Node:
    def __init__(self, action) -> None:
        self.action = action
        self.event = None

    def export_event(self):
        if self.event is None:
            self.event = asyncio.Event()
        return self.event

    def _signal_event(self):
        if self.event is not None:
            self.event.set()

    async def _run(self, context):
        output = await self.action.run(context)
        if output.failed:
            context.invalidate_dependencies(self.action.name)

        for k, v in output.variables.items():
            context.set_var(k, v)

        return output

    async def run(self, context):
        output = await self._run(context)
        context.set_result(self.action.name, output)
        self._signal_event()
        return output


class Joint:
    def __init__(self, awaits: List[Node], triggers) -> None:
        self.awaits = [n.export_event() for n in awaits]
        self.continuation = triggers

    async def run(self, context):
        await asyncio.gather(*[e.wait() for e in self.awaits])
        return await asyncio.gather(*[c.run(context) for c in self.continuation])


class ObjectPlan:
    def __init__(self, *starting):
        self._joints = []
        self._start = starting

    def joint(self, awaits, triggers):
        self._joints.append(
            Joint(awaits=awaits, triggers=triggers)
        )

    async def run(self, context):
        tasks = [s.run(context) for s in self._start] + [j.run(context) for j in self._joints]
        return await asyncio.gather(*tasks)


def plan_granular(actions: Dict[str, Action]) -> Plan:
    toposort_input = {}
    for k, v in actions.items():
        depends_on = set(el.module for el in v.requires() if not el.is_global)
        toposort_input[k] = depends_on
    # XXX toposort is a underused here
    groups = list(toposort(toposort_input))

    plan = {
        "start": groups[0]
    }
    for k, v in toposort_input.items():
        if v:
            plan.setdefault("joints", []).append({
                "awaits": list(v),
                "triggers": [k]
            })

    return Plan(
        dependency_graph=toposort_input,
        execution_plan=plan,
        object_plan=compile_object_plan(plan, actions),
    )


def populate_plan(plan, actions):
    """Populates plan with nodes"""

    _all = set(plan["start"])
    for joint in plan.get("joints", []):
        _all.update(joint["awaits"])
        _all.update(joint["triggers"])

    nodes = {n: Node(actions[n]) for n in _all}

    def ref_nodes(names):
        return [nodes[n] for n in names]

    plan["start"] = ref_nodes(plan["start"])
    joints = plan.get("joints", [])
    for idx, joint in enumerate(joints):
        joints[idx]["awaits"] = ref_nodes(joints[idx]["awaits"])
        joints[idx]["triggers"] = ref_nodes(joints[idx]["triggers"])
    return plan


def compile_object_plan(plan_definition, actions):
    plan_definition = deepcopy(plan_definition)
    ref_plan = populate_plan(plan_definition, actions)
    ref_joints = ref_plan.get("joints", [])

    plan = ObjectPlan(*ref_plan["start"])
    for ref_joint in ref_joints:
        plan.joint(
            awaits=ref_joint["awaits"],
            triggers=ref_joint["triggers"],
        )
    return plan
