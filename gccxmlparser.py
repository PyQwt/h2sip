#!/usr/bin/env python

debug = 0
import pprint

from copy import deepcopy

from cElementTree import *
from declaration import *

#------------------------------------------------------------------------------

class InvalidXmlError(Exception): pass
class ParserError(Exception): pass
class InvalidContextError(ParserError): pass


class GccXmlParser(object):

    def parse(self, filename):
        self.elements = self.parse_xml_file(filename)
        self.declarations = []
        self.names = {}
        if debug > 1:
            pprint.pprint(self.elements)
        for id in self.elements:
            element, declaration = self.elements[id]
            if declaration is None:
                try:
                    self.parseElement(id, element)
                except InvalidContextError:
                    pass # ignore nodes with invalid context (gccxml bug)
        
    # parse()

    def parse_xml_file(self, filename):
        tree = ElementTree(file=filename)
        root = tree.getroot()

        if root.tag != 'GCC_XML':
            raise RuntimeError, 'Not a vailid GCC_XML file'

        elements = {}
        type2typedef = {}
        for element in root:
            id = element.get('id')
            if id:
                elements[id] = element, None
                if element.tag == 'Typedef':
                    type2typedef[element.get('type')] = id
        for element in root:
            if element.tag != 'PointerType':
                continue
            type_t = element.get('type')
            if type2typedef.has_key(type_t):
                type_element, _ = elements[type_t]
                if type_element.tag == 'FunctionType':
                    element.set('type', type2typedef[type_t])
        return elements
    
    # parse_xml_file()

    def addDeclaration(self, declaration):
        if declaration.fullName() in self.names:
            declaration.is_unique = False
            for d in self.declarations:
                if d.fullName() == declaration.fullName():
                    d.is_unique = False
        self.names[declaration.fullName()] = 0
        self.declarations.append(declaration)

    # addDeclaration()

    def getArguments(self, element):
        arguments = []
        for child in element:
            if child.tag == 'Argument':
                type_t = self.getType(child.get('type'))
                type_t.default = child.get('default')
                arguments.append(type_t)
        return arguments

    # getArguments()

    def getDeclaration(self, id):
        if id not in self.elements:
            if id == '_0':
                raise InvalidContextError, 'Invalid context in the xml file.'
            else:
                raise ParserError, 'Failed to find %s in elements.' % id
                
        element, declaration = self.elements[id]
        if declaration is None:
            self.parseElement(id, element)
            element, declaration = self.elements[id]
            if declaration is None:
                raise ParserError, 'Failed to parse element: %s' % element.tag
            
        return declaration

    # getDeclaration()

    def getExceptions(self, exception_list):
        if exception_list is None:
            return None

        exceptions = []
        for t in exception_list.split():
            exceptions.append(self.getType(t))

        return exceptions

    # getExceptions()

    def getHierarchy(self, bases):
        if bases is None:
            return []
        base_names = bases.split()
        this_level = []
        next_levels = []
        for base in base_names:
            split = base.split(':')
            if len(split) == 2:
                visibility = split[0]
                base = split[1]
            else:
                visibility = Scope.public
            declaration = self.getDeclaration(base)
            if not isinstance(declaration, Class):
                continue
            base = Base(declaration.fullName(), visibility)
            this_level.append(base)
            # normalize with the other levels
            for index, level in enumerate(declaration.hierarchy):
                if index < len(next_levels):
                    next_levels[index] = next_levels[index] + level
                else:
                    next_levels.append(level)
        hierarchy = []
        if this_level:
            hierarchy.append(tuple(this_level))
        if next_levels:
            hierarchy.extend(next_levels)
        return hierarchy

    # getHierarchy()

    def getLocation(self, location):
        file, line = location.split(':')
        file = self.getDeclaration(file)
        return file, int(line)
    
    # getLocation()

    def getMembers(self, member_list):
        if member_list is None:
            return []
        members = []
        for member in member_list.split():
            declaration = self.getDeclaration(member)
            if type(declaration) in Class.validMemberTypes():
                members.append(declaration)
        return members

    # getMembers()
    
    def getType(self, id):

        def check(id, feature):
            pos = id.find(feature)
            if pos != -1:
                id = id[:pos] + id[pos+1:]
                return True, id
            else:
                return False, id

        const, id = check(id, 'c')
        volatile, id = check(id, 'v')
        restricted, id = check(id, 'r')

        declaration = self.getDeclaration(id)
        if isinstance(declaration, Type):
            result = deepcopy(declaration)
            if const:
                result.const = const
            if volatile:
                result.volatile = volatile
            if restricted:
                result.restricted = restricted
        else:
            result = Type(declaration.fullName(), const)
            result.volatile = volatile
            result.restricted = restricted

        return result

    # getType()

    def update(self, id, declaration):
        element, _ = self.elements[id]
        #pprint.pprint((id, element, declaration))
        self.elements[id] = element, declaration

    # update()

    def parseElement(self, id, element):
        method = 'parse' + element.tag
        if hasattr(self, method):
            func = getattr(self, method)
            func(id, element)
        else:
            #print method
            self.parseUnknown(id, element)

    # parseElement()

    def parseArrayType(self, id, element):
        type = self.getType(element.get('type'))
        min = element.get('min')
        max = element.get('max')
        array = ArrayType(type.name, type.const, min, max)
        self.update(id, array)

    # parseArrayType()
    
    def parseFunctionType(self, id, element):
        result = self.getType(element.get('returns'))
        args = self.getArguments(element)
        func = FunctionType(result, args)
        self.update(id, func)

    # parseFunctionType()

    def parseClass(self, id, element):
        #pprint.pprint((self.parseClass, element))
        name = element.get('name')
        abstract = bool(int(element.get('abstract', '0')))
        location = self.getLocation(element.get('location'))
        context = self.getDeclaration(element.get('context'))
        incomplete = bool(int(element.get('incomplete', 0)))
        if isinstance(context, str):
            klass = Class(name, context, [], abstract)
        else:
            visibility = element.get('access', Scope.public)
            klass = NestedClass(
                name, context.fullName(), visibility, [], abstract)
        klass.incomplete = incomplete
        self.addDeclaration(klass)
        klass.location = location
        self.update(id, klass)
        klass.hierarchy = self.getHierarchy(element.get('bases'))
        if klass.hierarchy:
            klass.bases = klass.hierarchy[0]
        members = self.getMembers(element.get('members'))
        for member in members:
            klass.addMember(member)

    # parseClass()
    
    def parseConstructor(self, id, element):
        name = element.get('name')
        visibility = element.get('access', Scope.public)
        classname = self.getDeclaration(element.get('context')).fullName()
        location = self.getLocation(element.get('location'))
        parameters = self.getArguments(element)
        artificial = element.get('artificial', False)
        if not artificial:
            constructor = Constructor(name, classname, parameters, visibility)
        else:
            # we don't want artificial constructors
            constructor = Unknown('__Unknown_Element_%s' % id)
        constructor.location = location
        self.update(id, constructor)

    # parseConstructor()

    def parseConverter(self, id, element):
        self.parseMethod(id, element, ConverterOperator)

    # parseConverter()

    def parseDestructor(self, id, element):
        name = element.get('name')
        visibility = element.get('access', Scope.public)
        classname = self.getDeclaration(element.get('context')).fullName()
        virtual = bool(int(element.get('virtual', '0')))
        location = self.getLocation(element.get('location'))
        destructor = Destructor(name, classname, visibility, virtual)
        destructor.location = location
        self.update(id, destructor)

    # parseDestructor()

    def parseEnumeration(self, id, element):
        name = element.get('name')
        location = self.getLocation(element.get('location'))
        context = self.getDeclaration(element.get('context'))
        incomplete = bool(int(element.get('incomplete', 0)))
        if isinstance(context, str):
            enum = Enumeration(name, context)
        else:
            visibility = element.get('access', Scope.public)
            enum = ClassEnumeration(name, context.fullName(), visibility)
        self.addDeclaration(enum)
        enum.location = location
        for child in element:
            if child.tag == 'EnumValue':
                name = child.get('name')
                value = int(child.get('init'))
                enum.values[name] = value
        enum.incomplete = incomplete
        self.update(id, enum)

    # parseEnumeration()

    def parseField(self, id, element):
        name = element.get('name')
        visibility = element.get('access', Scope.public)
        classname = self.getDeclaration(element.get('context')).fullName()
        type = self.getType(element.get('type'))
        static = bool(int(element.get('extern', '0')))
        location = self.getLocation(element.get('location'))
        variable = ClassVariable(type, name, classname, visibility, static)
        variable.location = location
        self.update(id, variable)

    # parseField()
    
    def parseFile(self, id, element):
        filename = element.get('name')
        self.update(id, filename)

    # parseFile()

    def parseFundamentalType(self, id, element):
        name = element.get('name')
        replacements = {
            'long int': 'long',
            'long unsigned int': 'unsigned long',
            'short int': 'short',
            'short unsigned int': 'unsigned short',
            'unsigned int': 'unsigned',
            }
        name = replacements.get(name, name)
        type = FundamentalType(name)
        self.update(id, type)

    # parseFundamentalType()

    def parseMethod(self, id, element, methodType=Method):
        name = element.get('name')
        result = self.getType(element.get('returns'))
        classname = self.getDeclaration(element.get('context')).fullName()
        visibility = element.get('access', Scope.public)
        static = bool(int(element.get('static', '0')))
        virtual = bool(int(element.get('virtual', '0')))
        abstract = bool(int(element.get('pure_virtual', '0')))
        const = bool(int(element.get('const', '0')))
        location = self.getLocation(element.get('location'))
        throws = self.getExceptions(element.get('throw', None))
        parameters = self.getArguments(element)
        method = methodType(name, classname, result, parameters, visibility,
                            virtual, abstract, static, const, throws)
        method.location = location
        self.update(id, method)

    # parseMethod()

    def parseNamespace(self, id, element):
        namespace = element.get('name')
        context = element.get('context')
        if context:
            outer = self.getDeclaration(context)
            if not outer.endswith('::'):
                outer += '::'
            namespace = outer + namespace
        if namespace.startswith('::'):
            namespace = namespace[2:]
        self.update(id, namespace)

    # parseNameSpace()

    def parseOperatorMethod(self, id, element):
        self.parseMethod(id, element, ClassOperator)

    # parseOperatorMethod()

    def parsePointerType(self, id, element):
        type = self.getType(element.get('type'))
        expand = not isinstance(type, FunctionType)
        ref = PointerType(type.name, type.const, None, expand, type.suffix)
        self.update(id, ref)

    # parsePointerType()

    def parseStruct(self, id, element):
        self.parseClass(id, element)

    # parseStruct()

    def parseReferenceType(self, id, element):
        type = self.getType(element.get('type'))
        expand = not isinstance(type, FunctionType)
        ref = ReferenceType(type.name, type.const, None, expand, type.suffix)
        self.update(id, ref)

    # parseReference
    
    def parseTypedef(self, id, element):
        name = element.get('name')
        type = self.getType(element.get('type'))
        context = self.getDeclaration(element.get('context'))
        if isinstance(context, Class):
            context = context.fullName()
        typedef = Typedef(type, name, context)
        self.update(id, typedef)
        self.addDeclaration(typedef)

    # parseTypedef()

    def parseUnknown(self, id, element):
        # catches for instance Union, CvQualifiedType, ??
        if debug > 1:
            pprint.pprint(element.tag)
        name = '__Unknown_Element__%s' % id
        declaration = Unknown(name)
        self.update(id, declaration)

    # parseUnknown()
    
    def parseVariable(self, id, element):
        # in gcc_xml, a static Field is declared as a Variable,
        # so we check this and call the Field parser.
        context = self.getDeclaration(element.get('context'))
        if isinstance(context, Class):
            self.parseField(id, element)
            _, declaration = self.elements[id]
            declaration.static = True
        else:
            namespace = context
            name = element.get('name')
            type = self.getType(element.get('type'))
            location = self.getLocation(element.get('location'))
            variable = Variable(type, name, namespace)
            variable.location = location
            self.addDeclaration(variable)
            self.update(id, variable)

    # parseVariable()

# class GccXmlParser

def main():
    pass

# main()

if __name__ == '__main__':
    main()


# Local Variables: ***
# mode: python ***
# End: ***
    
        
