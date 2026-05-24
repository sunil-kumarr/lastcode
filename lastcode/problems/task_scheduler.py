"""Task Scheduler — lastcode visualizer problem module."""
from __future__ import annotations
from lastcode.recorder import Recorder

TITLE = 'Task Scheduler'
CATEGORY = 'queue'
DIFFICULTY = 'medium'
RENDERER = 'queue'
DESCRIPTION = 'Given a characters array tasks, representing the tasks a CPU needs to do, where each character represents a unique task. Tasks could be done in any order. Each task is done in one unit of time. For each unit of time, the CPU could complete either one task or just be idle.'
DEFAULT_INPUT = (["A", "A", "A", "B", "B", "B"], 2)

CODE_LINES = ['def least_interval(tasks, n):', '    counts = {}', '    for t in tasks: counts[t] = counts.get(t, 0) + 1', '    max_heap = [-v for v in counts.values()]', '    max_heap.sort()', '    q = [] # (cnt, idle_until)', '    time = 0', '    while max_heap or q:', '        time += 1', '        if max_heap:', '            cnt = max_heap.pop(0)', '            if cnt + 1 < 0: q.append((cnt + 1, time + n))', '        if q and q[0][1] == time:', '            max_heap.append(q.pop(0)[0])', '            max_heap.sort()', '    return time']
_LINE_MAP = {i: i for i in range(1, 17)}

# Dummy visualization markers
def _viz_compare(*args, **kwargs): pass
def _viz_update(*args, **kwargs): pass
def _viz_found(*args, **kwargs): pass
def _viz_push(*args, **kwargs): pass
def _viz_pop(*args, **kwargs): pass
def _viz_peek(*args, **kwargs): pass
def _viz_enqueue(*args, **kwargs): pass
def _viz_dequeue(*args, **kwargs): pass
def _viz_link(*args, **kwargs): pass



def _task_scheduler_instrumented(tasks, n):
    counts = {}
    for t in tasks: counts[t] = counts.get(t, 0) + 1
    max_heap = [-v for v in counts.values()]
    max_heap.sort()
    queue = []
    time = 0
    while max_heap or queue:
        time += 1
        if max_heap:
            cnt = max_heap.pop(0)
            _viz_dequeue(cnt)
            if cnt + 1 < 0:
                queue.append((cnt + 1, time + n))
                _viz_enqueue(cnt + 1)
        if queue and queue[0][1] == time:
            item = queue.pop(0)
            _viz_dequeue(item)
            max_heap.append(item[0])
            max_heap.sort()
    return time

def run(input_data):
    tasks, n = input_data
    def handle_enq(locs: dict, depth: int) -> dict | None:
        return {"type": "enqueue", "val": locs.get("cnt") if locs.get("cnt") is not None else 0, "locals": {"queue": [x[0] for x in locs.get("queue", [])]}}
    def handle_deq(locs: dict, depth: int) -> dict | None:
        return {"type": "dequeue", "val": locs.get("cnt") if locs.get("cnt") is not None else 0, "locals": {"queue": [x[0] for x in locs.get("queue", [])]}}

    recorder = Recorder()
    return recorder.record(
        "_task_scheduler_instrumented",
        _task_scheduler_instrumented,
        tasks, n,
        marker_fns={"_viz_enqueue", "_viz_dequeue"},
        nested_fns=set(),
        marker_handlers={
            "_viz_enqueue": handle_enq,
            "_viz_dequeue": handle_deq,
        }
    )
