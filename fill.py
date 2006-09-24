#!/usr/bin/env python
#
# Generate the SIP specification files for C++ templates.

from boilerplate import head, keywords, sip_spec_for, tail
import os
import sys

QWT_ARRAY_BASE = {}

QWT_ARRAY_BASE['qwt5qt3'] = r'''
class %(ARRAY)s
{

%%TypeHeaderCode%(HEAD)s
%%End // %%TypeHeaderCode

public:
    %(ARRAY)s();
    %(ARRAY)s(int);
    %(ARRAY)s(const %(ARRAY)s &);
    %(ARRAY)s(SIP_PYOBJECT); 
%%MethodCode
    QwtArray<%(ITEM)s> array;
    // Numeric is not thread-safe
    if (-1 == try_PyObject_to_QwtArray(a0, array))
        return 0;

    sipCpp = new %(ARRAY)s(array);
%%End // %(ARRAY)s()
    ~%(ARRAY)s(); 
    // not possible: QwtArray<type> &operator=(const QArray<type> &); 
    // not Pythonic: type *data() const;
    // not Pythonic: uint nrefs() const; 
    uint size() const;
    uint count() const;
    bool isEmpty() const;
    bool isNull() const;
    bool resize(uint);
    bool truncate(uint);
    bool fill(const %(ITEM)s, int = -1);
    void detach();
    %(ARRAY)s copy() const;
    %(ARRAY)s & assign(const %(ARRAY)s &);
    // not Pythonic: QwtArray<type> & assign(const type *, uint); 
    %(ARRAY)s & duplicate(const %(ARRAY)s &);
    // not Pythonic: QwtArray<type> & duplicate(const type *, uint); 
    // not Pythonic: QwtArray<type> & setRawData(const type *, uint);
    // not Pythonic: void resetRawData(const type *, uint);
    int find(const %(ITEM)s &, uint = 0) const;
    int contains(const %(ITEM)s &) const;
    void sort();
    int bsearch(const %(ITEM)s &) const;
    // see __getitem__: type & operator[](int) const;
    %(ITEM)s /* & */ at(uint) const;
    // pulls in unwanted operators: bool operator==(const %(ARRAY)s &) const;
    // pulls in unwanted operators: bool operator!=(const %(ARRAY)s &) const;
    // No iterators, yet: Iterator begin();
    // No iterators, yet: Iterator end();
    // No iterators, yet: ConstIterator begin() const;
    // No iterators, yet: ConstIterator end() const;

    %(ITEM)s __getitem__(int);
%%MethodCode
    int len = sipCpp -> size();
    
    if (0 > (a0 = sipConvertFromSequenceIndex(a0, len)))
        sipIsErr = 1;
    else
        sipRes = (*sipCpp)[a0];
%%End // __getitem__()

    int __len__() const;
%%MethodCode
    sipRes = sipCpp -> size();
%%End // __len__()

    void __setitem__(int, %(ITEM)s);
%%MethodCode
    int len = sipCpp -> size();

    if (0 > (a0 = sipConvertFromSequenceIndex(a0, len)))
        sipIsErr = 1;
    else
        (*sipCpp)[a0] = a1;
%%End // __setitem__()

    void __setitem__(SIP_PYSLICE, const %(ARRAY)s &);
%%MethodCode
    int len = sipCpp -> size();
    Py_ssize_t start, stop, step, slicelength;

    if (0 > sipConvertFromSliceObject(a0, len,
                                      &start, &stop, &step, &slicelength))
        sipIsErr = 1;
    else {
        int vlen = a1 -> size();

        if (vlen != slicelength) {
            sipBadLengthForSlice(vlen, slicelength);
            sipIsErr = 1;
        } else {
            %(ARRAY)s::ConstIterator it = a1 -> begin();

            for (int i = 0; i < slicelength; ++i) {
                (*sipCpp)[int(start)] = *it;
                start += step;
                ++it;
            }
        }
    }
%%End // __setitem__()

}; // class %(ARRAY)s
'''

QWT_ARRAY_BASE['qwt4qt3'] = QWT_ARRAY_BASE['qwt5qt3']

QWT_ARRAY_BASE['qwt5qt4'] =  r'''
class %(ARRAY)s
{

%%TypeHeaderCode%(HEAD)s
%%End // %%TypeHeaderCode

public:
    %(ARRAY)s();
    %(ARRAY)s(int);
    %(ARRAY)s(const %(ARRAY)s &);
    %(ARRAY)s(SIP_PYOBJECT); 
%%MethodCode
    QwtArray<%(ITEM)s> array;
    // Numeric is not thread-safe
    if (-1 == try_PyObject_to_QwtArray(a0, array))
        return 0;

    sipCpp = new %(ARRAY)s(array);
%%End // %(ARRAY)s()
    ~%(ARRAY)s(); 
    // not possible: QwtArray<T> &operator=(const QwtArray<T> &);
    // pulls in unwanted operators: bool operator==(const QVector<T> &) const;
    // pulls in unwanted operators: bool operator!=(const QVector<T> &) const;
    int size() const;
    bool isEmpty() const;
    void resize(int);
    int capacity() const;
    void reserve(int);
    void squeeze();
    void detach();
    bool isDetached() const;
    void setSharable(bool sharable);
    // not Pythonic: T *data();
    // not Pythonic: const T *data() const;
    // not Pythonic: const T *constData() const;
    void clear();

    %(ITEM)s __getitem__(int);
%%MethodCode
    int len = sipCpp -> size();
    
    if (0 > (a0 = sipConvertFromSequenceIndex(a0, len)))
        sipIsErr = 1;
    else
        sipRes = (*sipCpp)[a0];
%%End // __getitem__()

    int __len__() const;
%%MethodCode
    sipRes = sipCpp -> size();
%%End // __len__()

    void __setitem__(int, %(ITEM)s);
%%MethodCode
    int len = sipCpp -> size();

    if (0 > (a0 = sipConvertFromSequenceIndex(a0, len)))
        sipIsErr = 1;
    else
        (*sipCpp)[a0] = a1;
%%End // __setitem__()

    void __setitem__(SIP_PYSLICE, const %(ARRAY)s &);
%%MethodCode
    int len = sipCpp -> size();
    Py_ssize_t start, stop, step, slicelength;

    if (0 > sipConvertFromSliceObject(a0, len,
                                      &start, &stop, &step, &slicelength))
        sipIsErr = 1;
    else {
        int vlen = a1 -> size();

        if (vlen != slicelength) {
            sipBadLengthForSlice(vlen, slicelength);
            sipIsErr = 1;
        } else {
            %(ARRAY)s::ConstIterator it = a1 -> begin();

            for (int i = 0; i < slicelength; ++i) {
                (*sipCpp)[int(start)] = *it;
                start += step;
                ++it;
            }
        }
    }
%%End // __setitem__()

}; // class %(ARRAY)s
'''

QWT_ARRAY_USER = {}
    
QWT_ARRAY_USER['qwt5qt3'] = r'''
class %(ARRAY)s
{

%%TypeHeaderCode%(HEAD)s
%%End // %%TypeHeaderCode

public:
    %(ARRAY)s();
    %(ARRAY)s(int);
    %(ARRAY)s(const %(ARRAY)s &);
    %(ARRAY)s(SIP_PYLIST); 
%%MethodCode
    QwtArray<%(ITEM)s> array(PyList_GET_SIZE(a0));

    int failed = 0;
    for (int i = 0; i < PyList_GET_SIZE(a0); ++i) {
        %(ITEM)s *item =
            reinterpret_cast<%(ITEM)s *>(
                sipForceConvertTo_%(FORCE)s(
                    PyList_GET_ITEM(a0, i), &failed));
                    
        if (failed) {
            return 0;
        }

        array[i] = *item;
    }

    sipCpp = new %(ARRAY)s(array);
%%End // %(ARRAY)s()

    // not Pythonic: type *data() const;
    // not Pythonic: uint nrefs() const;

    uint size() const;
    uint count() const;
    bool isEmpty() const;
    bool isNull() const;
    bool resize(uint);
    bool truncate(uint);
    bool fill(const %(ITEM)s, int = -1);
    void detach();
    %(ARRAY)s copy() const;
    %(ARRAY)s & assign(const %(ARRAY)s &);
    // not Pythonic: QwtArray<type> & assign(const type *, uint); 
    %(ARRAY)s & duplicate(const %(ARRAY)s &);
    // not Pythonic: QwtArray<type> & duplicate(const type *, uint); 
    // not Pythonic: QwtArray<type> & setRawData(const type *, uint);
    // not Pythonic: void resetRawData(const type *, uint);
    int find(const %(ITEM)s &, uint = 0) const;
    int contains(const %(ITEM)s &) const;
    void sort();
    int bsearch(const %(ITEM)s &) const;
    // see __getitem__: type & operator[](int) const;
    %(ITEM)s & at(uint) const;
    // pulls in unwanted operators: bool operator==(const %(ARRAY)s &) const;
    // pulls in unwanted operators: bool operator!=(const %(ARRAY)s &) const;
    // No iterators, yet: Iterator begin();
    // No iterators, yet: Iterator end();
    // No iterators, yet: ConstIterator begin() const;
    // No iterators, yes: ConstIterator end() const;

    %(ITEM)s & __getitem__(int);
%%MethodCode
    int len = sipCpp -> size();
    
    if (0 > (a0 = sipConvertFromSequenceIndex(a0, len)))
        sipIsErr = 1;
    else
        sipRes = &(*sipCpp)[a0];
%%End // __getitem__()

    int __len__() const;
%%MethodCode
    sipRes = sipCpp -> size();
%%End // __len__()

    void __setitem__(int, %(ITEM)s);
%%MethodCode
    int len = sipCpp -> size();

    if (0 > (a0 = sipConvertFromSequenceIndex(a0, len)))
        sipIsErr = 1;
    else
        (*sipCpp)[a0] = *a1;
%%End // __setitem__()

    void __setitem__(SIP_PYSLICE, const %(ARRAY)s &);
%%MethodCode
    int len = sipCpp -> size();
    Py_ssize_t start, stop, step, slicelength;

    if (0 > sipConvertFromSliceObject(a0, len,
                                      &start, &stop, &step, &slicelength))
        sipIsErr = 1;
    else {
        int vlen = a1 -> size();

        if (vlen != slicelength) {
            sipBadLengthForSlice(vlen, slicelength);
            sipIsErr = 1;
        } else {
            %(ARRAY)s::ConstIterator it = a1 -> begin();

            for (int i = 0; i < slicelength; ++i) {
                (*sipCpp)[int(start)] = *it;
                start += step;
                ++it;
            }
        }
    }
%%End // __setitem__()

}; // class %(ARRAY)s
'''

QWT_ARRAY_USER['qwt4qt3'] = QWT_ARRAY_USER['qwt5qt3']

QWT_ARRAY_USER['qwt5qt4'] = r'''
class %(ARRAY)s
{

%%TypeHeaderCode%(HEAD)s
%%End // %%TypeHeaderCode

public:
    %(ARRAY)s();
    %(ARRAY)s(int);
    %(ARRAY)s(const %(ARRAY)s &);
    %(ARRAY)s(SIP_PYLIST); 
%%MethodCode
    QwtArray<%(ITEM)s> array(PyList_GET_SIZE(a0));

    int failed = 0;
    for (int i = 0; i < PyList_GET_SIZE(a0); ++i) {
        %(ITEM)s *item =
            reinterpret_cast<%(ITEM)s *>(
                sipForceConvertTo_%(FORCE)s(
                    PyList_GET_ITEM(a0, i), &failed));
                    
        if (failed) {
            return 0;
        }

        array[i] = *item;
    }

    sipCpp = new %(ARRAY)s(array);
%%End // %(ARRAY)s()
    ~%(ARRAY)s(); 
    // not possible: QwtArray<T> &operator=(const QwtArray<T> &);
    // pulls in unwanted operators: bool operator==(const QVector<T> &) const;
    // pulls in unwanted operators: bool operator!=(const QVector<T> &) const;
    int size() const;
    bool isEmpty() const;
    void resize(int);
    int capacity() const;
    void reserve(int);
    void squeeze();
    void detach();
    bool isDetached() const;
    void setSharable(bool sharable);
    // not Pythonic: T *data();
    // not Pythonic: const T *data() const;
    // not Pythonic: const T *constData() const;
    void clear();

    %(ITEM)s & __getitem__(int);
%%MethodCode
    int len = sipCpp -> size();
    
    if (0 > (a0 = sipConvertFromSequenceIndex(a0, len)))
        sipIsErr = 1;
    else
        sipRes = &(*sipCpp)[a0];
%%End // __getitem__()

    int __len__() const;
%%MethodCode
    sipRes = sipCpp -> size();
%%End // __len__()

    void __setitem__(int, %(ITEM)s);
%%MethodCode
    int len = sipCpp -> size();

    if (0 > (a0 = sipConvertFromSequenceIndex(a0, len)))
        sipIsErr = 1;
    else
        (*sipCpp)[a0] = *a1;
%%End // __setitem__()

    void __setitem__(SIP_PYSLICE, const %(ARRAY)s &);
%%MethodCode
    int len = sipCpp -> size();
    Py_ssize_t start, stop, step, slicelength;

    if (0 > sipConvertFromSliceObject(a0, len,
                                      &start, &stop, &step, &slicelength))
        sipIsErr = 1;
    else {
        int vlen = a1 -> size();

        if (vlen != slicelength) {
            sipBadLengthForSlice(vlen, slicelength);
            sipIsErr = 1;
        } else {
            %(ARRAY)s::ConstIterator it = a1 -> begin();

            for (int i = 0; i < slicelength; ++i) {
                (*sipCpp)[int(start)] = *it;
                start += step;
                ++it;
            }
        }
    }
%%End // __setitem__()

}; // class %(ARRAY)s
'''


def main(qwt):
    file = open(os.path.join(
        'sip', qwt, 'QwtArrayDouble.sip'), 'w')
    keywords['description'] = sip_spec_for(['QwtArrayDouble'])
    print >> file, head % keywords
    print >> file, QWT_ARRAY_BASE[qwt] % {
        'HEAD': ('\n#include <qwt_array.h>'          
                 '\ntypedef QwtArray<double> QwtArrayDouble;'
                 ),
        'ITEM': 'double',
        'ARRAY': 'QwtArrayDouble',
        }
    print >> file, tail

    file = open(os.path.join(
        'sip', qwt, 'QwtArrayInt.sip'), 'w')
    keywords['description'] = sip_spec_for(['QwtArrayInt'])
    print >> file, head % keywords
    print >> file, QWT_ARRAY_BASE[qwt] % {
        'HEAD': ('\n#include <qwt_array.h>'          
                 '\ntypedef QwtArray<int> QwtArrayInt;'
                 ),
        'ITEM': 'int',
        'ARRAY': 'QwtArrayInt',
        }
    print >> file, tail

    if qwt == 'qwt4qt3':
        file = open(os.path.join(
            'sip', qwt, 'QwtArrayLong.sip'), 'w')
        keywords['description'] = sip_spec_for(['QwtArrayLong'])
        print >> file, head % keywords
        print >> file, QWT_ARRAY_BASE[qwt] % {
            'HEAD': ('\n#include <qwt_array.h>'
                     '\ntypedef QwtArray<long> QwtArrayLong;'
                     ),
            'ITEM': 'long',
            'ARRAY': 'QwtArrayLong',
            }
        print >> file, tail

    if qwt in ['qwt4qt3', 'qwt5qt3']:
        file = open(os.path.join(
            'sip', qwt, 'QwtArrayQwtDoublePoint.sip'), 'w')
        keywords['description'] = sip_spec_for(['QwtArrayDoublePoint'])
        print >> file, head % keywords
        print >> file, QWT_ARRAY_USER[qwt] % {
            'HEAD': ('\n#include <qwt_array.h>'
                     '\n#include <qwt_double_rect.h>'
                     '\ntypedef QwtArray<QwtDoublePoint>'
                     ' QwtArrayQwtDoublePoint;'
                     ),
            'ITEM': 'QwtDoublePoint',
            'ARRAY': 'QwtArrayQwtDoublePoint',
            'FORCE': 'QwtDoublePoint',
            }
        print >> file, tail

    if qwt == 'qwt5qt4':
        file = open(os.path.join(
            'sip', qwt, 'QwtArrayQwtDoublePoint.sip'), 'w')
        keywords['description'] = sip_spec_for(['QwtArrayDoublePoint'])
        print >> file, head % keywords
        print >> file, QWT_ARRAY_USER[qwt] % {
            'HEAD': ('\n#include <qwt_array.h>'
                     '\n#include <qpoint.h>'
                     '\ntypedef QwtArray<QPointF>'
                     ' QwtArrayQwtDoublePoint;'
                     ),
            'ITEM': 'QPointF',
            'ARRAY': 'QwtArrayQwtDoublePoint',
            'FORCE': 'QPointF',
            }
        print >> file, tail

# main()

if __name__ == '__main__':
    try:
        if sys.argv[1] in ['qwt5qt3', 'qwt5qt4']:
            main(sys.argv[1])
        else:
            raise IndexError
    except IndexError:
        print 'Usage: ./fill qwt5qt3'
        print 'or   : ./fill qwt5qt4'
        raise SystemExit


# Local Variables: ***
# mode: python ***
# End: ***
