

import sys

from ...session import KabaretSession

from qtpy import QtCore, QtWidgets
from .widgets.main_window import MainWindowManager
from .widgets.flow.flow_view import FlowView


class KabaretStandaloneGUISession(KabaretSession):

    def __init__(self, session_name='Standalone', tick_every_ms=10, debug=False):
        super(KabaretStandaloneGUISession, self).__init__(session_name, debug)
        self.main_window_manager = None
        self.tick_every_ms = tick_every_ms

    def is_gui(self):
        return True

    def create_window_manager(self):
        return MainWindowManager.create_window(self)
        
    def start(self):
        app = QtWidgets.QApplication(sys.argv)
        QtWidgets.QApplication.setOrganizationName("Supamonks")
        QtWidgets.QApplication.setApplicationName("Kabaret")
        self.main_window_manager = self.create_window_manager()
        self.main_window_manager.install()

        timer = QtCore.QTimer(self.main_window_manager.main_window)
        timer.timeout.connect(self.tick)
        timer.start(self.tick_every_ms)

        app.exec_()

    def register_view_types(self):
        '''
        Subclasses can register view types and create defaults view here.
        Use:
            self.main_window_manager.register()
            and
            self.main_window_manager.add_view()
        '''
        type_name = self.main_window_manager.register_view_type(FlowView)
        self.main_window_manager.add_view(type_name)

    def _on_cluster_connected(self):
        '''
        Overridden to also dispatch a 'cluster_connection' event to GUI.
        '''
        super(KabaretStandaloneGUISession, self)._on_cluster_connected()
        self.dispatch_event(
            'cluster_connection',
            cluter_name=self._cluster_actor.get_cluster_name()
        )

    def dispatch_event(self, event_type, **data):
        if self.main_window_manager is not None:
            self.main_window_manager.dispatch_event(event_type, data)
