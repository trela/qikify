#include <Python.h>
 


static PyObject* slicesample(PyObject* self, PyObject* args)
{
    const char* name;
 
    if (!PyArg_ParseTuple(args, "s", &name))
        return NULL;
 
    printf("Hello %s!\n", name);
 
    Py_RETURN_NONE;
}
 
static PyMethodDef SliceSampleMethods[] =
{
     {"slicesample", slicesample, METH_VARARGS, "Slice sampling."},
     {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initslicesample(void)
{
     (void) Py_InitModule("slicesample", SliceSampleMethods);
}