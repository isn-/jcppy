#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2015 Stanislav Ivochkin <isn@extrn.org>
# License: MIT (see LICENSE for details)

import jcppy.cpp as cpp
import jcppy.cpp.ast
import jcppy.cpp.struct
import jcppy.cpp.function

class Header(cpp.ast.AST):
    def __init__(self, name):
        super(Header, self).__init__(name)
        self._pragma_once = True
        self._include_guard = True
        self.functions = []
        self.classes = []

    @property
    def pragma_once(self):
        return self._pragma_once
    @pragma_once.setter
    def pragma_once(self, new):
        self._pragma_once = new

    @property
    def include_guard(self):
        return self._include_guard
    @include_guard.setter
    def include_guard(self, new):
        self._include_guard = new

    @property
    def includes(self):
        incs = set()
        for func in self.functions:
            for inc in func.includes:
                incs.add(inc)

        for cls in self.classes:
            for inc in cls.includes:
                incs.add(inc)

        return list(sorted(incs, key=lambda x: x.order))

    @property
    def include_guard_define(self):
        return self.name.upper().replace(".", "_").replace("/", "_") + "_"

    def write(self, out):
        out("/// @file {0}".format(self.name))
        out("/// @warning Generated by jcppy, not intended for editing")
        out("/// @copyright The MIT License (MIT)")
        out()
        if self.pragma_once:
            out("#pragma once")
        if self.include_guard:
            out("#ifndef {0}".format(self.include_guard_define))
            out("#define {0}".format(self.include_guard_define))
            out()

        if len(self.includes):
            for i in self.includes:
                i.write(out)

        ns_to_decl = {}
        for i in self.functions + self.classes:
            ns_to_decl.setdefault(i.namespace, []).append(i)

        def _write_ns(ns):
            if ns:
                ns.write_header(out)
                out()

            functions = [i for i in ns_to_decl[ns] if isinstance(i, cpp.function.Function)]
            classes = [i for i in ns_to_decl[ns] if isinstance(i, cpp.struct.Class)]
            for i in functions:
                i.write_declaration(out)

            if len(functions) and len(classes):
                out()

            for i in classes:
                i.write_declaration(out)

            if ns:
                out()
                ns.write_footer(out)

        if len(ns_to_decl.keys()) and len(self.includes):
            out()

        for ns in ns_to_decl.keys()[:-1]:
            _write_ns(ns)
            out()
        if len(ns_to_decl.keys()):
            _write_ns(ns_to_decl.keys()[-1])

        if len(ns_to_decl.keys()) and self.include_guard:
            out()

        if self.include_guard:
            out("#endif // {0}".format(self.include_guard_define))
