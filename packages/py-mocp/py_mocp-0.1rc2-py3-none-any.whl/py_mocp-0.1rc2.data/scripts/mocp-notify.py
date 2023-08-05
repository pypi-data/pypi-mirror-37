#!python

import os
import html
import notify2
import logging
from mocp import MocEventLoop


class MocNotify:
    def __init__(self, icon='audio-x-generic', timeout=5000):
        notify2.init("mocp-notify")
        self.wn = notify2.Notification('mocp-notify', icon=icon)

        self.icon = icon
        self.timeout = timeout

        self.current_file = None

        self.mocp = MocEventLoop()
        self.mocp.register('on_file_changed', self._on_file_changed)
        self.mocp.register('on_title_changed', self._on_title_changed)

    def _on_file_changed(self, filename):
        self.current_file = filename

    def _on_title_changed(self, x):
        track = '.'.join(os.path.basename(self.current_file).split('.')[:-1])
        message = "<b>File:</b> <i>%s</i>" % html.escape(track)
        if bool(x.artist) and bool(x.title) and bool(x.album):
            message = "<b>Artist:</b> <i>%s</i>\n<b>Track:</b> <i>%s</i> (%s)" % (  # NOQA
                html.escape(x.artist),
                html.escape(x.title),
                html.escape(x.album)
            )
        elif bool(x.artist) and bool(x.title):
            message = "<b>Artist:</b> <i>%s</i>\n<b>Track:</b> <i>%s</i>" % (  # NOQA
                html.escape(x.artist),
                html.escape(x.title)
            )
        elif bool(x.title):
            message = "<b>Track:</b> <i>%s</i>" % html.escape(x.title)

        self._show_message("Now Playing:", message)

    def _show_message(self, subj, body):
        # We should call notify2.init to avoid dbus.exceptions.DBusException
        # https://bitbucket.org/takluyver/pynotify2/issues/3/dbusexceptionsdbusexception
        notify2.init("mocp-notify")
        self.wn.set_timeout(self.timeout)
        self.wn.update(subj, body, self.icon)
        self.wn.show()

    def run(self):
        self.mocp.run()


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(asctime)s] [%(levelname)s] %(message)s',
        level=logging.ERROR
    )
    log = logging.getLogger('mocp')
    log.setLevel(logging.INFO)

    try:
        MocNotify().run()
    except KeyboardInterrupt:
        pass
