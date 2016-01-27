# -*- coding: utf-8 -*-
#########################
#       TODOLIST        #
#########################


#########################
# IMPORTS               #
#########################
from munin.plugin import Plugin
import pickle
import re


class TodoList(Plugin):
    """
    Advanced Plugin application.
    """
    REGEX     = re.compile(r"\s*to?do? (.+)")
    FEATURES  = {} # dict of regex:method, initialized in __init__
    SAVE_FILE_SUFFIX  = '.tdl'
    SAVE_FILE_DEFAULT = 'default_todo_list'


    def __init__(self, bot, savefile=SAVE_FILE_DEFAULT):
        super().__init__(bot)
        self.savefile = savefile
        self.todolist = self.default_persistant_data()
        TodoList.FEATURES.update({ # useless, except in the first case of instanciation
            re.compile(r"a(?:dd)? +(.*)")               : TodoList.todolist_add,
            re.compile(r"c(?:heck)?((?:\s+\d+)+)")      : TodoList.todolist_check,
            re.compile(r"p(?:rint)? *")                 : TodoList.todolist_print,
            re.compile(r"s(?:ave)? *((?:[a-zA-Z0-9_])+)?.*") : TodoList.todolist_save,
            re.compile(r"l(?:oad)? *((?:[a-zA-Z0-9_])+)?.*") : TodoList.todolist_load,
            re.compile(r"clean|clear *")                : TodoList.todolist_clean,
        })
        # if possible, load the todolist from savefile
        self.__load_todolist()

    def __del__(self):
        """Save todolist in self.savefile file"""
        self.__save_todolist()


# PUBLIC METHODS ##############################################################
    def do_command(self, bot, message, matched_groups=None, sudo=False):
        """Execute command for bot (unused), according to regex matchs (used) and sudo mode (unused)"""
        if not sudo: return '' # sudo is needed
        results = ''
        command = matched_groups[0]
        for regex, feature in self.FEATURES.items():
            regres = regex.fullmatch(command)
            if regres is not None:  # match !
                results += feature(self, regres.groups()) or ''
        return results

    def todolist_add(self, matched_groups):
        """add received string to todo list"""
        self.todolist.append((matched_groups[0], False))
        return None

    def todolist_check(self, matched_groups):
        """check received items of todo list"""
        indexes = [int(_) for _ in matched_groups[0].split(' ') if _ is not '']
        self.todolist = [(item[0], idx in indexes or item[1]) for idx, item in enumerate(self.todolist)]
        return None

    def todolist_print(self, matched_groups):
        """return a print of todo list"""
        if len(self.todolist) == 0: return 'no item in current todolist'
        return '\n'.join(['\t' + str(i) + ': ' + item[0]
                          + (' \t[CHECK]' if item[1] else '')
                          for i, item in enumerate(self.todolist)
                         ])

    def todolist_save(self, matched_groups):
        """save todo list in self.savefile file"""
        filename = self.__save_todolist(filename=matched_groups[0])
        if filename is None:
            return 'todolist not saved !'
        else:
            return 'todolist saved as ' + filename

    def todolist_load(self, matched_groups):
        """save todo list in self.savefile file"""
        filename = self.__load_todolist(filename=matched_groups[0])
        if filename is None:
            return 'todolist not loaded !'
        else:
            return 'todolist ' + filename + ' loaded'

    def todolist_clean(self, matched_groups):
        """delete check elements of todo list"""
        self.todolist = [(todo, False) for todo, checked in self.todolist if not checked]
        return None


# PRIVATE METHODS #############################################################
    def __load_todolist(self, filename=None):
        """Load todolist from filename or self.savefile if possible. Erase self.todolist."""
        filename = filename if filename is not None else self.savefile
        try:
            with open(self.filename(filename), 'rb') as f:
                self.todolist = pickle.load(f)
        except:
            filename = None
        return filename

    def __save_todolist(self, filename=None):
        """Save todolist in filename or self.savefile if possible. Erase existing data in this file."""
        filename = filename if filename else self.savefile
        try:
            with open(self.filename(filename), 'wb') as f:
                pickle.dump(self.todolist, f)
        except (IOError, PermissionError):
            filename = None
        return filename

    @property
    def help(self):
        return """TODOLIST: wait for 'todo {add,print,check,clean,load,save}' command, for management of todo lists. Need sudo."""

    @property
    def debug_data(self):
        return self.todolist

    @property
    def persistent_data(self):
        return self.todolist

    @persistent_data.setter
    def persistent_data(self, values):
        self.todolist = values

    def default_persistant_data(self):
        """Return the default persistent data"""
        return [] # (str, bool) strings are things to do, bool is check predicat
