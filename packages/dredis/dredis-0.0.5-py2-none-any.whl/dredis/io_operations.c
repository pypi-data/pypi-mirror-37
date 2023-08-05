#include "Python.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void write_content(const char *fname, const char *content) {
    FILE *fp;
    fp = fopen(fname, "w");
    fputs(content, fp);
    fclose(fp);
}

void append_content(const char *fname, const char *content) {
    FILE *fp;
    fp = fopen(fname, "a");
    fputs(content, fp);
    fclose(fp);
}

PyObject *writePython(PyObject *self, PyObject *args) {
    char *cPath = NULL;
    char *cContent = NULL;
    if (!PyArg_ParseTuple(args, "ss", &cPath, &cContent))
        return NULL;
    write_content(cPath, cContent);
    Py_RETURN_NONE;
}

PyObject *appendPython(PyObject *self, PyObject *args) {
    char *cPath = NULL;
    char *cContent = NULL;
    if (!PyArg_ParseTuple(args, "ss", &cPath, &cContent))
        return NULL;
    append_content(cPath, cContent);
    Py_RETURN_NONE;
}

PyMethodDef methods[] = {
    {"write", (PyCFunction)writePython, METH_VARARGS},
    {"append", (PyCFunction)appendPython, METH_VARARGS},
    {NULL, NULL},
};

void initio_operations()
{
    Py_InitModule("io_operations", methods);
}