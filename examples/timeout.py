from threading import Thread


def timeout(delay, call, *args, **kwargs):
    """Run a function call for `delay` seconds, and raise a RuntimeError
    if the operation didn't complete."""
    return_value = None

    def target():
        nonlocal return_value
        return_value = call(*args, **kwargs)

    t = Thread(target=target)
    t.start()
    t.join(delay)
    if t.is_alive():
        raise RuntimeError("Operation did not complete within time.")

    return return_value
