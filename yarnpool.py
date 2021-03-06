from remotepool import RemotePool, RemoteWorker
from threading import Thread
from time import sleep


class YarnPool(RemotePool):

    def __init__(self, processes=None, port=0, authkey=None):
        super(YarnPool, self).__init__(processes=processes,
                                       port=port,
                                       authkey=authkey,
                                       workerscript=None)
        self.stopping = False

        from knit import Knit
        self.k = Knit(autodetect=True)

        cmd = "python remoteworker.py --port %d --key %s" % (self.s.address[1], self.authkey)
        self.app_id = self.k.start(cmd,
                                   self._processes,
                                   files=['remoteworker.py', ])
        self.t = Thread(target=self._monitor_appid)
        self.t.deamon = True
        self.t.start()

    def _start_remote_worker(self, pid):
        rw = RemoteWorker(pid)
        self._pool.append(rw)

    def spinning_cursor(self):
        while True:
            for cursor in '|/-\\':
                yield cursor

    def _monitor_appid(self):
        cursor = self.spinning_cursor()
        while not self.stopping:
            try:
                status = self.k.status(self.app_id)
                yarnState = status['app']['state']
                print "YARN application is", yarnState
            except:
                pass
            sleep(1)

    def terminate(self):
        self.stopping = True
        super(YarnPool, self).terminate()

        self.k.kill(self.app_id)
