#!/usr/bin/env python


# argument types to be skipped
ARGUMENTS = [
    'void*',
    'const QMap<double,QMemArray<QwtDoublePoint> >&',
    'const QMap<double,QPolygonF>&',
    ]

# result types to be skipped
RESULTS = [
    # Qwt4
    #'QWidgetIntDictIt',
    #'QwtPlotCurveIterator',
    #'QwtPlotMarkerIterator',
    # Qwt4 and Qwt5
    'void*',
    'QMap<double,QMemArray<QwtDoublePoint> >', # Qt3
    'QMap<double,QPolygonF>', # Qt4
    ]

QOBJECT = [
    # Qt3
    '    virtual QMetaObject* metaObject() const;',
    '    virtual const char* className() const;',
    '    // FIXME: virtual void* qt_cast(const char*);',
    '    virtual bool qt_invoke(int, QUObject*);',
    '    virtual bool qt_emit(int, QUObject*);',
    '    virtual bool qt_property(int, int, QVariant*);',
    '    static bool qt_static_property(QObject*, int, int, QVariant*);',
    '    static QMetaObject* staticMetaObject();',
    '    QObject* qObject();',
    # Qt4.1
    '    static const QMetaObject staticMetaObject;',
    '    virtual const QMetaObject* metaObject() const;',
    '    // FIXME: virtual void* qt_metacast(const char*);',
    '    virtual int qt_metacall(QMetaObject::Call, int, void**);',
    '    static QString tr(const char*, const char* = 0);',
    '    static QString trUtf8(const char*, const char* = 0);',
    # Qt4.2
    '    static QString tr(const char*, const char*, int);',
    '    static QString trUtf8(const char*, const char*, int);',
    ]

DEFAULTS = {
    ' = Active': ' = QPalette::Active',
    ' = AutoText': ' = QwtText::AutoText',
    ' = BottomScale': ' = QwtScaleDraw::BottomScale',
    ' = Horizontal': ' = Qt::Horizontal',
    ' = NoButton': ' = Qt::NoButton',
    ' = QBrush(NoBrush)': ' = QBrush(Qt::NoBrush)',
    ' = QPen(NoPen)': ' = QPen(Qt::NoPen)',
    ' = RGB': ' = QwtColorMap::RGB',
    ' = Rtti_PlotItem': ' = QwtPlotItem::Rtti_PlotItem',
    ' = darkGray': ' = Qt::darkGray',            
    ' = gray': ' = Qt::gray',
    ' = red': ' = Qt::red',
    ' = white': ' = Qt::white',
    # FIXME: clean up integers
    ' = 0l': ' = 0',
    ' = -0x00000000000000001': ' = -1',
    ' = -0x000000001': ' = -1',
    }

MEMBERS =  { 
    'QwtAbstractScale':
    {'    void setScaleDraw(QwtScaleDraw*);':
     '    void setScaleDraw(QwtScaleDraw* /Transfer/);',
     
     '    void setScaleEngine(QwtScaleEngine*);':
     '    void setScaleEngine(QwtScaleEngine* /Transfer/);',
     
     '    void setAbstractScaleDraw(QwtAbstractScaleDraw*);':
     '    void setAbstractScaleDraw(QwtAbstractScaleDraw* /Transfer/);',
     },

    'QwtAbstractScaleDraw':
    {'    void setTransformation(QwtScaleTransformation*);':
     '    void setTransformation(QwtScaleTransformation* /Transfer/);',
     },

    'QwtAbstractSlider':
    {'    QwtAbstractSlider(Qt::Orientation, QWidget* = 0);':
     '    QwtAbstractSlider(Qt::Orientation, QWidget* /TransferThis/ = 0);',
     },

    'QwtAlphaColorMap':
    {'    QwtAlphaColorMap(const QColor& = QColor(((const QColor&)((const QColor*)Qt::gray))));':
     '    QwtAlphaColorMap(const QColor& = QColor(Qt::gray));',
     # Qt4
     '    QwtAlphaColorMap(const QColor& = QColor(gray));':
     '    QwtAlphaColorMap(const QColor& = QColor(Qt::gray));',
     },

    'QwtAnalogClock':
    {'    QwtAnalogClock(QWidget* = 0, const char* = 0);':
     '    QwtAnalogClock(QWidget* /TransferThis/ = 0, const char* = 0);',
     # Qwt5
     '    QwtAnalogClock(QWidget* = 0);':
     '    QwtAnalogClock(QWidget* /TransferThis/ = 0);',

     '    virtual void setHand(QwtAnalogClock::Hand, QwtDialNeedle*);':
     '    virtual void setHand(QwtAnalogClock::Hand, QwtDialNeedle* /Transfer/);',
     
     '    void setTime(const QTime& = QTime::currentTime()());':
     '    void setTime(const QTime& = QTime::currentTime());',

     '    virtual void setNeedle(QwtDialNeedle*);':
     '    virtual void setNeedle(QwtDialNeedle* /Transfer/);',
     },

    'QwtArrayData':
    {'    QwtArrayData(const double*, const double*, size_t);':
     r'''    QwtArrayData(SIP_PYOBJECT, SIP_PYOBJECT) [(const double*, const double*, size_t)];
%MethodCode
QwtArray<double> xArray;
if (-1 == try_PyObject_to_QwtArray(a0, xArray))
    return 0;

QwtArray<double> yArray;
if (-1 == try_PyObject_to_QwtArray(a1, yArray))
    return 0;

sipCpp = new sipQwtArrayData(xArray, yArray);
%End
''',

     '    virtual QwtData* copy() const;':
     '    virtual QwtData* copy() const /Factory/;',
     },

    'QwtArrowButton':
    {'    QwtArrowButton(int, Qt::ArrowType, QWidget*, const char* = 0);':
     '    QwtArrowButton(int, Qt::ArrowType, QWidget* /TransferThis/, const char* = 0);',
     # Qwt5
'    QwtArrowButton(int, Qt::ArrowType, QWidget* = 0);':
     '    QwtArrowButton(int, Qt::ArrowType, QWidget* /TransferThis/ = 0);',
     },

    'QwtAutoScale':
    {'    void adjust(double*, int, int = 0);':
     r'''    void adjust(SIP_PYOBJECT, int = 0);
%MethodCode
QwtArray<double> array;
if (-1 == try_PyObject_to_QwtArray(a0, array))
    return 0;

sipCpp->QwtAutoScale::adjust(array, a1);
%End
''',
     },

    'QwtCompass':
    {'    QwtCompass(QWidget* = 0, const char* = 0);':
     '    QwtCompass(QWidget* /TransferThis/ = 0, const char* = 0);',
     # Qwt5
     '    QwtCompass(QWidget* = 0);':
     '    QwtCompass(QWidget* /TransferThis/ = 0);',

     '    void setRose(QwtCompassRose*);':
     '    void setRose(QwtCompassRose* /Transfer/);',
     },

    'QwtCounter':
    {'    QwtCounter(QWidget* = 0, const char* = 0);':
     '    QwtCounter(QWidget* /TransferThis/ = 0, const char* = 0);',
     # Qwt5
     '    QwtCounter(QWidget* = 0);':
     '    QwtCounter(QWidget* /TransferThis/ = 0);',
     },

    'QwtCurve':
    {'    void setRawData(const double*, const double*, int);':
     '    // Not Pythonic: void setRawData(const double*, const double*, int);',

     '    void setData(const double*, const double*, int);':
     r'''    void setData(SIP_PYOBJECT, SIP_PYOBJECT);
%MethodCode
QwtArray<double> xArray;
if (-1 == try_PyObject_to_QwtArray(a0, xArray))
    return 0;

QwtArray<double> yArray;
if (-1 == try_PyObject_to_QwtArray(a1, yArray))
    return 0;

sipCpp->QwtCurve::setData(xArray, yArray);
%End
''',

     '    int verifyRange(int&, int&);':
     '    int verifyRange(int& /In,Out/, int& /In,Out/);',
     },

    'QwtData':
    {'    virtual QwtData* copy() const = 0;':
     '    virtual QwtData* copy() const = 0 /Factory/;',
     },

    'QwtDial':
    {'    QwtDial(QWidget* = 0, const char* = 0);':
     '    QwtDial(QWidget* /TransferThis/ = 0, const char* = 0);',
     # Qwt5
     '    QwtDial(QWidget* = 0);':
     '    QwtDial(QWidget* /TransferThis/ = 0);',

     '    virtual void setNeedle(QwtDialNeedle*);':
     '    virtual void setNeedle(QwtDialNeedle* /Transfer/);',

     '    virtual void setScaleDraw(QwtDialScaleDraw*);':
     '    virtual void setScaleDraw(QwtDialScaleDraw* /Transfer/);',

     '    virtual void getScrollMode(const QPoint&, int&, int&);':
     '    virtual void getScrollMode(const QPoint&, int& /Out/, int& /Out/);',
     },

    'QwtDiMap':
    {'    bool contains(int) const;':
     '    bool contains(int /Constrained/) const;',
     },

    'QwtDoublePoint':
    {'    double& rx();':
     '    double rx();',
     '    double& ry();':
     '    double ry();',
    },
    
    'QwtDoublePointData':
    {'    virtual QwtData* copy() const;':
     '    virtual QwtData* copy() const /Factory/;',
     },

    'QwtDoubleRect':
    {'    double& rx1();':
     '    double rx1();',

     '    double& rx2();':
     '    double rx2();',

     '    double& ry1();':
     '    double ry1();',

     '    double& ry2();':
     '    double ry2();',
     },

    'QwtDoubleSize':
    {'    double& rwidth();':
     '    double rwidth();',

     '    double& rheight();':
     '    double rheight();',
     },

    'QwtDynGridLayout':
    {'    QwtDynGridLayout(QWidget*, int = 0, int = -1, const char* = 0);':
     '    QwtDynGridLayout(QWidget* /TransferThis/, int = 0, int = -1, const char* = 0);',
     
     '    QwtDynGridLayout(QLayout*, int = -1, const char* = 0);':
     '    QwtDynGridLayout(QLayout* /TransferThis/, int = -1, const char* = 0);',
     # Qwt5
     '    QwtDynGridLayout(QWidget*, int = 0, int = -1);':
     '    QwtDynGridLayout(QWidget* /TransferThis/, int = 0, int = -1);',

     '    virtual void addItem(QLayoutItem*);':
     '    virtual void addItem(QLayoutItem* /Transfer/);',
     },

    'QwtEventPattern':
    {},
    
    'QwtKnob':
    {'    QwtKnob(QWidget* = 0, const char* = 0);':
     '    QwtKnob(QWidget* /TransferThis/ = 0, const char* = 0);',
     # Qwt5
     '    QwtKnob(QWidget* = 0);':
     '    QwtKnob(QWidget* /TransferThis/ = 0);',

     '    void setScaleDraw(QwtRoundScaleDraw*);':
     '    void setScaleDraw(QwtRoundScaleDraw* /Transfer/);',
     
     '    virtual void getScrollMode(const QPoint&, int&, int&);':
     '    virtual void getScrollMode(const QPoint&, int& /Out/, int& /Out/);',
     },

    'QwtLegend':
    {'    QwtLegend(QWidget* = 0, const char* = 0);':
     '    QwtLegend(QWidget* /TransferThis/ = 0, const char* = 0);',
     # Qwt5
     '    QwtLegend(QWidget* = 0);':
     '    QwtLegend(QWidget* /TransferThis/ = 0);',

     '    void insertItem(QWidget*, long);':
     '    void insertItem(QWidget* /Transfer/, long);',

     '    QWidget* takeItem(long);':
     '    QWidget* takeItem(long) /TransferBack/;',

     '    virtual QWidgetIntDictIt itemIterator() const;':
     '    /* FIXME: virtual */ QWidgetIntDictIt itemIterator() const;',
     
     '    void insert(const QwtPlotItem*, QWidget*);':
     '    void insert(const QwtPlotItem*, QWidget* /Transfer/);',
     },

    'QwtLegendButton':
    {'    QwtLegendButton(QWidget* = 0, const char* = 0);':
     '    QwtLegendButton(QWidget* /TransferThis/ = 0, const char* = 0);',

     '    QwtLegendButton(const QwtSymbol&, const QPen&, const QString&, QWidget* = 0, const char* = 0);':
     '    QwtLegendButton(const QwtSymbol&, const QPen&, const QString&, QWidget* /TransferThis/ = 0, const char* = 0);',
     },

    'QwtLegendItem':
    {'    QwtLegendItem(QWidget* = 0);':
     '    QwtLegendItem(QWidget* /TransferThis/ = 0);',
     
     '    QwtLegendItem(const QwtSymbol&, const QPen&, const QwtText&, QWidget* = 0);':
     '    QwtLegendItem(const QwtSymbol&, const QPen&, const QwtText&, QWidget* /TransferThis/ = 0);',
     },

    'QwtLinearScaleEngine':
    {'    virtual QwtScaleTransformation* transformation() const;':
     '    virtual QwtScaleTransformation* transformation() const /Factory/;',
     
     '    virtual void autoScale(int, double&, double&, double&) const;':
     '    virtual void autoScale(int, double& /In, Out/, double& /In, Out/, double&) const;',
     }, 

    'QwtLog10ScaleEngine':
    {'    virtual QwtScaleTransformation* transformation() const;':
     '    virtual QwtScaleTransformation* transformation() const /Factory/;',
     
     '    virtual void autoScale(int, double&, double&, double&) const;':
     '    virtual void autoScale(int, double& /In, Out/, double& /In, Out/, double&) const;',
     }, 

    'QwtMagnifier':
    {'    QwtMagnifier(QWidget*);':
     '    QwtMagnifier(QWidget* /TransferThis/);',
    },
    

    'QwtPicker':
    {'    QwtPicker(QWidget*, const char* = 0);':
     '    QwtPicker(QWidget* /TransferThis/, const char* = 0);',

     '    QwtPicker(int, QwtPicker::RubberBand, QwtPicker::DisplayMode, QWidget*, const char* = 0);':
     '    QwtPicker(int, QwtPicker::RubberBand, QwtPicker::DisplayMode, QWidget* /TransferThis/, const char* = 0);',

     '    QwtPicker(QWidget*);':
     '    QwtPicker(QWidget* /TransferThis/);',

     '    QwtPicker(int, QwtPicker::RubberBand, QwtPicker::DisplayMode, QWidget*);':
     '    QwtPicker(int, QwtPicker::RubberBand, QwtPicker::DisplayMode, QWidget* /TransferThis/);',

     '    virtual QwtPickerMachine* stateMachine(int) const;':
     '    virtual QwtPickerMachine* stateMachine(int) const /Factory/;',
     },

    'QwtPanner':
    {'    QwtPanner(QWidget*);':
     '    QwtPanner(QWidget* /TransferThis/);',
     },
     
    'QwtPlainText':
    {'    virtual QwtText* clone() const;':
     '    virtual QwtText* clone() const /Factory/;',
     },

    'QwtPlot':
    {'    QwtPlot(QWidget* = 0, const char* = 0);':
     '    QwtPlot(QWidget* /TransferThis/ = 0, const char* = 0);',
     
     '    QwtPlot(const QString&, QWidget* = 0, const char* = 0);':
     '    QwtPlot(const QString&, QWidget* /TransferThis/ = 0, const char* = 0);',
     # Qt4
     '    QwtPlot(QWidget* = 0);':
     '    QwtPlot(QWidget* /TransferThis/ = 0);',

     '    QwtPlot(const QwtText&, QWidget* = 0);':
     '    QwtPlot(const QwtText&, QWidget* /TransferThis/ = 0);',

     # Qwt4 and Qwt5
     '    void print(QPaintDevice&, const QwtPlotPrintFilter& = QwtPlotPrintFilter()) const;':
     '    void print(QPaintDevice&, const QwtPlotPrintFilter& = QwtPlotPrintFilter()) const /PyName=print_/;',

     '    virtual void print(QPainter*, const QRect&, const QwtPlotPrintFilter& = QwtPlotPrintFilter()) const;':
     '    virtual void print(QPainter*, const QRect&, const QwtPlotPrintFilter& = QwtPlotPrintFilter()) const /PyName=print_/;',

     '    void setAxisScaleEngine(int, QwtScaleEngine*);':
     '    void setAxisScaleEngine(int, QwtScaleEngine* /Transfer/);',

     '    void insertLegend(QwtLegend*, QwtPlot::LegendPosition = RightLegend, double = -1.0e+0);':
     '    void insertLegend(QwtLegend* /Transfer/, QwtPlot::LegendPosition = QwtPlot::RightLegend, double = -1);',

     '    void setAxisScaleDraw(int, QwtScaleDraw*);':
     '    void setAxisScaleDraw(int, QwtScaleDraw* /Transfer/);',

     '    long closestCurve(int, int, int&) const;':
     '    // FIXME: long closestCurve(int, int, int&) const;',

     '    long closestCurve(int, int, int&, double&, double&, int&) const;':
     '    long closestCurve(int, int, int& /Out/, double& /Out/, double& /Out/, int& /Out/) const;',
     
     # Qwt4
     '    bool setCurveRawData(long, const double*, const double*, int);':
     '    // Not Pythonic: bool setCurveRawData(long, const double*, const double*, int);',

     '    bool setCurveData(long, const double*, const double*, int);':
     r'''    bool setCurveData(long, SIP_PYOBJECT, SIP_PYOBJECT);
%MethodCode
QwtArray<double> xArray;
if (-1 == try_PyObject_to_QwtArray(a1, xArray))
    return 0;

QwtArray<double> yArray;
if (-1 == try_PyObject_to_QwtArray(a2, yArray))
    return 0;

sipRes = sipCpp->QwtPlot::setCurveData(a0, xArray, yArray);
%End
''',

     # Qwt4
     '    long closestMarker(int, int, int&) const;':
     '    long closestMarker(int, int, int& /Out/) const;',

     '    virtual void drawItems(QPainter*, const QRect&, const QwtScaleMap*, const QwtPlotPrintFilter&) const;':
     r'''    virtual void drawItems(QPainter*, const QRect&, SIP_PYLIST, const QwtPlotPrintFilter&) const [
        void (QPainter*, const QRect&, const QwtScaleMap*, const QwtPlotPrintFilter&)];
%MethodCode
        // PyQwt takes a list with QwtScaleMap objects in the first
        // QwtPlot::axisCnt elements.
        
        QwtScaleMap maps[QwtPlot::axisCnt];

        sipIsErr = QwtPlot::axisCnt > PyList_GET_SIZE(a2);

        if (!sipIsErr) {
            for (int i=0; i<QwtPlot::axisCnt; ++i) {
                void *cpp = sipForceConvertToInstance(
                    PyList_GET_ITEM(a2, i), sipClass_QwtScaleMap,
                    0, SIP_NO_CONVERTORS, 0, &sipIsErr);
                maps[i] = *reinterpret_cast<QwtScaleMap*>(cpp);
            }
        }

        if (!sipIsErr) {
            Py_BEGIN_ALLOW_THREADS
            sipCpp->sipProtectVirt_drawItems(sipSelfWasArg, a0, *a1, maps, *a3);
            Py_END_ALLOW_THREADS
        }
%End

%VirtualCatcherCode
        PyObject *maps = PyList_New(QwtPlot::axisCnt);

        sipIsErr = !maps;

        if (!sipIsErr) {
            for (int i=0; i<QwtPlot::axisCnt; ++i) {
                PyObject *object = sipConvertFromInstance(
                    const_cast<QwtScaleMap*>(&a2[i]), sipClass_QwtScaleMap, 0);
                if (!object) {
                    sipIsErr = true;
                    break;
                }
                PyList_SET_ITEM(maps, i, object);
            }
        }

        if (!sipIsErr) {
            PyObject *result = sipCallMethod(
                &sipIsErr, sipMethod, "CCSC",
                a0, sipClass_QPainter, 0,
                &a1, sipClass_QRect, 0,
                maps,
                &a3, sipClass_QwtPlotPrintFilter, 0);

            if (result)
            {
                sipParseResult(&sipIsErr, sipMethod, result, "Z");
                Py_DECREF(result);
            }
        }

        Py_XDECREF(maps);
%End
''',

     '    virtual void printCanvas(QPainter*, const QRect&, const QwtScaleMap*, const QwtPlotPrintFilter&) const;':
     r'''    virtual void printCanvas(QPainter*, const QRect&, SIP_PYLIST, const QwtPlotPrintFilter&) const [
     void (QPainter*, const QRect&, const QwtScaleMap*, const QwtPlotPrintFilter&)];
%MethodCode
        // PyQwt takes a list with QwtScaleMap objects in the first
        // QwtPlot::axisCnt elements.
        
        QwtScaleMap maps[QwtPlot::axisCnt];

        sipIsErr = QwtPlot::axisCnt > PyList_GET_SIZE(a2);

        if (!sipIsErr) {
            for (int i=0; i<QwtPlot::axisCnt; ++i) {
                void *cpp = sipForceConvertToInstance(
                    PyList_GET_ITEM(a2, i), sipClass_QwtScaleMap,
                    0, SIP_NO_CONVERTORS, 0, &sipIsErr);
                maps[i] = *reinterpret_cast<QwtScaleMap*>(cpp);
            }
        }

        if (!sipIsErr) {
            Py_BEGIN_ALLOW_THREADS
            sipCpp->sipProtectVirt_printCanvas(
                sipSelfWasArg, a0, *a1, maps, *a3);
            Py_END_ALLOW_THREADS
        }
End

%VirtualCatcherCode
        PyObject *maps = PyList_New(QwtPlot::axisCnt);

        sipIsErr = !maps;

        if (!sipIsErr) {
            for (int i=0; i<QwtPlot::axisCnt; ++i) {
                PyObject *object = sipConvertFromInstance(
                    const_cast<QwtScaleMap*>(&a2[i]), sipClass_QwtScaleMap, 0);
                if (!object) {
                    sipIsErr = true;
                    break;
                }
                PyList_SET_ITEM(maps, i, object);
            }
        }

        if (!sipIsErr) {
            PyObject *result = sipCallMethod(
                &sipIsErr, sipMethod, "CCSC",
                a0, sipClass_QPainter, 0,
                &a1, sipClass_QRect, 0,
                maps,
                &a3, sipClass_QwtPrintFilter, 0);

            if (result)
            {
                sipParseResult(&sipIsErr, sipMethod, result, "Z");
                Py_DECREF(result);
            }
        }

        Py_XDECREF(maps);
%End
''',
     },

    'QwtPlotCanvas':
    {'    QwtPlotCanvas(QwtPlot*);': # Qwt5
     '    QwtPlotCanvas(QwtPlot* /TransferThis/);',
     },

    'QwtPlotCurve':
    {'    QwtPlotCurve(QwtPlot*, const QString& = QString::null);':
     '    QwtPlotCurve(QwtPlot* /TransferThis/, const QString& = QString::null);',

     '    void setData(const double*, const double*, int);':
     r'''    void setData(SIP_PYOBJECT, SIP_PYOBJECT);
%MethodCode
QwtArray<double> xArray;
if (-1 == try_PyObject_to_QwtArray(a0, xArray))
    return 0;

QwtArray<double> yArray;
if (-1 == try_PyObject_to_QwtArray(a1, yArray))
    return 0;

sipCpp->QwtPlotCurve::setData(xArray, yArray);
%End
''',

     '    void setRawData(const double*, const double*, int);':
     '    // Not Pythonic: void setRawData(const double*, const double*, int);',
     # Fix ErrorBarDemo?
     '    virtual void draw(QPainter*, const QwtScaleMap&, const QwtScaleMap&, int, int) const;':
     '    virtual void draw(QPainter*, const QwtScaleMap&, const QwtScaleMap&, int, int) const /PyName=drawFromTo/;',

     '    int verifyRange(int&, int&) const;':
     '    int verifyRange(int& /In,Out/, int& /In,Out/) const;',

     '    void setCurveFitter(QwtCurveFitter*);':
     '    void setCurveFitter(QwtCurveFitter* /Transfer/);',
     },

    'QwtPlotGrid':
    {'    QwtPlotGrid(QwtPlot*);':
     '    QwtPlotGrid(QwtPlot* /TransferThis/);',
     },

    'QwtPlotItem':
    {'    QwtPlotItem(QwtPlot*, bool = TRUE);': # Qwt4
     '    QwtPlotItem(QwtPlot* /TransferThis/, bool = TRUE);',

     # Qwt5
     '    QwtPlotItem(const QwtText& = QwtText(((const QString&)(& QString::null)), AutoText));':
     '    QwtPlotItem(const QwtText& = QwtText(QString::null, QwtText::AutoText));',
     
     '    QwtPlotItem(const QwtText& = QwtText(((const QString&)(& QString(((const QString::Null&)(& QString::null))))), AutoText));':
     '    QwtPlotItem(const QwtText& = QwtText(QString::null, QwtText::AutoText));',

     # Qwt5     
     '    void attach(QwtPlot*);':
     '    void attach(QwtPlot* /TransferThis/);',
     # Qwt5     

     '    void detach();':
     r'''    void detach();
%MethodCode
sipCpp->QwtPlotItem::detach();
sipTransferBack(sipSelf);
%End
''',
     },

    'QwtPlotLayout':
    {'    void expandLineBreaks(int, const QRect&, int&, int*) const;':
     r'''    SIP_PYTUPLE expandLineBreaks(int, const QRect&) const [
        void (int, const QRect&, int&, int*)];
%MethodCode
int title, axes[QwtPlot::axisCnt];
sipCpp->sipProtect_expandLineBreaks(a0, *a1, title, axes);
sipRes = Py_BuildValue("i(iiii)", title, axes[0], axes[1], axes[2], axes[3]);
%End
''',

     '    void alignScales(int, QRect&, QRect*) const;':
     r'''    SIP_PYTUPLE alignScales(int, QRect&) const [
        void (int, QRect&, QRect*)];
%MethodCode
QRect scales[QwtPlot::axisCnt];
sipCpp->sipProtect_alignScales(a0, *a1, scales);
sipRes = sipBuildResult(0, "(BBBB)",
                        new QRect(scales[0]), sipClass_QRect, 0,
                        new QRect(scales[1]), sipClass_QRect, 0,
                        new QRect(scales[2]), sipClass_QRect, 0,
                        new QRect(scales[3]), sipClass_QRect, 0);
%End
''',
     },

    'QwtPlotMagnifier':
    {'    QwtPlotMagnifier(QwtPlotCanvas*);':
     '    QwtPlotMagnifier(QwtPlotCanvas* /TransferThis/);',
    },
    
    'QwtPlotMarker':
    {'    QwtPlotMarker(QwtPlot*);':
     '    QwtPlotMarker(QwtPlot* /TransferThis/);',
     },

    'QwtPlotMappedItem':
    {'    QwtPlotMappedItem(QwtPlot*, bool = TRUE);': # Qwt4
     '    QwtPlotMappedItem(QwtPlot* /TransferThis/, bool = TRUE);',
     },

    'QwtPlotPanner':
    {'    QwtPlotPanner(QwtPlotCanvas*);':
     '    QwtPlotPanner(QwtPlotCanvas* /TransferThis/);',
     },

    'QwtPlotPicker':
    {'    QwtPlotPicker(QwtPlotCanvas*, const char* = 0);':
     '    QwtPlotPicker(QwtPlotCanvas* /TransferThis/, const char* = 0);',
     
     '    QwtPlotPicker(int, int, QwtPlotCanvas*, const char* = 0);':
     '    QwtPlotPicker(int, int, QwtPlotCanvas* /TransferThis/, const char* = 0);',
     
     '    QwtPlotPicker(int, int, int, QwtPicker::RubberBand, QwtPicker::DisplayMode, QwtPlotCanvas*, const char* = 0);':
     '    QwtPlotPicker(int, int, int, QwtPicker::RubberBand, QwtPicker::DisplayMode, QwtPlotCanvas* /TransferThis/, const char* = 0);',
     # Qwt5
     '    QwtPlotPicker(QwtPlotCanvas*);':
     '    QwtPlotPicker(QwtPlotCanvas* /TransferThis/);',

     '    QwtPlotPicker(int, int, QwtPlotCanvas*);':
     '    QwtPlotPicker(int, int, QwtPlotCanvas* /TransferThis/);',

     '    QwtPlotPicker(int, int, int, QwtPicker::RubberBand, QwtPicker::DisplayMode, QwtPlotCanvas*);':
     '    QwtPlotPicker(int, int, int, QwtPicker::RubberBand, QwtPicker::DisplayMode, QwtPlotCanvas* /TransferThis/);',

     '    virtual QwtText trackerText(const QwtDoublePoint&) const;':
     '    virtual QwtText trackerText(const QwtDoublePoint&) const /PyName=trackerTextF/;',
     },

    'QwtPlotScaleItem':
    {'    void setScaleDraw(QwtScaleDraw*);':
     '    void setScaleDraw(QwtScaleDraw* /Transfer/);',
     },
    
    'QwtPlotRescaler':
    {'    QwtPlotRescaler(QwtPlotCanvas*, int = xBottom, QwtPlotRescaler::RescalePolicy = Expanding);':
     '    QwtPlotRescaler(QwtPlotCanvas*, int = QwtPlot::xBottom, QwtPlotRescaler::RescalePolicy = Expanding);',
     },
    
    'QwtPlotZoomer':
    {'    QwtPlotZoomer(QwtPlotCanvas*, const char* = 0);':
     '    QwtPlotZoomer(QwtPlotCanvas* /TransferThis/, const char* = 0);',

     '    QwtPlotZoomer(int, int, QwtPlotCanvas*, const char* = 0);':
     '    QwtPlotZoomer(int, int, QwtPlotCanvas* /TransferThis/, const char* = 0);',

     '    QwtPlotZoomer(int, int, int, QwtPicker::DisplayMode, QwtPlotCanvas*, const char* = 0);':
     '    QwtPlotZoomer(int, int, int, QwtPicker::DisplayMode, QwtPlotCanvas* /TransferThis/, const char* = 0);',
     # Qwt5
     '    QwtPlotZoomer(QwtPlotCanvas*, bool = true);':
     '    QwtPlotZoomer(QwtPlotCanvas* /TransferThis/, bool = true);',

     '    QwtPlotZoomer(int, int, QwtPlotCanvas*, bool = true);':
     '    QwtPlotZoomer(int, int, QwtPlotCanvas* /TransferThis/, bool = true);',

     '    QwtPlotZoomer(int, int, int, QwtPicker::DisplayMode, QwtPlotCanvas*, bool = true);':
     '    QwtPlotZoomer(int, int, int, QwtPicker::DisplayMode, QwtPlotCanvas* /TransferThis/, bool = true);',
     },

    'QwtPushButton':
    {'    QwtPushButton(QWidget* = 0, const char* = 0);':
     '    QwtPushButton(QWidget* /TransferThis/ = 0, const char* = 0);',
     
     '    QwtPushButton(const QString&, QWidget* = 0, const char* = 0);':
     '    QwtPushButton(const QString&, QWidget* /TransferThis/ = 0, const char* = 0);',
     
     '    QwtPushButton(const QIconSet&, const QString&, QWidget* = 0, const char* = 0);':
     '    QwtPushButton(const QIconSet&, const QString&, QWidget* /TransferThis/ = 0, const char* = 0);',
    },

    'QwtRasterData':
    {'    virtual QwtRasterData* copy() const = 0;':
     '    virtual QwtRasterData* copy() const = 0 /Factory/;',
     },
    
    'QwtRichText':
    {'    virtual QwtText* clone() const;':
     '    virtual QwtText* clone() const /Factory/;',
     },

    'QwtScale':
    {'    QwtScale(QwtScale::Position, QWidget* = 0);':
     '    QwtScale(QwtScale::Position, QWidget* /TransferThis/ = 0);',

     '    QwtScale(QWidget* = 0, const char* = 0);':
     '    QwtScale(QWidget* /TransferThis/ = 0, const char* = 0);',

     '    QwtScale(QwtScale::Position, QWidget* = 0, const char* = 0);':
     '    QwtScale(QwtScale::Position, QWidget* /TransferThis/ = 0, const char* = 0);',

     '    void minBorderDist(int&, int&) const;':
     '    void minBorderDist(int& /Out/, int& /Out/) const;',

     '    void setScaleDraw(QwtScaleDraw*);':
     '    void setScaleDraw(QwtScaleDraw* /Transfer/);',
     
     '    void labelFormat(char&, int&, int&) const;':
     '    void labelFormat(char& /Out/, int& /Out/, int& /Out/) const;',
     },

    'QwtScaleDiv':
    {'    QwtScaleDiv(const QwtDoubleInterval&, QwtValueList*);':
     r'''    QwtScaleDiv(const QwtDoubleInterval&, QwtValueList, QwtValueList, QwtValueList) [(const QwtDoubleInterval&, QwtValueList*)];
%MethodCode
Py_BEGIN_ALLOW_THREADS
QwtValueList ticks[QwtScaleDiv::NTickTypes] = {*a1, *a2, *a3};
sipCpp = new QwtScaleDiv(*a0, ticks);
Py_END_ALLOW_THREADS
%End
''',
     
     '    QwtScaleDiv(double, double, QwtValueList*);':
     r'''    QwtScaleDiv(double, double, QwtValueList, QwtValueList, QwtValueList) [(const QwtDoubleInterval&, QwtValueList*)];
%MethodCode
Py_BEGIN_ALLOW_THREADS
QwtValueList ticks[QwtScaleDiv::NTickTypes] = {*a2, *a3, *a4};
sipCpp = new QwtScaleDiv(a0, a1, ticks);
Py_END_ALLOW_THREADS
%End
''',
     },

    'QwtScaleDraw':
    {'    void minBorderDist(const QFontMetrics&, int&, int& /Out/) const;': # Qwt4
     '    void minBorderDist(const QFontMetrics&, int& /Out/, int& /Out/) const;',

     '    void labelFormat(char&, int&, int&) const;':
     '    void labelFormat(char& /Out/, int& /Out/, int& /Out/) const;',

     '    virtual void labelPlacement(const QFontMetrics&, double, QPoint&, int&, double&) const;':
     '    virtual void labelPlacement(const QFontMetrics&, double, QPoint&, int& /Out/, double& /Out/) const;',

     '    void getBorderDistHint(const QFont&, int&, int&) const;': # Qwt5
     '    void getBorderDistHint(const QFont&, int& /Out/, int& /Out/) const;',
    },

    'QwtScaleEngine':
    {'    virtual QwtScaleTransformation* transformation() const = 0;':
     '    virtual QwtScaleTransformation* transformation() const = 0 /Factory/;',

     '    virtual void autoScale(int, double&, double&, double&) const = 0;':
     '    virtual void autoScale(int, double& /In, Out/, double& /In, Out/, double&) const = 0;',
     }, 

    'QwtScaleMap':
    {'    void setTransformation(QwtScaleTransformation*);':
     '    void setTransformation(QwtScaleTransformation* /Transfer/);',
     
     '    const QwtScaleTransformation* transformation() const;':
     '    const QwtScaleTransformation* transformation() const /Transfer/;',
     },
    
    'QwtScaleIf': # Qwt4
    {'    void setScaleDraw(QwtScaleDraw*);':
     '    void setScaleDraw(QwtScaleDraw* /Transfer/);',     
     },

    'QwtScaleTransformation':
    {'    virtual QwtScaleTransformation* copy() const;':
     '    virtual QwtScaleTransformation* copy() const /Factory/;',
     },

    'QwtScaleWidget':
    {'    QwtScaleWidget(QwtScaleDraw::Alignment, QWidget* = 0);':
     '    QwtScaleWidget(QwtScaleDraw::Alignment, QWidget* /TransferThis/ = 0);',
     
     '    void getMinBorderDistHint(int&, int&) const;':
     '    void getMinBorderDistHint(int& /Out/, int& /Out/) const;',

     '    void getMinBorderDist(int&, int&) const;':
     '    void getMinBorderDist(int& /Out/, int& /Out/) const;',

     '    void setScaleDiv(QwtScaleTransformation*, const QwtScaleDiv&);':
     '    void setScaleDiv(QwtScaleTransformation* /Transfer/, const QwtScaleDiv&);',
     
     '    void setScaleDraw(QwtScaleDraw*);':
     '    void setScaleDraw(QwtScaleDraw*) /Transfer/;',

     '    const QwtScaleDraw* scaleDraw() const;':
     '    // signature: const QwtScaleDraw* scaleDraw() const /Transfer/;',

     '    QwtScaleDraw* scaleDraw();':
     '    QwtScaleDraw* scaleDraw() /Transfer/;',
     },

    'QwtSlider':
    {'    QwtSlider(QWidget*, const char* = 0, Qt::Orientation = Qt::Horizontal, QwtSlider::ScalePos = None, QwtSlider::BGSTYLE = BgTrough);':
     '    QwtSlider(QWidget* /TransferThis/, const char* = 0, Qt::Orientation = Qt::Horizontal, QwtSlider::ScalePos = None, QwtSlider::BGSTYLE = BgTrough);',
     # Qwt5
     '    QwtSlider(QWidget*, const char*);':
     '    QwtSlider(QWidget* /TransferThis/, const char*);',
     
     '    QwtSlider(QWidget*, Qt::Orientation = Qt::Horizontal, QwtSlider::ScalePos = NoScale, QwtSlider::BGSTYLE = BgTrough);':
     '    QwtSlider(QWidget* /TransferThis/, Qt::Orientation = Qt::Horizontal, QwtSlider::ScalePos = NoScale, QwtSlider::BGSTYLE = BgTrough);',
          
     '    void setScaleDraw(QwtScaleDraw*);':
     '    void setScaleDraw(QwtScaleDraw* /Transfer/);',

     '    virtual void getScrollMode(const QPoint&, int&, int&);':
     '    virtual void getScrollMode(const QPoint&, int& /Out/, int& /Out/);',
     },

    'QwtSliderBase':
    {'    QwtSliderBase(Qt::Orientation, QWidget* = 0, const char* = 0, uint = 0);':
     '    QwtSliderBase(Qt::Orientation, QWidget* /TransferThis/ = 0, const char* = 0, uint = 0);',

     '    virtual void getScrollMode(const QPoint&, int&, int&) = 0;':
     '    virtual void getScrollMode(const QPoint&, int& /Out/, int& /Out/) = 0;',
     },

    'QwtSpline':
    {'    int recalc(double*, double*, int, int = 0);':
     r'''    int recalc(SIP_PYOBJECT, SIP_PYOBJECT, int = 0);
%MethodCode
QwtArray<double> xArray;
if (1 != try_PyObject_to_QwtArray(a0, xArray))
    return 0;

QwtArray<double> yArray;       
if (1 != try_PyObject_to_QwtArray(a1, yArray))
    return 0;

    int n = xArray.size() < yArray.size() ? xArray.size() : yArray.size();
        
    sipRes = sipCpp->QwtSpline::recalc(xArray.data(), yArray.data(), n, a2);
%End // recalc()
''',

     '    void copyValues(int = 1);':
     '    // Not Pythonic: void copyValues(int = 1);',

     # Qwt5
     '    QMemArray<QwtDoublePoint> points() const;':
     r'''
%If (Qwt_5_0_1 - )
    QMemArray<QwtDoublePoint> points() const;
%End // (Qwt_5_0_1 - )
''',
     
     '    QPolygonF points() const;':
     r'''
%If (Qwt_5_0_1 - )
    QPolygonF points() const;
%End // (Qwt_5_0_1 - )
''',
     },

    'QwtSymbol':
    {'    virtual QwtSymbol* clone() const;':
     '    virtual QwtSymbol* clone() const /Factory/;',
     },

    'QwtText':
    {'    virtual QwtText* clone() const = 0;':
     '    virtual QwtText* clone() const = 0 /Factory/;',
     },

    'QwtTextLabel':
    {'    QwtTextLabel(QWidget* = 0);':
     '    QwtTextLabel(QWidget* /TransferThis/ = 0);',

     '    QwtTextLabel(const QwtText&, QWidget* = 0);':
     '    QwtTextLabel(const QwtText&, QWidget* /TransferThis/ = 0);',
    },

    'QwtText':
    {'    QwtText(const QString& = QString::null, QwtText::TextFormat = QwtText::AutoText);':
     '''    QwtText();
    QwtText(const QString&);
    QwtText(const QString&, QwtText::TextFormat);''',
    },
    
    'QwtThermo':
    {'    QwtThermo(QWidget* = 0, const char* = 0);':
     '    QwtThermo(QWidget* /TransferThis/ = 0, const char* = 0);',

     '    QwtThermo(QWidget* = 0);':
     '    QwtThermo(QWidget* /TransferThis/ = 0);',

     '    void setScaleDraw(QwtScaleDraw*);':
     '    void setScaleDraw(QwtScaleDraw* /Transfer/);',
     },

    'QwtWheel':
    {'    QwtWheel(QWidget* = 0, const char* = 0);':
     '    QwtWheel(QWidget* /TransferThis/ = 0, const char* = 0);',

     '    QwtWheel(QWidget* = 0);':
     '    QwtWheel(QWidget* /TransferThis/ = 0);',
     
     '    virtual void getScrollMode(const QPoint&, int&, int&);':
     '    virtual void getScrollMode(const QPoint&, int& /Out/, int& /Out/);',
     },
    }
# MEMBERS


EXTRA = {
    'QwtAbstractSlider':
    r'''
// python mksccode PyQt4.Qwt5
%ConvertToSubClassCode
    static struct class_graph {
        const char *name;
        sipWrapperType **type;
        int yes, no;
    } graph[] = {
        {sipName_QwtAbstractSlider, &sipClass_QwtAbstractSlider, 13, 1},
#if QWT_VERSION >= 0x050100
        {sipName_QwtPanner, &sipClass_QwtPanner, 19, 2},
#else
        {0, 0, 19, 2},
#endif
        {sipName_QwtDynGridLayout, &sipClass_QwtDynGridLayout, -1, 3},
        {sipName_QwtCounter, &sipClass_QwtCounter, -1, 4},
        {sipName_QwtLegend, &sipClass_QwtLegend, -1, 5},
        {sipName_QwtArrowButton, &sipClass_QwtArrowButton, -1, 6},
        {sipName_QwtScaleWidget, &sipClass_QwtScaleWidget, -1, 7},
        {sipName_QwtTextLabel, &sipClass_QwtTextLabel, 20, 8},
        {sipName_QwtPlotCanvas, &sipClass_QwtPlotCanvas, -1, 9},
        {sipName_QwtThermo, &sipClass_QwtThermo, -1, 10},
#if QWT_VERSION >= 0x050100
        {sipName_QwtMagnifier, &sipClass_QwtMagnifier, 21, 11},
#else
        {0, 0, 21, 11},
#endif
        {sipName_QwtPlot, &sipClass_QwtPlot, -1, 12},
        {sipName_QwtPicker, &sipClass_QwtPicker, 22, -1},
        {sipName_QwtDial, &sipClass_QwtDial, 17, 14},
        {sipName_QwtSlider, &sipClass_QwtSlider, -1, 15},
        {sipName_QwtWheel, &sipClass_QwtWheel, -1, 16},
        {sipName_QwtKnob, &sipClass_QwtKnob, -1, -1},
        {sipName_QwtAnalogClock, &sipClass_QwtAnalogClock, -1, 18},
        {sipName_QwtCompass, &sipClass_QwtCompass, -1, -1},
        {sipName_QwtPlotPanner, &sipClass_QwtPlotPanner, -1, -1},
        {sipName_QwtLegendItem, &sipClass_QwtLegendItem, -1, -1},
        {sipName_QwtPlotMagnifier, &sipClass_QwtPlotMagnifier, -1, -1},
        {sipName_QwtPlotPicker, &sipClass_QwtPlotPicker, 23, -1},
        {sipName_QwtPlotZoomer, &sipClass_QwtPlotZoomer, -1, -1},
    };
    int i = 0;
    sipClass = NULL;
    do {
        struct class_graph *cg = &graph[i];
        if (cg->name != NULL && sipCpp->inherits(cg->name)) {
            sipClass = *cg->type;
            i = cg->yes;
        } else {
            i = cg->no;
        }
    } while (i >= 0);
%End
''',
    
    # Private copy constructor prevents SIP to generate an assignment operator
    # ConvertToSubClass code for QwtData
    'QwtData':
    r'''
private:
    QwtData(const QwtData&);
%If (CXX_DYNAMIC_CAST)
%ConvertToSubClassCode
    // Walk the inheritance tree depth first in alphabetical order
    // This code is for Qwt4 and Qwt5
#ifdef sipClass_QwtArrayData
    if (dynamic_cast<const QwtArrayData *>(sipCpp))
        sipClass = sipClass_QwtArrayData;
    else
#endif
#ifdef sipClass_QwtDoublePointData
    if (dynamic_cast<const QwtDoublePointData *>(sipCpp))
        sipClass = sipClass_QwtDoublePointData;
    else
#endif
#ifdef sipClass_QwtPolygonFData
    if (dynamic_cast<const QwtPolygonFData *>(sipCpp))
        sipClass = sipClass_QwtPolygonFData;
    else
#endif
#ifdef sipClass_QwtData
    if (dynamic_cast<const QwtData *>(sipCpp))
        sipClass = sipClass_QwtData;
    else
#endif
        sipClass = 0;
%End
%End
''',

    # Extra constructor for QwtIntervalData
    'QwtIntervalData':
    r'''
    QwtIntervalData(const QwtArrayQwtDoubleInterval&, const QwtArrayDouble&);
    void setData(const QwtArrayQwtDoubleInterval&, const QwtArrayDouble&);
''',
    
    # ConvertToSubClass code for QwtPickerMachine
    'QwtPickerMachine':
    r'''
%If (CXX_DYNAMIC_CAST)
%ConvertToSubClassCode
    // Walk the inheritance tree depth first in alphabetical order
#ifdef sipClass_QwtPickerClickPointMachine
    if (dynamic_cast<const QwtPickerClickPointMachine *>(sipCpp))
        sipClass = sipClass_QwtPickerClickPointMachine;
    else
#endif
#ifdef sipClass_QwtPickerClickRectMachine 
    if (dynamic_cast<const QwtPickerClickRectMachine *>(sipCpp))
        sipClass = sipClass_QwtPickerClickRectMachine;
    else
#endif
#ifdef sipClass_QwtPickerDragPointMachine
    if (dynamic_cast<const QwtPickerDragPointMachine *>(sipCpp))
        sipClass = sipClass_QwtPickerDragPointMachine;
    else
#endif
#ifdef sipClass_QwtPickerDragRectMachine 
    if (dynamic_cast<const QwtPickerDragRectMachine *>(sipCpp))
        sipClass = sipClass_QwtPickerDragRectMachine;
    else
#endif
#ifdef sipClass_QwtPickerPolygonMachine
    if (dynamic_cast<const QwtPickerPolygonMachine *>(sipCpp))
        sipClass = sipClass_QwtPickerPolygonMachine;
    else
#endif
#ifdef sipClass_QwtPickerMachine
    if (dynamic_cast<const QwtPickerMachine *>(sipCpp))
        sipClass = sipClass_QwtPickerMachine;
    else
#endif
        sipClass = 0;
%End
%End
''',

    # ConvertToSubClass code for QwtPlotItem
    'QwtPlotItem':
    r'''
%If (HAS_QWT5)
%ConvertToSubClassCode
    Py_BEGIN_ALLOW_THREADS
    switch (sipCpp->rtti()) {
    case QwtPlotItem::Rtti_PlotItem: sipClass = sipClass_QwtPlotItem; break;
    case QwtPlotItem::Rtti_PlotGrid: sipClass = sipClass_QwtPlotGrid; break; 
#ifdef sipClass_QwtPlotScaleItem
    case QwtPlotItem::Rtti_PlotScale: sipClass = sipClass_QwtPlotScaleItem; break; 
#endif // sipClass_QwtPlotScaleItem
    case QwtPlotItem::Rtti_PlotMarker: sipClass = sipClass_QwtPlotMarker; break; 
    case QwtPlotItem::Rtti_PlotCurve: sipClass = sipClass_QwtPlotCurve; break;
#ifdef sipClass_QwtPlotHistogram
    case QwtPlotItem::Rtti_PlotHistogram: sipClass = sipClass_QwtPlotHistogram; break;
#endif // sipClass_QwtPlotHistogram
    case QwtPlotItem::Rtti_PlotSpectrogram: sipClass = sipClass_QwtPlotSpectrogram; break;
#ifdef sipClass_QwtPlotSvgItem
    case QwtPlotItem::Rtti_PlotSVG: sipClass = sipClass_QwtPlotSvgItem; break; 
#endif // sipClass_QwtPlotSvgItem
    default: sipClass = 0;
    }
    Py_END_ALLOW_THREADS
%End // %ConvertToSubClassCode
%End // HAS_QWT5
''',

    'QwtScaleMap':
    r'''
public:
    QwtScaleMap(int, int, double, double);
%MethodCode
sipCpp = new QwtScaleMap();
sipCpp->setPaintInterval(a0, a1);
sipCpp->setScaleInterval(a2, a3);
%End
''',

    # Private copy constructor prevents SIP to generate an assignment operator
    'QwtScaleTransformation':
    r'''
private:
    QwtScaleTransformation(const QwtScaleTransformation&);
''',

    'QwtSliderBase':
    r'''
// python mksccode Qwt4
%ConvertToSubClassCode
    static struct class_graph {
        const char *name;
        sipWrapperType **type;
        int yes, no;
    } graph[] = {
        {sipName_QwtLegend, &sipClass_QwtLegend, -1, 1},
        {sipName_QwtArrowButton, &sipClass_QwtArrowButton, -1, 2},
        {sipName_QwtScale, &sipClass_QwtScale, -1, 3},
        {sipName_QwtPlot, &sipClass_QwtPlot, -1, 4},
        {sipName_QwtCounter, &sipClass_QwtCounter, -1, 5},
        {sipName_QwtDynGridLayout, &sipClass_QwtDynGridLayout, -1, 6},
        {sipName_QwtPlotCanvas, &sipClass_QwtPlotCanvas, -1, 7},
        {sipName_QwtThermo, &sipClass_QwtThermo, -1, 8},
        {sipName_QwtLegendLabel, &sipClass_QwtLegendLabel, -1, 9},
        {sipName_QwtSliderBase, &sipClass_QwtSliderBase, 12, 10},
        {sipName_QwtPicker, &sipClass_QwtPicker, 18, 11},
        {sipName_QwtPushButton, &sipClass_QwtPushButton, 20, -1},
        {sipName_QwtWheel, &sipClass_QwtWheel, -1, 13},
        {sipName_QwtKnob, &sipClass_QwtKnob, -1, 14},
        {sipName_QwtSlider, &sipClass_QwtSlider, -1, 15},
        {sipName_QwtDial, &sipClass_QwtDial, 16, -1},
        {sipName_QwtAnalogClock, &sipClass_QwtAnalogClock, -1, 17},
        {sipName_QwtCompass, &sipClass_QwtCompass, -1, -1},
        {sipName_QwtPlotPicker, &sipClass_QwtPlotPicker, 19, -1},
        {sipName_QwtPlotZoomer, &sipClass_QwtPlotZoomer, -1, -1},
        {sipName_QwtLegendButton, &sipClass_QwtLegendButton, -1, -1},
    };
    int i = 0;
    sipClass = NULL;
    do {
        struct class_graph *cg = &graph[i];
        if (cg->name != NULL && sipCpp->inherits(cg->name)) {
            sipClass = *cg->type;
            i = cg->yes;
        } else {
            i = cg->no;
        }
    } while (i >= 0);
%End
''',
    }
# EXTRA


# Local Variables: ***
# mode: python ***
# End: ***
