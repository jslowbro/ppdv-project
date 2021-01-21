from models import TraceModel

max_marks = 10


def generate_marks(max_range):
    marks = {}
    n_marks = max_marks
    if max_range < max_marks:
        n_marks = max_range
    step = round(max_range / n_marks)
    for i in range(0, n_marks):
        marks[i * step] = str(i * step)
    marks[max_range] = str(max_range)
    return marks


def is_anomaly_detected(trace_model: TraceModel):
    if trace_model.l0a | trace_model.l1a | trace_model.l2a | trace_model.r0a | trace_model.r1a | trace_model.r2a:
        return True
    return False
