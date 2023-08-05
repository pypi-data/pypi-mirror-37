from .utils import get_proxy_url
import dask
from dask.distributed import Client, sync
import logging
import os
from tornado import gen
from tornado.ioloop import IOLoop

logger = logging.getLogger(__name__)


class LSSTDaskClient(Client):
    """This uses the proxy info to provide an externally-reachable dashboard
    URL for the Client.  Other than that it does nothing differently from the
    standard dask.distributed.Client.  It assumes the LSST JupyterLab
    environment.
    """
    proxy_url = None

    @gen.coroutine
    def _update_scheduler_info(self):
        if self.status not in ('running', 'connecting'):
            return
        try:
            self._scheduler_identity = yield self.scheduler.identity()
        except EnvironmentError:
            logger.debug("Not able to query scheduler for identity")
        srv = self._scheduler_identity.get("services")
        if srv:
            self.proxy_url = get_proxy_url(srv.get("bokeh"))

    def __repr__(self):
        # Note: avoid doing I/O here...
        info = self._scheduler_identity
        addr = self.proxy_url or info.get('address')
        if addr:
            workers = info.get('workers', {})
            nworkers = len(workers)
            ncores = sum(w['ncores'] for w in workers.values())
            return '<%s: scheduler=%r processes=%d cores=%d>' % (
                self.__class__.__name__, addr, nworkers, ncores)
        elif self.scheduler is not None:
            return '<%s: scheduler=%r>' % (
                self.__class__.__name__, self.scheduler.address)
        else:
            return '<%s: not connected>' % (self.__class__.__name__,)

    def _repr_html_(self):
        if (self.cluster and hasattr(self.cluster, 'scheduler') and
                self.cluster.scheduler):
            info = self.cluster.scheduler.identity()
            scheduler = self.cluster.scheduler
        elif (self._loop_runner.is_started() and
                self.scheduler and
                not (self.asynchronous and self.loop is IOLoop.current())):
            info = sync(self.loop, self.scheduler.identity)
            scheduler = self.scheduler
        else:
            info = False
            scheduler = self.scheduler

        if scheduler is not None:
            text = ("<h3>Client</h3>\n"
                    "<ul>\n"
                    "  <li><b>Scheduler: </b>%s\n") % scheduler.address
        else:
            text = ("<h3>Client</h3>\n"
                    "<ul>\n"
                    "  <li><b>Scheduler: not connected</b>\n")
        sched_addr = self.proxy_url or scheduler.address
        if info and 'bokeh' in info['services']:
            protocol, rest = sched_addr.address.split('://')
            port = info['services']['bokeh']
            if protocol == 'inproc':
                host = 'localhost'
            else:
                host = rest.split(':')[0]
            template = dask.config.get('distributed.dashboard.link')
            address = template.format(host=host, port=port, **os.environ)
            text += "  <li><b>Dashboard: </b>"
            text += "<a href='%(web)s' target='_blank'>%(web)s</a>\n" % {
                'web': address}

        text += "</ul>\n"

        if info:
            workers = len(info['workers'])
            cores = sum(w['ncores'] for w in info['workers'].values())
            memory = sum(w['memory_limit'] for w in info['workers'].values())
            # memory = format_bytes(memory)
            text2 = ("<h3>Cluster</h3>\n"
                     "<ul>\n"
                     "  <li><b>Workers: </b>%d</li>\n"
                     "  <li><b>Cores: </b>%d</li>\n"
                     "  <li><b>Memory: </b>%s</li>\n"
                     "</ul>\n") % (workers, cores, memory)

            return ('<table style="border: 2px solid white;">\n'
                    '<tr>\n'
                    '<td style="vertical-align: top; '
                    'border: 0px solid white">\n%s</td>\n'
                    '<td style="vertical-align: top; '
                    'border: 0px solid white">\n%s</td>\n'
                    '</tr>\n</table>') % (text, text2)

        else:
            return text
