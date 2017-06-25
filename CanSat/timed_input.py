import signal

class AlarmException(Exception):
    pass

def alarmHandler(signum, frame):
    #raise AlarmException
    return null

def nonBlockingRawInput(prompt='', timeout=3):
    signal.signal(signal.SIGALRM, alarmHandler)
    signal.alarm(timeout)
    try:
        text = raw_input(prompt)
        signal.alarm(0)
        return text
    except AlarmException:
        return -1
    signal.signal(signal.SIGALRM, signal.SIG_IGN)
    return None
