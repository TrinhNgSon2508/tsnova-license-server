import threading


# =========================================================
# START DAEMON THREAD
# =========================================================

def start_daemon_thread(

    target,

    args=(),

    kwargs=None
):

    if kwargs is None:

        kwargs = {}

    thread = threading.Thread(

        target=target,

        args=args,

        kwargs=kwargs,

        daemon=True
    )

    thread.start()

    return thread