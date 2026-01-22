import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import terminatorlib.plugin as plugin
from terminatorlib.config import Config
from terminatorlib.factory import Factory
from terminatorlib.plugin import KeyBindUtil
from terminatorlib.terminator import Terminator

# AVAILABLE must contain a list of all the classes that you want exposed
AVAILABLE = ['BalanceSplitsPlugin']


PLUGIN_ACT_BALANCE = 'plugin_balance_splits'
PLUGIN_DESC_BALANCE = 'Balance Splits'
PLUGIN_DEFAULT_KEY = '<Shift><Control>b'


class BalanceSplitsPlugin(plugin.MenuItem):
    capabilities = ['terminal_menu']

    def __init__(self):
        plugin.MenuItem.__init__(self)
        config = Config()
        self.keyb = KeyBindUtil(config)
        self.keyb.bindkey_check_config(
            [PLUGIN_DESC_BALANCE, PLUGIN_ACT_BALANCE, PLUGIN_DEFAULT_KEY]
        )

        self._window_handlers = {}
        self._refresh_connections()

    def _active_root(self, terminal):
        window = terminal.get_toplevel()
        if window is None:
            return None

        root = window.get_child()
        maker = Factory()
        if maker.isinstance(root, 'Notebook'):
            page_num = root.get_current_page()
            if page_num < 0:
                return None
            return root.get_nth_page(page_num)
        return root

    def _balance_root(self, terminal):
        if terminal is None:
            return
        root = self._active_root(terminal)
        maker = Factory()
        if root and (maker.isinstance(root, 'HPaned') or maker.isinstance(root, 'VPaned')):
            root.do_redistribute(False, True)

    def do_balance(self, _menuitem, terminal):
        self._balance_root(terminal)

    def _on_keypress(self, widget, event):
        act = self.keyb.keyaction(event)
        if act != PLUGIN_ACT_BALANCE:
            return False

        terminal = widget.get_focussed_terminal()
        if terminal is None:
            terminal = Terminator().last_focused_term
        self._balance_root(terminal)
        return True

    def _refresh_connections(self):
        windows = Terminator().get_windows()
        for window in windows:
            if window not in self._window_handlers:
                handler_id = window.connect('key-press-event', self._on_keypress)
                self._window_handlers[window] = handler_id
        return False

    def callback(self, menuitems, _menu, terminal):
        item = Gtk.MenuItem(label='Balance Splits')
        item.connect('activate', self.do_balance, terminal)

        root = self._active_root(terminal)
        maker = Factory()
        has_splits = root and (maker.isinstance(root, 'HPaned') or maker.isinstance(root, 'VPaned'))
        item.set_sensitive(bool(has_splits))

        menuitems.append(item)

    def unload(self):
        for window, handler_id in list(self._window_handlers.items()):
            try:
                window.disconnect(handler_id)
            except Exception:
                pass
        self._window_handlers.clear()

        self.keyb.unbindkey([PLUGIN_DESC_BALANCE, PLUGIN_ACT_BALANCE, PLUGIN_DEFAULT_KEY])
