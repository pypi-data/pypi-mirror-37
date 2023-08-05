class Webserver(object):
    def __init__(self, machine, webapp_root_path, webapp_name):
        self._machine = machine
        self._webapp_name = webapp_name
        self._webapp_root_path = webapp_root_path

    def restart_server(self):
        raise NotImplementedError("Subclass responsibility.")

    def configure_server(self):
        raise NotImplementedError("Subclass responsibility.")

    def _webapp_root_path(self):
        return self._webapp_root_path
