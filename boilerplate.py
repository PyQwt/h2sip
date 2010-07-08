#!/usr/bin/env python

import os

head = '''%(description)s
%(copyright)s
// This file is part of %(package)s.
//
// %(package)s is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 2
// of the License, or (at your option) any later version.
//
// %(package)s is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License along
// with %(package)s; if not, write to the Free Software Foundation, Inc.,
// 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
//
// In addition, as a special exception, Gerard Vermeulen gives permission
// to link %(package)s dynamically with non-free versions of Qt and PyQt,
// and to distribute %(package)s in this form, provided that equally powerful
// versions of Qt and PyQt have been released under the terms of the GNU
// General Public License.
//
// If %(package)s is dynamically linked with non-free versions of Qt and PyQt,
// %(package)s becomes a free plug-in for a non-free program.
'''

keywords = {}

keywords['copyright'] = '''//
// Copyright (C) 2001-2010 Gerard Vermeulen
// Copyright (C) 2000 Mark Colclough
//'''

keywords['description'] = '''// What is this for?
'''

keywords['package'] = 'PyQwt'

tail = '''// Local Variables:
// mode: C++
// c-file-style: "stroustrup"
// indent-tabs-mode: nil
// End:
'''

def sip_spec_for(contents):
    return os.linesep.join([
        '// The SIP interface specification for:',
        '//      %s.' % (',%s//      ' % os.linesep).join(contents)
        ])

# sip_spec_for()


def main():
    print head % keywords
    print tail

# main()


if __name__ == '__main__':
    main()

# Local Variables: ***
# mode: python ***
# End: ***
