"""
This type stub file was generated by pyright.
"""

from logging.handlers import BaseRotatingHandler

""" cloghandler.py:  A smart replacement for the standard RotatingFileHandler

ConcurrentRotatingFileHandler:  This class is a log handler which is a drop-in
replacement for the python standard log handler 'RotateFileHandler', the primary
difference being that this handler will continue to write to the same file if
the file cannot be rotated for some reason, whereas the RotatingFileHandler will
strictly adhere to the maximum file size.  Unfortunately, if you are using the
RotatingFileHandler on Windows, you will find that once an attempted rotation
fails, all subsequent log messages are dropped.  The other major advantage of
this module is that multiple processes can safely write to a single log file.

To put it another way:  This module's top priority is preserving your log
records, whereas the standard library attempts to limit disk usage, which can
potentially drop log messages. If you are trying to determine which module to
use, there are number of considerations: What is most important: strict disk
space usage or preservation of log messages? What OSes are you supporting? Can
you afford to have processes blocked by file locks?

Concurrent access is handled by using file locks, which should ensure that log
messages are not dropped or clobbered. This means that a file lock is acquired
and released for every log message that is written to disk. (On Windows, you may
also run into a temporary situation where the log file must be opened and closed
for each log message.) This can have potentially performance implications. In my
testing, performance was more than adequate, but if you need a high-volume or
low-latency solution, I suggest you look elsewhere.

See the README file for an example usage of this module.

"""
__version__ = ...
__author__ = ...
__all__ = ["ConcurrentRotatingFileHandler"]
FORCE_ABSOLUTE_PATH = ...
class ConcurrentRotatingFileHandler(BaseRotatingHandler):
    """
    Handler for logging to a set of files, which switches from one file to the
    next when the current file reaches a certain size. Multiple processes can
    write to the log file concurrently, but this may mean that the file will
    exceed the given size.
    """
    def __init__(self, filename, mode=..., maxBytes=..., backupCount=..., encoding=..., debug=..., supress_abs_warn=...) -> None:
        """
        Open the specified file and use it as the stream for logging.

        By default, the file grows indefinitely. You can specify particular
        values of maxBytes and backupCount to allow the file to rollover at
        a predetermined size.

        Rollover occurs whenever the current log file is nearly maxBytes in
        length. If backupCount is >= 1, the system will successively create
        new files with the same pathname as the base file, but with extensions
        ".1", ".2" etc. appended to it. For example, with a backupCount of 5
        and a base file name of "app.log", you would get "app.log",
        "app.log.1", "app.log.2", ... through to "app.log.5". The file being
        written to is always "app.log" - when it gets filled up, it is closed
        and renamed to "app.log.1", and if files "app.log.1", "app.log.2" etc.
        exist, then they are renamed to "app.log.2", "app.log.3" etc.
        respectively.

        If maxBytes is zero, rollover never occurs.

        On Windows, it is not possible to rename a file that is currently opened
        by another process.  This means that it is not possible to rotate the
        log files if multiple processes is using the same log file.  In this
        case, the current log file will continue to grow until the rotation can
        be completed successfully.  In order for rotation to be possible, all of
        the other processes need to close the file first.  A mechanism, called
        "degraded" mode, has been created for this scenario.  In degraded mode,
        the log file is closed after each log message is written.  So once all
        processes have entered degraded mode, the next rotate log attempt should
        be successful and then normal logging can be resumed.

        This log handler assumes that all concurrent processes logging to a
        single file will are using only this class, and that the exact same
        parameters are provided to each instance of this class.  If, for
        example, two different processes are using this class, but with
        different values for 'maxBytes' or 'backupCount', then odd behavior is
        expected. The same is true if this class is used by one application, but
        the RotatingFileHandler is used by another.

        NOTE:  You should always provide 'filename' as an absolute path, since
        this class will need to re-open the file during rotation. If your
        application call os.chdir() then subsequent log files could be created
        in the wrong directory.
        """
        ...
    
    def acquire(self): # -> None:
        """Acquire thread and file locks. Also re-opening log file when running
        in 'degraded' mode."""
        ...
    
    def release(self): # -> None:
        """Release file and thread locks. Flush stream and take care of closing
        stream in 'degraded' mode."""
        ...
    
    def close(self): # -> None:
        """
        Closes the stream.
        """
        ...
    
    def flush(self): # -> None:
        """flush():  Do nothing.

        Since a flush is issued in release(), we don't do it here. To do a flush
        here, it would be necessary to re-lock everything, and it is just easier
        and cleaner to do it all in release(), rather than requiring two lock
        ops per handle() call.

        Doing a flush() here would also introduces a window of opportunity for
        another process to write to the log file in between calling
        stream.write() and stream.flush(), which seems like a bad thing."""
        ...
    
    def doRollover(self): # -> None:
        """
        Do a rollover, as described in __init__().
        """
        ...
    
    def shouldRollover(self, record): # -> bool:
        """
        Determine if rollover should occur.

        For those that are keeping track. This differs from the standard
        library's RotatingLogHandler class. Because there is no promise to keep
        the file size under maxBytes we ignore the length of the current record.
        """
        ...
    

