/* frozendict: read-only and hashable dict */

#include "Python.h"

#if PY_MAJOR_VERSION < 3
typedef Py_ssize_t Py_hash_t;
typedef size_t Py_uhash_t;
#define _PyHASH_MULTIPLIER 1000003UL  /* 0xf4243 */
#endif

typedef struct {
    PyObject_HEAD
    PyObject *dict;
    Py_hash_t hash;
} PyFrozenDictObject;

static PyTypeObject PyFrozenDict_Type;

static Py_ssize_t
frozendict_len(PyFrozenDictObject *pp)
{
    return PyObject_Size(pp->dict);
}

static PyObject *
frozendict_getitem(PyFrozenDictObject *pp, PyObject *key)
{
    return PyObject_GetItem(pp->dict, key);
}

static PyMappingMethods frozendict_as_mapping = {
    (lenfunc)frozendict_len,                  /* mp_length */
    (binaryfunc)frozendict_getitem,           /* mp_subscript */
    0,                                        /* mp_ass_subscript */
};

static int
frozendict_contains(PyFrozenDictObject *pp, PyObject *key)
{
    return PyDict_Contains(pp->dict, key);
}

static PySequenceMethods frozendict_as_sequence = {
    0,                                          /* sq_length */
    0,                                          /* sq_concat */
    0,                                          /* sq_repeat */
    0,                                          /* sq_item */
    0,                                          /* sq_slice */
    0,                                          /* sq_ass_item */
    0,                                          /* sq_ass_slice */
    (objobjproc)frozendict_contains,            /* sq_contains */
    0,                                          /* sq_inplace_concat */
    0,                                          /* sq_inplace_repeat */
};

static PyObject *
frozendict_get(PyFrozenDictObject *pp, PyObject *args)
{
    PyObject *key, *def = Py_None;
#if PY_MAJOR_VERSION >= 3
    _Py_IDENTIFIER(get);
#endif

    if (!PyArg_UnpackTuple(args, "get", 1, 2, &key, &def))
        return NULL;

#if PY_MAJOR_VERSION >= 3
    return _PyObject_CallMethodId(pp->dict, &PyId_get, "(OO)", key, def);
#else
    return PyObject_CallMethod(pp->dict, "get", "(OO)", key, def);
#endif
}

static PyObject *
frozendict_keys(PyFrozenDictObject *pp)
{
#if PY_MAJOR_VERSION >= 3
    _Py_IDENTIFIER(keys);
    return _PyObject_CallMethodId(pp->dict, &PyId_keys, NULL);
#else
    return PyObject_CallMethod(pp->dict, "keys", NULL);
#endif
}

static PyObject *
frozendict_values(PyFrozenDictObject *pp)
{
#if PY_MAJOR_VERSION >= 3
    _Py_IDENTIFIER(values);
    return _PyObject_CallMethodId(pp->dict, &PyId_values, NULL);
#else
    return PyObject_CallMethod(pp->dict, "values", NULL);
#endif
}

static PyObject *
frozendict_items(PyFrozenDictObject *pp)
{
#if PY_MAJOR_VERSION >= 3
    _Py_IDENTIFIER(items);
    return _PyObject_CallMethodId(pp->dict, &PyId_items, NULL);
#else
    return PyObject_CallMethod(pp->dict, "items", NULL);
#endif
}

static PyObject *
frozendict_copy(PyFrozenDictObject *pp)
{
#if PY_MAJOR_VERSION >= 3
    _Py_IDENTIFIER(copy);
    return _PyObject_CallMethodId(pp->dict, &PyId_copy, NULL);
#else
    return PyObject_CallMethod(pp->dict, "copy", NULL);
#endif
}

/* WARNING: frozendict methods must not give access
            to the underlying mapping */

static PyObject *
frozendict_getnewargs(PyFrozenDictObject *ob)
{
    PyObject *args;

    args = PyTuple_Pack(1, ob->dict);

    return args;
}

static PyObject *
frozendict_reduce(PyFrozenDictObject *ob)
{
    PyObject *res, *tmp;

    tmp = PyTuple_Pack(1, ob->dict);
    res = PyTuple_Pack(2, &PyFrozenDict_Type, tmp);
    Py_DECREF(tmp);

    return res;
}


static PyMethodDef frozendict_methods[] = {
   {"__getnewargs__",(PyCFunction)frozendict_getnewargs,  METH_NOARGS, PyDoc_STR("d.__getnewargs__()")},
    {"__copy__",     (PyCFunction)frozendict_copy, METH_NOARGS, PyDoc_STR("d.__copy__()")},
//     {"__len__",      (PyCFunction)frozendict_len, METH_NOARGS, memoryslots_len_doc},
//     {"__sizeof__",   (PyCFunction)frozendict_sizeof, METH_NOARGS, memoryslots_sizeof_doc},     
    {"__reduce__",   (PyCFunction)frozendict_reduce, METH_NOARGS, PyDoc_STR("d.__reduce__()")},
    {"get",       (PyCFunction)frozendict_get,        METH_VARARGS,
     PyDoc_STR("D.get(k[,d]) -> D[k] if k in D, else d."
               "  d defaults to None.")},
    {"keys",      (PyCFunction)frozendict_keys,       METH_NOARGS,
     PyDoc_STR("D.keys() -> list of D's keys")},
    {"values",    (PyCFunction)frozendict_values,     METH_NOARGS,
     PyDoc_STR("D.values() -> list of D's values")},
    {"items",     (PyCFunction)frozendict_items,      METH_NOARGS,
     PyDoc_STR("D.items() -> list of D's (key, value) pairs, as 2-tuples")},
    {"copy",      (PyCFunction)frozendict_copy,       METH_NOARGS,
     PyDoc_STR("D.copy() -> a shallow copy of D")},
    {0}
};

static void
frozendict_dealloc(PyFrozenDictObject *pp)
{
    PyObject_GC_UnTrack(pp);
    Py_DECREF(pp->dict);
    PyObject_GC_Del(pp);
}

static PyObject *
frozendict_getiter(PyFrozenDictObject *pp)
{
    return PyObject_GetIter(pp->dict);
}

// static PyObject *
// frozendict_str(PyFrozenDictObject *pp)
// {
//     return PyObject_Str(pp->dict);
// }

static PyObject *
frozendict_repr(PyFrozenDictObject *pp)
{
#if PY_MAJOR_VERSION >= 3
    return PyUnicode_FromFormat("frozendict(%R)", pp->dict);
#else
    PyObject *reprobj = PyObject_Repr(pp->dict);
    return PyString_FromFormat("frozendict(%s)", PyString_AS_STRING(reprobj));
#endif
}

static int
frozendict_traverse(PyObject *self, visitproc visit, void *arg)
{
    PyFrozenDictObject *pp = (PyFrozenDictObject *)self;
    Py_VISIT(pp->dict);
    return 0;
}

static PyObject *
frozendict_richcompare(PyFrozenDictObject *v, PyObject *w, int op)
{
    return PyObject_RichCompare(v->dict, w, op);
}

// static int
// frozendict_check_mapping(PyObject *mapping)
// {
//     if (!PyMapping_Check(mapping)
//         || PyList_Check(mapping)
//         || PyTuple_Check(mapping)) {
//         PyErr_Format(PyExc_TypeError,
//                     "frozendict() argument must be a mapping, not %s",
//                     Py_TYPE(mapping)->tp_name);
//         return -1;
//     }
//     return 0;
// }

static PyObject*
frozendict_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    PyObject *new_dict;
    PyFrozenDictObject *frozendict;

    frozendict = (PyFrozenDictObject*)PyObject_GC_New(PyFrozenDictObject, &PyFrozenDict_Type);
    if (frozendict == NULL)
        return NULL;
    
    new_dict = PyObject_Call(((PyObject *)(&PyDict_Type)), args, kwargs); 
    if (new_dict == NULL) {
        return NULL;
    }
     
    Py_INCREF(new_dict);
    frozendict->dict = new_dict;
    frozendict->hash = 0;
        
    PyObject_GC_Track(frozendict);
    
    return (PyObject *)frozendict;
}

static Py_hash_t frozendict_hash(PyFrozenDictObject *fd) {
    PyObject *key, *value;
    Py_ssize_t pos=0, len;    
    Py_hash_t hash_key, hash_value;
    Py_uhash_t mult = _PyHASH_MULTIPLIER;
    Py_uhash_t hash, hash_keyval, keyval_mult;
    
    if (fd->hash == 0) {
        
        len = PyDict_Size(fd->dict);
        hash = 0x345678UL;
        while (PyDict_Next(fd->dict, &pos, &key, &value)) {
            hash_keyval = 0x345678UL;
            keyval_mult = _PyHASH_MULTIPLIER;
            
            hash_key = PyObject_Hash(key);
            if (hash_key == -1)
                return -1;
            
            hash_keyval = (hash_keyval ^ hash_key) * keyval_mult;
            keyval_mult += 82524UL;
            
            hash_value = PyObject_Hash(value);
            if (hash_value == -1)
                return -1;
            hash_keyval = (hash_keyval ^ hash_value) * keyval_mult;
            hash_keyval += 97531UL;
            
            if (hash_keyval == (Py_uhash_t)-1)
                hash_keyval = -2;
            
            hash = (hash ^ hash_keyval) * mult;
            mult += (Py_hash_t)(82520UL + len + len);
        }
        
        hash += 97531UL;
        if (hash == (Py_uhash_t)-1)
            hash = -2;
        fd->hash = (Py_hash_t)hash;
    }
        
    return fd->hash;
}

#define DEFERRED_ADDRESS(addr) 0

static PyTypeObject PyFrozenDict_Type = {
    PyVarObject_HEAD_INIT(DEFERRED_ADDRESS(&PyType_Type), 0)
    "frozenmap._frozendict.frozendict",       /* tp_name */
    sizeof(PyFrozenDictObject),               /* tp_basicsize */
    0,                                        /* tp_itemsize */
    /* methods */
    (destructor)frozendict_dealloc,           /* tp_dealloc */
    0,                                        /* tp_print */
    0,                                        /* tp_getattr */
    0,                                        /* tp_setattr */
    0,                                        /* tp_reserved */
    (reprfunc)frozendict_repr,                /* tp_repr */
    0,                                        /* tp_as_number */
    &frozendict_as_sequence,                  /* tp_as_sequence */
    &frozendict_as_mapping,                   /* tp_as_mapping */
    (hashfunc)frozendict_hash,                /* tp_hash */
    0,                                        /* tp_call */
    (reprfunc)frozendict_repr,                 /* tp_str */
    PyObject_GenericGetAttr,                  /* tp_getattro */
    0,                                        /* tp_setattro */
    0,                                        /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC | Py_TPFLAGS_BASETYPE, 
                                              /* tp_flags */
    0,                                        /* tp_doc */
    frozendict_traverse,                      /* tp_traverse */
    0,                                        /* tp_clear */
    (richcmpfunc)frozendict_richcompare,      /* tp_richcompare */
    0,                                        /* tp_weaklistoffset */
    (getiterfunc)frozendict_getiter,          /* tp_iter */
    0,                                        /* tp_iternext */
    frozendict_methods,                       /* tp_methods */
    0,                                        /* tp_members */
    0,                                        /* tp_getset */
    0,                                        /* tp_base */
    0,                                        /* tp_dict */
    0,                                        /* tp_descr_get */
    0,                                        /* tp_descr_set */
    0,                                        /* tp_dictoffset */
    0,                                        /* tp_init */
    0,                                        /* tp_alloc */
    frozendict_new,                           /* tp_new */
};

/* List of functions defined in the module */

PyDoc_STRVAR(frozendictmodule_doc,
"Module provide mutable frozendict type.");

#if PY_MAJOR_VERSION >= 3
static PyMethodDef frozendictmodule_methods[] = {
  {0, 0, 0, 0}
};

static struct PyModuleDef frozendictmodule = {
  #if PY_VERSION_HEX < 0x03020000
    { PyObject_HEAD_INIT(NULL) NULL, 0, NULL },
  #else
    PyModuleDef_HEAD_INIT,
  #endif
    "frozenmap._frozendict",
    frozendictmodule_doc,
    -1,
    frozendictmodule_methods,
    NULL,
    NULL,
    NULL,
    NULL
};
#endif

#if PY_MAJOR_VERSION >= 3
PyMODINIT_FUNC
PyInit__frozendict(void)
{
    PyObject *m;
    
    m = PyState_FindModule(&frozendictmodule);
    if (m) {
        Py_INCREF(m);
        return m;
    }    

    m = PyModule_Create(&frozendictmodule);
    if (m == NULL)
        return NULL;

    if (PyType_Ready(&PyFrozenDict_Type) < 0)
        Py_FatalError("Can't initialize frozendict type");
    
    Py_INCREF(&PyFrozenDict_Type);
    PyModule_AddObject(m, "frozendict", (PyObject *)&PyFrozenDict_Type);

    
//     if (PyType_Ready(&PyfrozendictIter_Type) < 0)
//         Py_FatalError("Can't initialize frozendict iter type");

//     Py_INCREF(&PyfrozendictIter_Type);    
//     PyModule_AddObject(m, "frozendictiter", (PyObject *)&PyfrozendictIter_Type);
    

    return m;
}
#else
PyMODINIT_FUNC
init_frozendict(void)
{
    PyObject *m;
    
    m = Py_InitModule3("frozenmap._frozendict", NULL, frozendictmodule_doc);
    if (m == NULL)
        return;
    Py_XINCREF(m);

    if (PyType_Ready(&PyFrozenDict_Type) < 0)
         Py_FatalError("Can't initialize frozendict type");

    Py_INCREF(&PyFrozenDict_Type);
    PyModule_AddObject(m, "frozendict", (PyObject *)&PyFrozenDict_Type);

//     if (PyType_Ready(&PyfrozendictIter_Type) < 0)
//         Py_FatalError("Can't initialize frozendict iter type");

//     Py_INCREF(&PyfrozendictIter_Type);
//     PyModule_AddObject(m, "frozendictiter", (PyObject *)&PyfrozendictIter_Type);

    return;
}
#endif
