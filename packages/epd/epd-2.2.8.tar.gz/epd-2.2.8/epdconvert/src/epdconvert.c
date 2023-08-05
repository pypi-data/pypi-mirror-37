#define PY_SSIZE_T_CLEAN
#include <Python.h>

#if PY_MAJOR_VERSION >= 3
#define PY3K
#endif

#include "Type0.h"
#include "Type2.h"
#include "Compression.h"
#include "Invert.h"

static PyMethodDef module_methods[] = {
   {"toType0_1bit", (PyCFunction)convertToType0_1bit, METH_VARARGS | METH_KEYWORDS, "Conversion of data to Type0 2 bit format. Data is in bytes format as from PIL Image.tobytes()."},
   {"toType0_2bit", (PyCFunction)convertToType0_2bit, METH_VARARGS | METH_KEYWORDS, "Conversion of data to Type0 1 bit format. Data is in bytes format as from PIL Image.tobytes(). Image width (X size) is needed."},

   {"toType2_1bit", (PyCFunction)convertToType2_1bit, METH_VARARGS | METH_KEYWORDS, "Conversion of data to Type2 1 bit format. Data is in bytes format as from PIL Image.tobytes()."},

   {"invert", (PyCFunction)invert, METH_VARARGS | METH_KEYWORDS, "Inverts (bitwise) data."},

   {"compress_lz", (PyCFunction)compress_lz, METH_VARARGS | METH_KEYWORDS, "Method for EPD data compression according to LZ77 algorythm. Algorythm is based on BCL library, but modified to support smaller RAM footprint on TC."},
   {"compress_rle", (PyCFunction)compress_rle, METH_VARARGS | METH_KEYWORDS, "Method for EPD data compression according to RLE algorythm."},
   {NULL}
};

#ifdef PY3K
// module definition structure for python3
static struct PyModuleDef convert_mod =
{
    PyModuleDef_HEAD_INIT,
    "c_convert", /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,   /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    module_methods
};

PyMODINIT_FUNC PyInit_c_convert(void)
{
    return PyModule_Create(&convert_mod);
}
#else
// module initializer for python2
PyMODINIT_FUNC initc_convert(void)
{
    Py_InitModule("c_convert", module_methods);
}
#endif