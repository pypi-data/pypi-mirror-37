"""\
procrun: process runner

a cool process runner.
"""
import os, signal, threading, time, traceback
__version__ = "1.2.0"
class ProcessRunnerMixin:
    def record_pid(_, procname):
        open(_.name+'/'+procname+'.pid', 'w').write(str(os.getpid()))
    def kill(_, procname):
        os.system("kill `cat %s/%s.pid` 2>/dev/null" % (_.name, procname))
    def cmd_loop(_, prefix, cmd):
        if cmd.startswith('@'): cmd = 'python -um ' + cmd[1:]
        sfx1 = ' 1>>%s/logs/%s.out' % (_.name, prefix)
        sfx2 = ' 2>>%s/logs/%s.err' % (_.name, prefix)
        while 1:
            print("%s: SPAWN %s" % (prefix, cmd))
            ret = os.system(cmd + sfx1 + sfx2); time.sleep(1)
    def launch_jobs(_, lines):
        _.record_pid('node')
        for cmd in (x.strip() for x in lines):
            if cmd and cmd[0]!='#':
                args = [ x.strip() for x in cmd.split(':', 1) ]
                threading.Thread(target=_.cmd_loop, args=args).start()
                time.sleep(0.05)
    def start(_, jobs='jobs'):
        def _suicide(): os.killpg(os.getpgid(os.getpid()), 9)
        try:
            signal.signal(signal.SIGUSR1, lambda*a: _suicide())
            _.launch_jobs(jobs)
            time.sleep(3600*24*365*100)
        except:
            traceback.print_exc() # goes to stderr
            _suicide()
    def stop(_):     os.system("kill -USR1 `cat %s/node.pid`" % _.name)
    pass # end class ProcessRunnerMixin
