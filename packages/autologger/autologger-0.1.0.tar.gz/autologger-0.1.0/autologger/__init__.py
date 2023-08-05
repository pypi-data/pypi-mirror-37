import json
import inspect
import logging

from colorlog.colorlog import ColoredRecord, ColoredFormatter
import structlog


class AutoLogger:
    """
    A logger proxy object, with all of the methods and attributes of C{Logger}.

    When an attribute (e.g., "debug") is requested, inspects the stack for the
    calling module's name, and passes that name to C{logging.getLogger}.

    What this means is that you can instantiate an C{AutoLogger} anywhere, and
    when you call it, the log entry shows the module where you called it, not
    where it was created.

    C{AutoLogger} also inspects the local variables where it is called, looking
    for C{self}. If C{self} exists, its classname is added to the module name.
    """

    def __init__(self):
        pass

    def __getattr__(self, name):

        stack = inspect.stack()
        frame = stack[1][0] if len(stack) > 1 else stack[0][0]

        try:
            # print("-" * 80)
            # print(inspect.stack()[1])
            # print("-" * 80)

            if 'self' in frame.f_locals:
                other = frame.f_locals['self']
                caller_name = '%s.%s' % (other.__class__.__module__, other.__class__.__name__)
            else:
                if '__name__' in frame.f_globals:
                    caller_name = frame.f_globals['__name__']
                else:
                    caller_name = '__main__'

            logger = structlog.get_logger(caller_name)

            return getattr(logger, name)
        finally:
            # See https://docs.python.org/3/library/inspect.html#the-interpreter-stack
            del frame


log = AutoLogger()


def log_exceptions(fn):
    """ A decorator designed to wrap a function and log any exception that method produces.

    The exception will still be raised after being logged.

    Also logs (at the trace level) the arguments to every call.

    Currently this is only designed for module-level functions.  Not sure what happens if a method is decorated
    with this (since logger is resolved from module name).
    """

    def wrapper(*args, **kwargs):
        try:
            a = args or []
            a = [str(x)[:255] for x in a]
            kw = kwargs or {}
            kw = dict([(str(k)[:255], str(v)[:255]) for k, v in kw.items()])
            log.debug('Calling %s.%s %r %r' % (fn.__module__, fn.__name__, a, kw))
            return fn(*args, **kwargs)
        except Exception as e:
            log.error("Error calling function %s: %s" % (fn.__name__, e))
            log.exception(e)
            raise

    wrapper.__name__ = fn.__name__
    return wrapper


def unstructure(record, msgobj):
    """
    Parameters:
        record: logging.LogRecord

        msgobj: Dict[str,Any]

    Returns:
        logging.LogRecord
    """

    event = msgobj.pop('event')

    # Remove a few other attributes that would be duplicated
    msgobj.pop('timestamp', None)
    msgobj.pop('level', None)
    msgobj.pop('logger', None)

    exc = msgobj.pop('exception', None)

    kwstrs = []
    for k in sorted(msgobj):
        kwstrs.append('{}={}'.format(k, msgobj[k]))

    if kwstrs:
        msg = '{event} [{kw}]'.format(event=event, kw=', '.join(kwstrs))
    else:
        msg = '{event}'.format(event=event)

    if exc:
        msg += '\n{}'.format(exc)

    clazz = record.__class__

    new_record = logging.LogRecord(name=record.name, level=record.levelno, pathname=record.pathname,
                       lineno=record.lineno, msg=msg, args=record.args, exc_info=record.exc_info,
                       funct=record.funcName, sinfo=record.stack_info)


    new_record.message = msg

    if hasattr(record, 'asctime'):
        new_record.asctime = record.asctime

    if hasattr(record, 'log_color'):
        new_record.log_color = record.log_color

    if isinstance(record, ColoredRecord):
        new_record = ColoredRecord(new_record)

    return new_record


class UnstructuredLogFormatter(logging.Formatter):

    def formatMessage(self, record):
        """
        Paramters:
            record: logging.LogRecord
        """
        try:
            msgobj = json.loads(record.getMessage())
        except ValueError:
            # JSONDecodeError is a subclass of ValueError but is not present in py27
            return self._style.format(record)
        else:
            new_record = unstructure(record, msgobj)
            return self._style.format(new_record)


class UnstructuredColoredFormatter(ColoredFormatter):

    def formatMessage(self, record):
        """
        Paramters:
            record: logging.LogRecord
        """
        try:
            msgobj = json.loads(record.getMessage())
        except ValueError:
            # JSONDecodeError is a subclass of ValueError but is not present in py27
            return self._style.format(record)
        else:
            new_record = unstructure(record, msgobj)
            return self._style.format(new_record)
