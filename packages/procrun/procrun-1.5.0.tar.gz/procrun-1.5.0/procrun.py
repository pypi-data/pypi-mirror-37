"""\
procrun: process runner
a cool process runner.
"""
import re, os, sys, signal, threading, time, traceback
__version__ = "1.5.0"
def suicide(*a): os.killpg(os.getpgid(os.getpid()), 9)
def run_thread(f, *a): threading.Thread(target=f, args=a).start()
class ProcessMixin:
    def record_pid(_, procname):
        open(_.name+'/'+procname+'.pid', 'w').write(str(os.getpid()))
    kill_fmt = "kill `cat %s/%s.pid` 2>/dev/null"
    def kill(_, procname): os.system(_.kill_fmt % (_.name, procname))
    def stop(_):           os.system("kill -USR1 `cat %s/node.pid`" % _.name)
    pass # end class ProcessMixin
class ProcessRunnerMixin(ProcessMixin):
    def cmd_loop(_, prefix, cmd):
        prefix = prefix.strip();cmd = cmd.strip()
        if cmd.startswith('@'): cmd = 'python -um ' + cmd[1:]
        sfx1 = ' 1>>%s/logs/%s.out' % (_.name, prefix)
        sfx2 = ' 2>>%s/logs/%s.err' % (_.name, prefix)
        while 1:
            print("%s: SPAWN %s" % (prefix, cmd))
            os.system(cmd + sfx1 + sfx2) ; time.sleep(1)
    def start(_, lines):
        _.record_pid('node'); signal.signal(signal.SIGUSR1, suicide)
        [ (run_thread(_.cmd_loop, *cmd.split(':', 1)), time.sleep(0.1))
          for cmd in (x.strip() for x in lines) if cmd and cmd[0]!='#' ]
        time.sleep(3600)
    pass # end class ProcessRunnerMixin
class ProcessRunner(ProcessRunnerMixin):
    def __init__(_, name): _.name = name
    def cmd_loop(_, prefix, cmd):
        cmd2 = re.sub(r'\$\((\w+)\)', lambda m: os.getenv(m.group(0)), cmd)
        ProcessRunnerMixin.cmd_loop(_, prefix, cmd2)
    pass # end class ProcessRunner
if __name__=='__main__': ProcessRunner(sys.argv[1]).start(open(sys.argv[2]))
