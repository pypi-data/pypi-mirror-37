#!coding:utf-8
import sys
import argparse
import functools
import inspect
from collections import Iterable


def singleton(cls):
    instances = {}

    @functools.wraps(cls)
    def getinstance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return getinstance


def chain(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kw):
        func(self, *args, **kw)
        return self

    return wrapper


class arg_map(object):
    def __init__(self):
        self.map = []
        self._index = 0

    def __str__(self):
        return str(self.map)

    def __repr__(self):
        return str(self.map)

    def __getitem__(self, key):
        return self.map[key]

    def __next__(self):
        for i in self.map:
            return i

    @property
    def len(self):
        return self._index

    @chain
    def set(self, name=None, **kw):
        """
        Code:
            > map = arg_map()
            > map.set(name='asdf', foo=1, boo=2, coo=3)
            > map
            [{'name':'asdf', 'foo':1, 'boo':2, 'coo'=3}]
        """
        if name:
            self.map.append(dict(name=name, **kw))
            self._index += 1

    @chain
    def set_all(self, map):
        """
        Code:
            > map = arg_map().set_all([
                {'name':'asdf', 'fun':1, 'foo':34},
                {'name':'zxcv', 'fun':2, 'hoo':78},
                {'name':'zxcv', 'boo':3, 'hoo':88}
            ])

            > map
            [
                {'name':'asdf', 'fun':1, 'foo':34},
                {'name':'zxcv', 'fun':2, 'hoo':78},
                {'name':'zxcv', 'boo':3, 'hoo':88}
            ])

        """
        if map and type(map) == list:
            self.map = map
            self._index = len(map)

    def get(self, key="name", value=None, boolFunc=None):
        """ 
        Code:
            > map = arg_map().set_all([
                {'name':'asdf', 'fun':1, 'foo':34},
                {'name':'zxcv', 'fun':2, 'foo':78},
                {'name':'zxcv', 'boo':3, 'hoo':88}
            ])

            > map.get('name', 'asdf')
            [{'name':'asdf', 'fun':1, 'foo':34}]

            > map.get('name', boolFunc=lambda x: 'hoo' in x and x['hoo']==88)
            [{'name':'zxcv', 'boo':3, 'hoo':88}]
        """
        if not value:
            if not boolFunc:
                return self.search(key)
            else:
                return [i for i in self.search(key) if boolFunc(i)]
        else:
            if not boolFunc:
                return [i for i in self.search(key) if i[key] == value]
            else:
                return [i for i in self.search(key) if i[key] == value and boolFunc(i)]

    def get_leaf(self, key="name", value=None, boolFunc=None, leaf=None):
        """ 
        Code:
            > map = arg_map().set_all([
                {'name':'asdf', 'fun':1, 'foo':34},
                {'name':'zxcv', 'fun':2, 'hoo':78},
                {'name':'zxcv', 'boo':3, 'hoo':88}
            ])

            > map.get('name', 'zxcv')
            [{'name':'zxcv', 'fun':2, 'hoo':78},{'name':'zxcv', 'boo':3, 'hoo':88}]

            > map.get_leaf('name', 'zxcv', leaf='hoo')
            [78, 88]

            > map.get_leaf('fun')
            [['asdf', 1, 34], ['zxcv', 2, 78]]

            > map.get_leaf('fun', leaf='name')
            ['asdf', 'zxcv']
        """
        i = self.get(key=key, value=value, boolFunc=boolFunc)
        if not leaf:
            ret = []
            for d in i:
                ret.append([d[k] for k in d])
            return ret
        else:
            return [d[leaf] for d in i if leaf in d]

    def search(self, key):
        """ 
        Code:
            > map = arg_map().set_all([
                {'name':'asdf', 'fun':1, 'foo':34},
                {'name':'fdas', 'fun':2, 'foo':78},
                {'name':'zxcv', 'boo':3, 'hoo':88}
            ])

            > map.search('boo')
            [{'name':'zxcv', 'boo':3, 'hoo':88}]
        """
        ret = []
        if self.map:
            for d in self.map:
                if key in d:
                    ret.append(d)
        return ret

    def search_leaf(self, leaf):
        """ 
        Code:
            > map = arg_map().set_all([
                {'name':'asdf', 'fun':1, 'foo':34},
                {'name':'fdas', 'fun':2, 'foo':78},
                {'name':'zxcv', 'boo':3, 'hoo':88}
            ])

            > map.search_leaf(88)
            [{'name':'zxcv', 'boo':3, 'hoo':88}]
        """
        ret = []
        if self.map:
            for d in self.map:
                for k in d:
                    if leaf == d[k]:
                        ret.append(d)
        return ret

    @chain
    def add(self, name_key, name_value, key, value=None):
        """
        Code:
            > map = arg_map().set_all([
                {'name':'asdf', 'fun':1, 'foo':34},
                {'name':'zxcv', 'fun':2, 'hoo':78},
                {'name':'zxcv', 'boo':3, 'hoo':88}
            ])

            > map.add('name', 'asdf', 'coo', 11)
            [
                {'name':'asdf', 'fun':1, 'foo':34, 'coo':11},
                {'name':'zxcv', 'fun':2, 'hoo':78},
                {'name':'zxcv', 'boo':3, 'hoo':88}
            ]

            > map.add('name', 'zxcv', 'doo', 22)
            [
                {'name':'asdf', 'fun':1, 'foo':34, 'coo':11},
                {'name':'zxcv', 'fun':2, 'hoo':78, 'doo':22},
                {'name':'zxcv', 'boo':3, 'hoo':88, 'doo':22}
            ]
        """
        for i in self.map:
            if name_key in i and name_value == i[name_key]:
                if key not in i:
                    i[key] = value
                else:
                    i[key] += value

    @chain
    def change_type(self, name_key, name_value, key, t=None):
        """
        Code:
            > map = arg_map().set_all([
                {'name':'asdf', 'fun':1, 'foo':[34, 35]},
                {'name':'zxcv', 'fun':2, 'hoo':78},
                {'name':'zxcv', 'boo':3, 'hoo':88}
            ])

            > map.change_type('name', 'asdf', 'foo', str)
            [
                {'name':'asdf', 'fun':1, 'foo':['34', '35']},
                {'name':'zxcv', 'fun':2, 'hoo':78},
                {'name':'zxcv', 'boo':3, 'hoo':88}
            ]
        """
        if t:
            for i in self.map:
                if name_key in i and key in i and i[name_key] == name_value:
                    if type(i[key]) == list:
                        for k in range(len(i[key])):
                            i[key][k] = t(i[key][k])
                    else:
                        i[key] = t(i[key])

    def sort(self, key=None, reverse=False):
        """
        Code:
            > map = arg_map().set_all([
                {'name':'asdf', 'fun':1, 'foo':34},
                {'name':'fdas', 'fun':2, 'hoo':78},
                {'name':'zxcv', 'boo':3, 'hoo':88}
            ])

            > map.sort(key=lambda x: x['name'])
            [
                {'name':'asdf', 'fun':1, 'foo':34},
                {'name':'fdas', 'fun':2, 'hoo':78},
                {'name':'zxcv', 'boo':3, 'hoo':88}
            ]

            > map.sort(key=lambda x: x['name'], reverse=True)
            [
                {'name':'zxcv', 'boo':3, 'hoo':88},
                {'name':'fdas', 'fun':2, 'hoo':78},
                {'name':'asdf', 'fun':1, 'foo':34}
            ]
        """
        return sorted(self.map, reverse=reverse, key=key)


@singleton
class cmd(object):
    def __init__(self, description="", parser=None, debug=False):
        self.description = description
        self.parser = parser or argparse.ArgumentParser(description=self.description)
        self.map = arg_map()
        self.func_map = arg_map()
        self.debug = debug

    @chain
    def add_argument(self, *args, **kw):
        self.parser.add_argument(*args, **kw)

    @chain
    def set_defaults(self, *args, **kw):
        self.parser.set_defaults(*args, **kw)

    def parse_args(self, *args, **kw):
        return self.parser.parse_args(*args, **kw)

    def args(
        self, short_name, long_name=None, nargs=1, help=None, action="store", type=None
    ):
        """ Accept cmd argument and map as *args to decorated function """

        def decorator(func):
            if long_name:
                self.map.set(
                    name=long_name.strip("-"),
                    func=func,
                    func_name=func.__name__,
                    short_name=short_name,
                    long_name=long_name,
                    nargs=nargs,
                    help=help,
                    action=action,
                    type=type,
                )
            else:
                self.map.set(
                    name=short_name.strip("-"),
                    func=func,
                    func_name=func.__name__,
                    short_name=short_name,
                    long_name=long_name,
                    nargs=nargs,
                    help=help,
                    action=action,
                    type=type,
                )

            @functools.wraps(func)
            def wrapper(*args, **kw):
                return func(*args, **kw)

            return wrapper

        return decorator

    def kwargs(self, nargs=1, help=None, action="store", type=None, **kw_options):
        """ Accept cmd argument and map as **kwargs to decorated function """

        def decorator(func):
            if kw_options:
                for i in kw_options:
                    self.map.set(
                        name=kw_options[i].strip("-"),
                        func=func,
                        func_name=func.__name__,
                        short_name=kw_options[i],
                        long_name=None,
                        nargs=nargs,
                        help=help,
                        action=action,
                        type=type,
                        kw_options=kw_options,
                    )

            @functools.wraps(func)
            def wrapper(*args, **kw):
                return func(*args, **kw)

            return wrapper

        return decorator

    def mark(self, run_order=None):
        def decorator(func):
            if run_order:
                self.map.add("func_name", func.__name__, "run_order", run_order)

            @functools.wraps(func)
            def wrapper(*args, **kw):
                return func(*args, **kw)

            return wrapper

        return decorator

    def _gen_cmd_args(self):
        # generate cmd interface
        for i in self.map:
            if i["short_name"] and i["long_name"]:
                self.parser.add_argument(
                    i["short_name"],
                    i["long_name"],
                    nargs=i["nargs"],
                    help=i["help"],
                    action=i["action"],
                )
            elif i["short_name"] and not i["long_name"]:
                self.parser.add_argument(
                    i["short_name"], help=i["help"], action=i["action"]
                )
        # get cmd args
        parser_args = self.parser.parse_args()
        cmd_args = {k: v for k, v in vars(parser_args).items() if v is not None}

        self.func_map.set("cmd_args", cmd_args=cmd_args)
        return cmd_args

    def _gen_func_set(self, cmd_args=None):
        if cmd_args:
            # add args to self.map and change return value type
            for i in cmd_args:
                self.map.add("name", i, "args", cmd_args[i])
                t = self.map.get_leaf("name", i, leaf="type")[0]
                self.map.change_type("name", i, "args", t)

            # get unique function name which have cmd deco decorated
            func_set = list(set(self.map.get_leaf(leaf="func_name")))

            self.func_map.set("func_set", func_set=func_set)
            return func_set

    def _gen_func_map(self, func_set=None):
        if func_set:

            for i in func_set:
                j = self.map.get("func_name", i)
                if j:
                    func_args = []
                    func_kwargs = {}

                    # collecte function args, add to func_args/func_kwargs
                    for k in j:
                        if "args" in k:
                            if "kw_options" in k:
                                for u, v in k["kw_options"].items():
                                    func_kwargs[u] = k["args"]
                            else:
                                if (
                                    isinstance(k["args"], Iterable)
                                    and not type(k["args"]) == str
                                ):
                                    func_args += list(k["args"])
                                else:
                                    func_args.append(k["args"])

                    # add self, if use in class
                    if "self" in inspect.getfullargspec(j[0]["func"]).args:
                        func_args = ["self"] + func_args

                    # add run_order to func_map
                    if func_args or func_kwargs:
                        if "run_order" in j[0]:
                            self.func_map.set(
                                i,
                                func_obj=j[0]["func"],
                                args=func_args,
                                kwargs=func_kwargs,
                                run_order=j[0]["run_order"],
                            )
                        else:
                            self.func_map.set(
                                i,
                                func_obj=j[0]["func"],
                                args=func_args,
                                kwargs=func_kwargs,
                            )

    def run(self):

        cmd_args = self._gen_cmd_args()
        # if not self.map.map, then no decorator used
        if cmd_args and self.map.map:
            func_set = self._gen_func_set(cmd_args)
            self._gen_func_map(func_set)

            if not self.debug:
                # run function in order to run_order value
                if self.func_map.get_leaf("run_order"):
                    for i in sorted(
                        self.func_map.get("func_obj"),
                        key=lambda x: x["run_order"],
                        reverse=True,
                    ):
                        i["func_obj"](*i["args"], **i["kwargs"])
                else:
                    for i in self.func_map.get("func_obj"):
                        i["func_obj"](*i["args"], **i["kwargs"])
            else:
                self._debug()
        else:
            return self.parser.parse_args()

    def _debug(self, debug_str="debug>"):
        if self.debug:

            flag = True
            while flag:
                i = input(debug_str)

                if i == "exit" or i == "0":
                    flag = False
                else:
                    if i == "func_map" or i == "1":
                        print(self.func_map)
                    elif i == "func_set" or i == "2":
                        print(self.func_map.get_leaf("func_set", leaf="func_set")[0])
                    elif i == "func_args" or i == "3":
                        print(self.func_map.get_leaf("args", leaf="args")[0])
                    elif i == "cmd_args" or i == "4":
                        print(self.func_map.get_leaf("cmd_args", leaf="cmd_args")[0])
                    elif i == "map" or i == "5":
                        print(self.map)
                    elif i == "run" or i == "6":
                        if self.func_map.get_leaf("run_order"):
                            for i in sorted(
                                self.func_map.get("func_obj"),
                                key=lambda x: x["run_order"],
                                reverse=True,
                            ):
                                i["func_obj"](*i["args"], **i["kwargs"])
                        else:
                            for i in self.func_map.get("func_obj"):
                                i["func_obj"](*i["args"], **i["kwargs"])
                    else:
                        print(
                            "options: 0:exit 1:func_map 2:func_set 3:func_args 4:cmd_args 5:map 6:run"
                        )
