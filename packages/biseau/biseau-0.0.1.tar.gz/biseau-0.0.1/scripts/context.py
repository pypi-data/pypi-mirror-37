# encoding: utf8
"""Widget helping user picking a formal context to use.

If the choosen file is in ASP format, the data will be output as-is.

"""

import os
import glob
import tempfile
import tkinter as tk
from tkinter import ttk

from biseau.gui import Runnable
from biseau.core import format_converters


CONTEXTS_GLOB = 'contexts/*.[ctxsvlp]*'


class Container(Runnable):

    NAME = 'Context Picker'
    TAGS = {'FCA', 'ASP', 'initial example'}
    INPUTS = {}
    OUTPUTS = {'rel/2'}


    def _run_on(self, previous_context:str):
        """Return the ASP source code describing the context"""
        if self.current_context:
            return previous_context + '\n\n% Context encoding\n' + self.current_context
        else:
            return previous_context + '\n\n% Context was not choosen by user.'


    def create_widgets(self):
        self.current_context = ''
        box_value = tk.StringVar(self, 'Pick one')
        self.box = ttk.Combobox(self, textvariable=box_value,
                                justify='left', state='readonly')
        self.update_box()
        self.box.bind("<<ComboboxSelected>>", self.newselection)
        self.box.grid(row=0, column=0, columnspan=2, padx=15)

        self.but_reloadbox = tk.Button(self, text='Reload', command=self.update_box)
        self.but_reloadbox.grid(row=0, column=2)

        return {}


    def newselection(self, _=None):
        if not os.path.exists(self.box.get()): return None
        self.current_context = self._compute_context(self.box.get())
        self.update()


    def update_box(self):
        self.box['values'] = tuple(sorted(glob.glob(CONTEXTS_GLOB)))
        self.newselection()  # trigger the change


    def _state_change(self, state):
        """Set in deactivated on in readonly"""
        self.box.configure(state={'normal': 'readonly'}.get(state, state))

    def _open_sources(self):
        return self.current_context

    def _edit_sources(self, new_context:str):
        self.current_context = str(new_context)


    def select(self, context_name:str):
        """API for master ; allow it to choose a context to open"""
        context = 'contexts/{}'.format(context_name)
        self.box.set(context)
        self.newselection()


    @staticmethod
    def _compute_context(fname:str) -> str:
        """Return the Context object describing the context in given file"""
        if not fname.endswith('.lp'):
            with tempfile.NamedTemporaryFile('w', suffix='.lp', delete=False) as fd:
                format_converters.convert(fname, fd.name)
                fname = fd.name
        with open(fname) as fd:
            return fd.read()
