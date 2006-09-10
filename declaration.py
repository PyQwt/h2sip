#!/usr/bin/env python

import os

TAB = ' '*4

from xml2sip_config import *


class Declaration(object):

    def __init__(self, name, namespace):
        self.name = name
        self.namespace = namespace
        self.location = '', -1
        self.incomplete = False
        self.is_unique = True

    # __init__()

    def fullName(self):
        namespace = self.namespace or ''
        if namespace and not namespace.endswith('::'):
            namespace += '::'
        return namespace + self.name

    # fullName()

    def __repr__(self):
        return '<Declaration %s at %s>' % (self.fullName(), id(self))

    # __repr__

    def __str__(self):
        return 'Declaration of %s' % self.fullName()

    # __str__()

    def sipify(self, indent=''):
        raise NotImplementedError

    # sipify()

# class Declaration


class Scope:
    
    public = 'public'
    private = 'private'
    protected = 'protected'

# class Scope


class Base:
    
    def __init__(self, name, visibility=Scope.public):
        self.name = name
        self.visibility = visibility

    # __init__()

# class Base


class Class(Declaration):

    def __init__(self, name, namespace, members, abstract):
        Declaration.__init__(self, name, namespace)
        self.__members = members
        self.__member_names = {}
        self.abstract = abstract
        self.bases = ()
        self.hierarchy = ()
        self.operator = {}

    # __init__()

    def __iter__(self):
        return iter(self.__members)

    # __iter__()
    
    def constructors(self, publics_only=True):
        result = []
        for member in self:
            if isinstance(member, Constructor):
                if publics_only and member.visibility != Scope.public:
                    continue
                result.append(member)
        return result

    # constructors()

    def hasCopyConstructor(self):
        for constructor in self.constructors():
            if constructor.IsCopy():
                return True
        return False

    # hasCopyConstructors()

    def hasDefaultConstructor(self):
        for constructor in self.constructors():
            if constructor.IsDefault():
                return True
        return False

    # hasDefaultConstructors

    def addMember(self, member):
        if member.name in self.__member_names:
            member.is_unique = False
            for m in self:
                if m.name == member.name:
                    m.is_unique = False
        else:
            member.is_unique = True
        self.__member_names[member.name] = 1
        self.__members.append(member)
        if isinstance(member, ClassOperator):
            self.operator[member.name] = member

    # addMember()

    def validMemberTypes():
        return (NestedClass, Method, Constructor, Destructor, ClassVariable,
                ClassOperator, ConverterOperator, ClassEnumeration)

    validMemberTypes = staticmethod(validMemberTypes)

    # validMemberTypes()

    def qtfy(self, qt_access):
        #print qt_access
        for member in self.__members:
            _, line = member.location
            for qt_line, qt_visibility in qt_access:
                #print member.name, member.location
                #print line, qt_line, qt_visibility
                if qt_line <= line:
                    visibility = qt_visibility
                else:
                    break

            if visibility in ('Q_OBJECT', 'public', 'protected', 'private'):
                continue

            if ((visibility == 'public slots'
                 and member.visibility == 'public')
                or (visibility in ('protected slots', 'signals')
                    and member.visibility == 'protected')
                or (visibility == 'private slots'
                    and member.visibility == 'private')):
                member.visibility = visibility
            else:
                #print visibility, member.visibility
                raise ValueError, \
                      'Failed to match Qt- and C++-access specifiers' 

    # qtfy()
    
    def sipify(self, indent='', excluded_bases=[], typecode={}):
        if self.incomplete or self.name.startswith('._'):
            return ''
        
        chunks = []

        # annotate the class as abstract if:
        # - the class is abstract
        # - there are no pure virtual class operators or methods
        has_protected_virtual_destructor = False
        if self.abstract:
            annotations = ' /Abstract/'
            for member in self:
                if (type(member) in [ClassOperator,
                                     Method,
                                     ]
                    and member.abstract
                    #and member.visibility == Scope.public # Sip bug?
                    ):
                    annotations = ''
                if (type(member) in [Destructor]
                    and member.virtual
                    and member.visibility == Scope.protected
                    ):
                    has_protected_virtual_destructor = True
        else:
            annotations = ''


        # FIXME: must we make the private destructors more visible?
        for member in self: 
            if (type(member) in [Destructor]
                and member.visibility == Scope.private
                ):
                break

        bases = []
        for base in self.bases:
            if (base.visibility == Scope.private
                or base.name in excluded_bases
                ):
                pass
            else:
                bases.append(base)

        if bases:
            # FIXME: multiple inheritance?
            chunks.append('%sclass %s: %s%s' %
                          (indent, self.name,
                           ', '.join([base.name for base in self.bases]),
                           annotations))
        else:
            chunks.append('%sclass %s%s' % (indent, self.name, annotations))
        chunks.extend([
            '%s{' % indent, 
            '%TypeHeaderCode',
            '#include <%s>' % os.path.basename(self.location[0]),
            ])
        if self.name == 'SoQt':
            chunks.extend(['#include <qapplication.h>'])
        chunks.extend([
            '%End // %TypeHeaderCode',
            '',
            ])
        #chunks.append(typecode.get(self.name, ''))
        visibility = ''
        #print self.__members
        appendix = EXTRA.get(self.name, '')
        has_extra_destructor = (-1 != appendix.find('~%s' % self.name))
        #print has_extra_destructor, self.name
        for member in self.__members:
            if (member.visibility == 'protected'
                and type(member) in [NestedClass,
                                     ]
                ):
                continue
            if (member.visibility == 'private'
                and type(member) in [ClassEnumeration,
                                     NestedClass,
                                     ]
                ):
                continue
            if (member.visibility == 'private'
                and type(member) in [ClassOperator,
                                     Method,
                                     ]
                and not member.virtual # FIXME: virtual or abstract?
                ):
                continue

            if (type(member) in [Destructor]
                and has_extra_destructor
                ):
                continue
            
            chunk = member.sipify(indent + TAB)
                
            if chunk:
                if member.visibility != visibility:
                    chunks.append('%s%s:' % (indent, member.visibility))
                    visibility = member.visibility
                chunks.append(chunk)

        if appendix:
            chunks.append(appendix)
        chunks.extend([
            '%s}; // class %s' % (indent, self.name),
            '',
            ])
        return os.linesep.join(chunks)

    # sipify()
        
# class Class


class NestedClass(Class):

    def __init__(self, name, klass, visibility, members, abstract):
        Class.__init__(self, name, None, members, abstract)
        self.klass = klass
        self.visibility = visibility

    # __init__()

    def fullName(self):
        return '%s::%s' % (self.klass, self.name)

    # fullName()

# class NestedClass


class Enumeration(Declaration):

    def __init__(self, name, namespace):
        Declaration.__init__(self, name, namespace)
        self.values = {}

    # __init__()

    def ValueFullName(self, name):
        assert name in self.values
        namespace = self.namespace
        if namespace:
            namespace += '::'
        return namespace + name

    # valueFullName()

    def sipify(self, indent=''):
        names = [(int(value), name) for name, value in self.values.iteritems()]
        names.sort()
        names = [name for _, name in names]
        return '%s%s%s' % (
            '%senum %s {%s' % (indent, self.name, os.linesep),
            '%s' % (',%s%s%s' % (os.linesep, indent, TAB)).join(names),
            '%s%s}; // enum %s' % (os.linesep, indent, self.name))

    # sipify()
    
# class Enumeration


class ClassEnumeration(Enumeration):

    def __init__(self, name, klass, visibility):
        Enumeration.__init__(self, name, None)
        self.klass = klass
        self.visibility = visibility

    # __init__()

    def fullName(self):
        return '%s::%s' % (self.klass, self.name)

    # fullName()

    def valueFullName(self, name):
        assert name in self.values
        return '%s::%s' % (self.klass, name)

    # valueFullName()

    def sipify(self, indent=''):
        names = [(int(value), name) for name, value in self.values.iteritems()]
        names.sort()
        names = [name for _, name in names]
        if self.name.startswith('._'):
            enum = 'enum'
        else:
            enum =  'enum %s' % self.name
        return '%s%s%s' % (
            '%s%s {%s%s%s' % (indent, enum, os.linesep, indent, TAB),
            '%s' % (',%s%s%s' % (os.linesep, indent, TAB)).join(names),
            '%s%s}; // %s%s' % (os.linesep, indent, enum, os.linesep),
            )

    # sipify()

# class ClassEnumeration


class Function(Declaration):

    def __init__(self, name, namespace, result, parameters, throws=None):
        Declaration.__init__(self, name, namespace)
        # the result type: instance of Type, or None (constructors)
        self.result = result
        # the parameters: instances of Type
        self.parameters = parameters
        # the exception specification
        self.throws = throws

    # __init__()

    def exceptions(self):
        if self.throws is None:
            return ""
        else:
            return " throw(%s)" % ', '.join (
                [x.fullName() for x in self.throws]
                )

    # exception()

    def pointerDeclaration(self, force=False):
        if self.is_unique and not force:
            return '&%s' % self.fullName()
        else:
            result = self.result.fullName()
            params = ', '.join([x.fullName() for x in self.parameters])
            return '(%s (*)(%s)%s)&%s' % (
                result, params, self.exceptions(), self.fullName()
                )

    # pointerDeclaration()

    def minArgs(self):
        min = 0
        for arg in self.parameters:
            if arg.default is None:
                min += 1
        return min

    minArgs = property(minArgs)

    # minArgs()

    def maxArgs(self):
        return len(self.parameters)

    maxArgs = property(maxArgs)

    # maxArgs()

# class Function


class Method(Function):

    def __init__(self, name, klass, result, parameters, visibility,
                 virtual, abstract, static, const, throws=None):
        Function.__init__(self, name, None, result, parameters, throws)
        self.visibility = visibility
        self.virtual = virtual
        self.abstract = abstract
        self.static = static
        self.klass = klass
        self.const = const

    # __init__()

    def fullName(self):
        return self.klass + '::' + self.name

    # fullName()

    def pointerDeclaration(self, force=False):
        if self.static:
            # static methods are like normal functions
            return Function.pointerDeclaration(self, force)
        if self.is_unique and not force:
            return '&%s' % self.fullName()
        else:
            result = self.result.fullName()
            parameters = ', '.join([x.fullName() for x in self.parameters])
            if self.const:
                const = ' const'
            else:
                const = ''
            return '(%s (%s::*)(%s)%s%s)&%s' % (
                result, self.klass, parameters, const,
                self.exceptions(), self.fullName())

    # pointerDeclaration()

    def sipify(self, indent=''):
        if self.static:
            static = 'static '
        else:
            static = ''
            
        if self.virtual:
            virtual = 'virtual '
        else:
            virtual = ''

        if self.const:
            const = ' const'
        else:
            const = ''
            
        if self.abstract:
            abstract = ' = 0'
        else:
            abstract = ''

        fixme = ''
        annotations = ''
        signature = ''
        code = ''

        result = self.result.sipify()
        if result in RESULTS:
            fixme = '// FIXME: '

        body = []
        for parameter in self.parameters:
            chunk = parameter.sipify()
            body.append(chunk)

        for chunk in body:
            if chunk.split(' = ')[0] in ARGUMENTS:
                fixme = '// FIXME: '
                break;
                
        result = (
            '%s%s%s%s%s %s('
            '%s'
            ')%s%s%s%s;%s'
            ) % (
            indent, fixme, static, virtual, result, self.name,
            ', '.join(body),
            const, abstract, annotations, signature, code,
            )

        if result in QOBJECT:
            return ''

        return MEMBERS.get(self.klass, {}).get(result, result)
        
    # sipify()

# class Method


class ClassOperator(Method):
    
    def fullName(self):
        return self.klass + '::operator ' + self.name

    # fullName()

    def sipify(self, indent=''):
        if self.static:
            static = 'static '
        else:
            static = ''
            
        if self.virtual:
            virtual = 'virtual '
        else:
            virtual = ''

        fixme = ''
        slot = 'operator%s' % self.name
        if self.name in ['[]', '!']:
            fixme = '// FIXME: '
##         if self.name in ['*=', '+=', '-=', '/='] and not self.is_unique:
##             fixme = '// FIXME: '

        result = self.result.sipify()

        body = []
        for parameter in self.parameters:
            body.append(parameter.sipify())

##         print 'Operator: ', self.name, body
        
        if len(body) == 0:
            if self.name == '-':
                slot = '__neg__'

        if len(body) == 1:
            slot = {
                '+=': '__iadd__',
                '&=': '__iand__',
                '/=': '__idiv__',
                '<<=': '__ilshift__',
                '%=': '__imod__',
                '*=': '__imul__',
                '|=': '__ior__',
                '>>=': '__irshift__',
                '-=': '__isub__',
                '^=': '__ixor__',
                #'|': '__or__',
                }.get(self.name, slot)
            if not (slot == self.name or self.is_unique):
                if body[0] == 'int':
                    body[0] = 'int /Constrained/'
            
        body = ', '.join(body)

        if self.name in ['!', '=']:
            fixme = '// Not Pythonic: '

        head = '%s%s%s%s%s %s(' %  (
            indent, fixme, static, virtual, result, slot
            )

        if self.const:
            const = ' const'
        else:
            const = ''
            
        if self.abstract:
            abstract = ' = 0'
        else:
            abstract = ''

        tail = ')%s%s;' % (const, abstract)

        return '%s%s%s' % (head, body, tail)

    # sipify()

# class ClassOperator


class Constructor(Method):

    def __init__(self, name, klass, parameters, visibility):
        Method.__init__(self, name, klass, None, parameters, visibility,
                        False, False, False, False)

    # __init__()

    def isDefault(self):
        return len(self.parameters) == 0 and self.visibility == Scope.public

    # isDefault()
    
    def isCopy(self):
        if len(self.parameters) != 1:
            return False
        parameter = self.parameters[0]
        class_as_parameter = self.parameters[0].name == self.klass
        parameter_reference = isinstance(parameter, ReferenceType)
        is_public = self.visibility == Scope.public
        return (parameter_reference
                and class_as_parameter
                and parameter.const
                and is_public)

    # isCopy()

    def pointerDeclaration(self, force=False):
        return ''

    # pointerDeclaration()

    def sipify(self, indent=''):
        fixme = ''

        body = []
        for parameter in self.parameters:
            chunk = parameter.sipify()
            body.append(chunk)
        for chunk in body:
            if chunk.split(' = ')[0] in ARGUMENTS:
                fixme = '// FIXME: '
                break;
            
        head = '%s%s%s(' % (indent, fixme, self.name)            
        body = ', '.join(body)
        tail = ');'
        code = ''

        result = '%s%s%s%s' % (head, body, tail, code)

        result = MEMBERS.get(self.klass, {}).get(result, result)

        return result

    # sipify()

# class Constructor


class ConverterOperator(Method):
    
    def fullName(self):
        return self.klass + '::operator ' + self.name

    # fullName()

    def sipify(self, indent=''):
        if self.static:
            static = 'static '
        else:
            static = ''
            
        if self.virtual:
            virtual = 'virtual '
        else:
            virtual = ''

        fixme = '// Not Pythonic: '

        result = self.result.sipify()

        body = []
        for parameter in self.parameters:
            body.append(parameter.sipify())
            
        body = ', '.join(body)

        head = '%s%s%s%s%s %s(' %  (
            indent, fixme, static, virtual, result, self.name
            )

        if self.const:
            const = ' const'
        else:
            const = ''
            
        if self.abstract:
            abstract = ' = 0'
        else:
            abstract = ''

        tail = ')%s%s;' % (const, abstract)

        return '%s%s%s' % (head, body, tail)

    # sipify()

# class ConverterOperator


class Destructor(Method):

    def __init__(self, name, klass, visibility, virtual):
        Method.__init__(self, name, klass, None, [], visibility, virtual,
                        False, False, False)

    # __init__()

    def fullName(self):
        return self.klass + '::~' + self.name

    # fullName()

    def pointerDeclaration(self, force=False):
        return ''

    # pointerDeclaration()

    def sipify(self, indent=''):
        if self.virtual:
            virtual = 'virtual '
        else:
            virtual = ''
        if self.abstract:
            abstract = ' = 0'
        else:
            abstract = ''

        code = ''

        return '%s%s~%s()%s;%s' % (indent, virtual, self.name, abstract, code)

    # sipify()
    
# class Destructor


class Type(Declaration):

    def __init__(self, name, const=False, default=None, suffix=''):
        Declaration.__init__(self, name, None)
        self.const = const
        # function arguments
        self.default = default
        self.volatile = False
        self.restricted = False
        self.suffix = suffix

    # __init__()

    def __repr__(self):
        if self.const:
            const = 'const '
        else:
            const = ''
        return '<Type ' + const + self.name + '>'

    # __repr__()
    
    def fullName(self):
        if self.const:
            const = 'const '
        else:
            const = ''
        return const + self.name + self.suffix

    # fullName()

    def sipify(self, indent=''):
        if self.const:
            const = 'const '
        else:
            const = ''
            
        if self.default == None:
            default = ''
        else:
            default = ' = %s' % self.default
            default = DEFAULTS.get(default, default)

        name = self.name

        return '%s%s%s%s%s' % (
            indent, const, name, self.suffix, default
            )

    # sipify()

# class Type


class ArrayType(Type):

    def __init__(self, name, const, min, max):
        Type.__init__(self, name, const)
        self.min = min
        self.max = max

    # __init__()

    def sipify(self, indent=''):
        const = ''
        if self.const:
            const = 'const '

        return '%s%s%s[%s]' % (indent, const, self.name, 1+int(self.max))

    # sipify()

# class ArrayType


class FunctionType(Type):

    def __init__(self, result, parameters):
        Type.__init__(self, '', False)
        self.result = result
        self.parameters = parameters
        self.name = self.fullName()

    # __init__()

    def fullName(self):
        full = '%s (*)' % self.result.fullName()
        params = [x.fullName() for x in self.parameters]
        full += '(%s)' % ', '.join(params)
        return full

    # fullName()

# class FunctionType


class FundamentalType(Type):

    def __init__(self, name, const=False, default=None):
        Type.__init__(self, name, const, default)

    # __init__()

# class FundamentalType


class PointerType(Type):

    def __init__(
        self, name, const=False, default=None, expandPointer=False, suffix=''
        ):
        Type.__init__(self, name, const, default)
        if expandPointer:
            self.suffix = suffix + '*'

    # __init__()

# class PointerType


class ReferenceType(Type):

    def __init__(
        self, name, const=False, default=None, expandRef=True, suffix=''
        ):
        Type.__init__(self, name, const, default)
        if expandRef:
            self.suffix = suffix + '&'

    # __init__()

# class ReferenceType


class Typedef(Declaration):

    def __init__(self, type, name, namespace):
        Declaration.__init__(self, name, namespace)
        self.type = type
        self.visibility = Scope.public

    # __init__()

# class Typedef


class Unknown(Declaration):

    def __init__(self, name):
        Declaration.__init__(self, name, None)

    # __init__()

# class Unknown


class Variable(Declaration):

    def __init__(self, type, name, namespace):
        Declaration.__init__(self, name, namespace)
        self.type = type

    # __init__()

# class Variable


class ClassVariable(Variable):

    def __init__(self, type, name, klass, visibility, static):
        Variable.__init__(self, type, name, None)
        self.visibility = visibility
        self.static = static
        self.klass = klass

    # __init__()

    def fullName(self):
        return self.klass + '::' + self.name

    # fullName()

    def sipify(self, indent=''):
        if self.visibility in (Scope.protected, Scope.private):
            return ''

        static = ''
        if self.static:
            static = 'static '

        ctype =  self.type.sipify()

        result = '%s%s%s %s;' % (indent, static, ctype, self.name)

        result = MEMBERS.get(self.klass, {}).get(result, result)

        if result in QOBJECT:
            result = ''

        return result;

    # sipify()

# class ClassVariable

if __name__ == '__main__':

    pass

# Local Variables: ***
# mode: python ***
# End: ***
