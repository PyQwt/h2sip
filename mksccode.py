import sys
import sip


class Wrapper:
    def __init__(self, type):
        self.type = type
        self.superclass = None
        self.subclasses = []
        self.index = -1


def dump_tree(base=None, indent=-1):
    if base:
        print "%s%s" % ("    " * indent, base.__name__)
        scl = wrappers[base].subclasses
    else:
        scl = base_wrappers

    for w in scl:
        dump_tree(w.type, indent + 1)


def output():
    def output_pass1(scl, index=0):
        for w in scl:
            w.index = index
            index += 1

        for w in scl:
            index = output_pass1(w.subclasses, index)

        return index

    def output_pass2(scl):
        for w in scl:
            name = w.type.__name__

            if w.subclasses:
                yes = w.subclasses[0].index
            else:
                yes = -1

            if w.superclass is None:
                if base_wrappers[-1] is w:
                    no = -1
                else:
                    no = w.index + 1
            elif w.superclass.subclasses[-1] is w:
                no = -1
            else:
                no = w.index + 1

            print "        {sipName_%s, &sipClass_%s, %d, %d}," % (name, name, yes, no)

        for w in scl:
            output_pass2(w.subclasses)

    print "%ConvertToSubClassCode"
    print "    static struct class_graph {"
    print "        char *name;"
    print "        sipWrapperType **type;"
    print "        int yes, no;"
    print "    } graph[] = {"

    output_pass1(base_wrappers)
    output_pass2(base_wrappers)

    print "    };"
    print "    int i = 0;"
    print "    sipClass = NULL;"
    print "    do {"
    print "        struct class_graph *cg = &graph[i];"
    print "        if (cg->name != NULL && sipCpp->inherits(cg->name)) {"
    print "            sipClass = *cg->type;"
    print "            i = cg->yes;"
    print "        } else {"
    print "            i = cg->no;"
    print "        }"
    print "    } while (i >= 0);"
    print "%End"


def import_module(name):
    mod = __import__(name)
    for chunk in name.split('.')[1:]:
        mod = getattr(mod, chunk)
    return mod    


argv = sys.argv[1:]

if argv and argv[0] == "-d":
    dump = True
    argv = argv[1:]
else:
    dump = False

if len(argv) > 1:
    print "Usage: %s [-d] module" % sys.argv[0]
    sys.exit(1)

mod = import_module(argv[0])

wrappers = {}

for o in mod.__dict__.values():
    if type(o) is sip.wrappertype:
        for sup in o.__mro__[1:]:
            if sup.__name__ == "QObject":
                wrappers[o] = Wrapper(o)
                break

base_wrappers = []

for w in wrappers.values():
    parent = w.type.__mro__[1]

    try:
        w.superclass = wrappers[parent]
    except KeyError:
        base_wrappers.append(w)
    else:
        wrappers[parent].subclasses.append(w)

if dump:
    dump_tree()
else:
    output()

