#include <Python.h>
#include <structmember.h>
#include "twoth.h"
#include "splitbbox.h"


typedef struct {
    PyObject_HEAD
    Py_ssize_t nbins;
    struct positions *pos;
} cgracio_pos;


static int cgracio_pos_init(cgracio_pos *self, PyObject *args)
{
    destroy_positions(self->pos);
    return 0;
}


static void cgracio_pos_dealloc(cgracio_pos *self)
{
    destroy_positions(self->pos);
    Py_TYPE(self)->tp_free((PyObject *)self);
}


static int cgracio_pos_getbuffer(PyObject *obj, Py_buffer *view, int flags)
{
    cgracio_pos *self = (cgracio_pos *)obj;

    if (view == NULL || self->pos == NULL || self->pos->pos == NULL) {
        PyErr_SetString(PyExc_ValueError, "NULL view in getbuffer or bins are not calculated");
        return -1;
    }
    self->nbins = (Py_ssize_t)self->pos->nbins;
    view->obj = obj;
    view->buf = (void *)self->pos->pos;
    view->len = self->pos->s_pos_buf;
    view->readonly = 1;
    view->itemsize = (Py_ssize_t)sizeof(float_ti);
    view->format = EXPORT_TYPE;
    view->ndim = 1;
    view->shape = &self->nbins;
    view->strides = &view->itemsize;
    view->suboffsets = NULL;
    view->internal = NULL;
    Py_INCREF(self);  /* need to increase the reference count */
    return 0;
}

static PyBufferProcs cgracio_pos_as_buffer = {
  (getbufferproc)cgracio_pos_getbuffer,
  (releasebufferproc)0,
};


static PyTypeObject cgracio_pos_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    TP_NAME_POS,                                /* tp_name */
    sizeof(cgracio_pos),                        /* tp_basicsize */
    0,                                          /* tp_itemsize */
    (destructor)cgracio_pos_dealloc,            /* tp_dealloc */
    0,                                          /* tp_print */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    0,                                          /* tp_reserved */
    0,                                          /* tp_repr */
    0,                                          /* tp_as_number */
    0,                                          /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    0,                                          /* tp_hash  */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    0,                                          /* tp_getattro */
    0,                                          /* tp_setattro */
    &cgracio_pos_as_buffer,                     /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,                         /* tp_flags */
    "_positions object",                        /* tp_doc */
    0,                                          /* tp_traverse */
    0,                                          /* tp_clear */
    0,                                          /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    0,                                          /* tp_iter */
    0,                                          /* tp_iternext */
    0,                                          /* tp_methods */
    0,                                          /* tp_members */
    0,                                          /* tp_getset */
    0,                                          /* tp_base */
    0,                                          /* tp_dict */
    0,                                          /* tp_descr_get */
    0,                                          /* tp_descr_set */
    0,                                          /* tp_dictoffset */
    (initproc)cgracio_pos_init,                 /* tp_init */
    0,                                          /* tp_alloc */
    PyType_GenericNew,                          /* tp_new */
};


typedef struct {
    PyObject_HEAD
    struct integration in;
    PyObject *apos;
    PyObject *rpos;
} cgracio_integration;


static PyObject *cgacio_integration_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    cgracio_integration *self;

    self = (cgracio_integration *)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->apos = PyObject_CallObject((PyObject *)&cgracio_pos_type, NULL);
        if (self->apos == NULL) {
            Py_DECREF(self);
            return NULL;
        }
        self->rpos = PyObject_CallObject((PyObject *)&cgracio_pos_type, NULL);
        if (self->rpos == NULL) {
            Py_DECREF(self);
            return NULL;
        }
    }
    return (PyObject *)self;
}

static int cgracio_integration_init(cgracio_integration *self, PyObject *args)
{
    int dim1, dim2, retval;
    struct integration *in;
    struct geometry *g;
    Py_buffer geo;
    cgracio_pos *apos, *rpos;

    if (!PyArg_ParseTuple(args, "iiy*", &dim1, &dim2, &geo))
        return -1;

    if (geo.len != sizeof(struct geometry)) {
        PyErr_SetString(PyExc_TypeError, "The PONI geometry structure cannot be interpreted");
        return -1;
    }

    if (dim1 <= 0 || dim2 <= 0) {
        PyErr_SetString(PyExc_ValueError, "The dimensions cannot be less than zero");
        return -1;
    }
    destroy_integration(&self->in);

    self->in.mem = NULL;
    self->in.dim1 = dim1;
    self->in.dim2 = dim2;
    in = &self->in;
    g = (struct geometry *)geo.buf;
    Py_BEGIN_ALLOW_THREADS
    retval = calculate_positions(in, g);
    Py_END_ALLOW_THREADS
    if (!retval) {
        PyErr_SetString(PyExc_MemoryError, "It seems that the memory cannot be allocated. Buy more RAM.");
        return -1;
    }

    apos = (cgracio_pos *)self->apos;
    rpos = (cgracio_pos *)self->rpos;
    apos->pos = in->azimuth;
    rpos->pos = in->radial;
    return 0;
}


static PyMemberDef cgracio_integration_members[] = {
    {"apos", T_OBJECT_EX, offsetof(cgracio_integration, apos), READONLY, "Azimuthal bin position array"},
    {"rpos", T_OBJECT_EX, offsetof(cgracio_integration, rpos), READONLY, "Radial bin position array"},
    {NULL}  /* Sentinel */
};


static void cgracio_integration_dealloc(cgracio_integration *self)
{
    Py_XDECREF(self->apos);
    Py_XDECREF(self->rpos);
    destroy_integration(&self->in);
    Py_TYPE(self)->tp_free((PyObject *)self);
}


static PyTypeObject cgracio_integration_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    TP_NAME_CGRACIO,                            /* tp_name */
    sizeof(cgracio_integration),                /* tp_basicsize */
    0,                                          /* tp_itemsize */
    (destructor)cgracio_integration_dealloc,    /* tp_dealloc */
    0,                                          /* tp_print */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    0,                                          /* tp_reserved */
    0,                                          /* tp_repr */
    0,                                          /* tp_as_number */
    0,                                          /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    0,                                          /* tp_hash  */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    0,                                          /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,                         /* tp_flags */
    "_integration object",                      /* tp_doc */
    0,                                          /* tp_traverse */
    0,                                          /* tp_clear */
    0,                                          /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    0,                                          /* tp_iter */
    0,                                          /* tp_iternext */
    0,                                          /* tp_methods */
    cgracio_integration_members,                /* tp_members */
    0,                                          /* tp_getset */
    0,                                          /* tp_base */
    0,                                          /* tp_dict */
    0,                                          /* tp_descr_get */
    0,                                          /* tp_descr_set */
    0,                                          /* tp_dictoffset */
    (initproc)cgracio_integration_init,         /* tp_init */
    0,                                          /* tp_alloc */
    cgacio_integration_new,                     /* tp_new */
};


typedef struct {
    PyObject_HEAD
    struct results res;
    Py_ssize_t shape[2];
    Py_ssize_t strides[2];
} cgracio_results;


static int cgracio_results_init(cgracio_results *self, PyObject *args)
{
    float_ti *fimage;
    PyObject *np_image;
    Py_buffer image;
    cgracio_integration *py_integration;
    struct integration *in;
    struct results *res;
    enum integration_type it;
    int retval;
    int (*func)(struct integration*, float_ti*, struct results*);

    res = &self->res;
    destroy_results(res);
    if (!PyArg_ParseTuple(args, IMPORT_TYPE, &py_integration, &np_image, &it, &res->lm.azmin, &res->lm.azmax))
        return -1;

    PyObject_GetBuffer(np_image, &image, PyBUF_C_CONTIGUOUS);
    if (image.len != py_integration->in.s_array_buf) {
        PyBuffer_Release(&image);
        PyErr_SetString(PyExc_ValueError, "The image has wrong dimensions");
        return -1;
    }

    switch (it) {
        case radial:    func = integrate_image_radial; break;
        case azimuthal: func = integrate_image_azimuth; break;
        case twodim:    func = integrate_image_2d; break;
        default:        PyErr_SetString(PyExc_NotImplementedError, "Integration type is unknown");
                        PyBuffer_Release(&image);
                        return -1;
    }

    in = &py_integration->in;
    fimage = (float_ti *)image.buf;
    res->lm.rdmin = in->radmin;       /* TODO: get it through the parameters */
    res->lm.rdmax = in->radmax;
    Py_BEGIN_ALLOW_THREADS
    retval = func(in, fimage, res);
    Py_END_ALLOW_THREADS
    PyBuffer_Release(&image);
    if (!retval) {
        PyErr_SetString(PyExc_MemoryError, "Memory for integration cannot be allocated. Buy more RAM.");
        return -1;
    }
    return 0;
}


static int cgracio_results_getbuffer(PyObject *obj, Py_buffer *view, int flags)
{
    cgracio_results *self = (cgracio_results *)obj;

    if (view == NULL) {
        PyErr_SetString(PyExc_ValueError, "NULL view in getbuffer");
        return -1;
    }
    view->obj = obj;
    view->buf = (void *)self->res.merge;
    view->readonly = 1;
    view->format = EXPORT_TYPE;
    view->ndim = 2;
    if (self->res.type == twodim) {
        self->shape[0] = (Py_ssize_t)self->res.rbins;
        self->shape[1] = (Py_ssize_t)self->res.abins;
        self->strides[0] = (Py_ssize_t)(self->res.abins * sizeof(float_ti));
        view->len = ((Py_ssize_t)self->res.rbins) * self->strides[0];
    } else {
        /* fill up the buffer structures to be interpreted as a 2D numpy array */
        /* the first column is intensity, the second one is the standard deviations */
        self->shape[0]   = 2;
        self->shape[1]   = (Py_ssize_t)self->res.bins;
        self->strides[0] = (Py_ssize_t)(self->res.bins * sizeof(float_ti));
        view->len = self->strides[0] * 2;
    }
    self->strides[1] = (Py_ssize_t)sizeof(float_ti);
    view->itemsize = self->strides[1];
    view->shape = (Py_ssize_t *)self->shape;
    view->strides = (Py_ssize_t *)self->strides;
    view->suboffsets = NULL;
    view->internal = NULL;
    Py_INCREF(self);
    return 0;
}


static void cgracio_results_dealloc(cgracio_results *self)
{
    destroy_results(&self->res);
    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyBufferProcs cgracio_results_as_buffer = {
  (getbufferproc)cgracio_results_getbuffer,
  (releasebufferproc)0,
};


static PyTypeObject cgracio_results_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    TP_NAME_RESULTS,                            /* tp_name */
    sizeof(cgracio_results),                    /* tp_basicsize */
    0,                                          /* tp_itemsize */
    (destructor)cgracio_results_dealloc,        /* tp_dealloc */
    0,                                          /* tp_print */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    0,                                          /* tp_reserved */
    0,                                          /* tp_repr */
    0,                                          /* tp_as_number */
    0,                                          /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    0,                                          /* tp_hash  */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    0,                                          /* tp_getattro */
    0,                                          /* tp_setattro */
    &cgracio_results_as_buffer,                 /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,                         /* tp_flags */
    "_results object",                          /* tp_doc */
    0,                                          /* tp_traverse */
    0,                                          /* tp_clear */
    0,                                          /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    0,                                          /* tp_iter */
    0,                                          /* tp_iternext */
    0,                                          /* tp_methods */
    0,                                          /* tp_members */
    0,                                          /* tp_getset */
    0,                                          /* tp_base */
    0,                                          /* tp_dict */
    0,                                          /* tp_descr_get */
    0,                                          /* tp_descr_set */
    0,                                          /* tp_dictoffset */
    (initproc)cgracio_results_init,             /* tp_init */
    0,                                          /* tp_alloc */
    PyType_GenericNew,                          /* tp_new */
};


static PyMethodDef cgracio_methods[] = {
    {NULL, NULL, 0, NULL}
};


struct module_state {
    PyObject *error;
};


#define GETSTATE(m) ((struct module_state*)PyModule_GetState(m))


static int cgracio_traverse(PyObject *m, visitproc visit, void *arg)
{
    Py_VISIT(GETSTATE(m)->error);
    return 0;
}


static int cgracio_clear(PyObject *m)
{
    Py_CLEAR(GETSTATE(m)->error);
    return 0;
}


static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    TP_NAME,
    NULL,
    sizeof(struct module_state),
    cgracio_methods,
    NULL,
    cgracio_traverse,
    cgracio_clear,
    NULL
};


PyMODINIT_FUNC MODULE_NAME(void)
{
    PyObject *module;
    struct module_state *st;

    if (PyType_Ready(&cgracio_integration_type) < 0 ||
        PyType_Ready(&cgracio_pos_type) < 0         ||
        PyType_Ready(&cgracio_results_type) < 0)
        return NULL;

    module = PyModule_Create(&moduledef);
    if (module == NULL)
        return NULL;
    st = GETSTATE(module);
    st->error = PyErr_NewException(TP_NAME_ERROR, NULL, NULL);
    if (st->error == NULL) {
        Py_DECREF(module);
        return NULL;
    }

    Py_INCREF(&cgracio_pos_type);
    PyModule_AddObject(module, "_pos", (PyObject *)&cgracio_pos_type);

    Py_INCREF(&cgracio_integration_type);
    PyModule_AddObject(module, "_integration", (PyObject *)&cgracio_integration_type);

    Py_INCREF(&cgracio_results_type);
    PyModule_AddObject(module, "_results", (PyObject *)&cgracio_results_type);

    return module;
}
