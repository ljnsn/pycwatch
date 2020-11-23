from functools import reduce


def log_has(line, logs):
    # caplog mocker returns log as a tuple: `(module, level, message)`
    # and we want to match line against `message` in the tuple
    return reduce(
        lambda a, b: a or b,
        filter(lambda x: x[2] == line, logs.record_tuples),
        False
    )
