#include <Python.h>
#include "arrayobject.h"
#include "C_slicesample.h"
#include "math.h"

#define RANDF       ((double)rand()/(double)RAND_MAX)


static PyMethodDef _C_slicesampleMethods[] = {
    {"slicesample", slicesample, METH_VARARGS},
    {NULL, NULL}     /* Sentinel - marks the end of this structure */
};
  
  
void init_C_slicesample()
{
     (void) Py_InitModule("_C_slicesample", _C_slicesampleMethods);
     import_array();
}

static PyObject *slicesample(PyObject* self, PyObject* args)
{    
    PyArrayObject *vecin, *vecout;
    double width;
    int maxiter;
    
    double *py_x0, *py_out, *rnd, *RW, *RD, *xl, *xr, *xp;
    double z;
    int i, n, dims[2], iteration;
    
    if (!PyArg_ParseTuple(args, "O!di", &PyArray_Type, &vecin, &width, &maxiter))
        return NULL;
    if (NULL == vecin) return NULL;
    if (!is_double_vector(vecin)) return NULL;
       
    n       = dims[0] = vecin->dimensions[0];
    vecout  = (PyArrayObject*) PyArray_FromDims(1,dims,NPY_DOUBLE);
    py_x0   = pyvector_to_Carrayptrs(vecin);
    py_out  = pyvector_to_Carrayptrs(vecout);
    
    /****** Ported Python code starts here ******/
    xl      = create1D_doubles(n);
    xr      = create1D_doubles(n);
    xp      = create1D_doubles(n);
    RW      = rand_array(create1D_doubles(n), n);
    RD      = rand_array(create1D_doubles(n), n);
    
    for ( i = 0; i < n; i++ )
    {
        RW[i] = RW[i] * width;
        xl[i] = py_x0[i] - RW[i];
        xr[i] = xl[i] + width;
    }
    
    z = logpdf(py_x0) - rand_exponential(1.0f);
    
    /* Univariate case */
    if ( n == 1)
    {
        iteration = 0;
        while ((logpdf(xl) > z) && iteration < maxiter)
        {
            xl[0] -= width;
            iteration += 1;
        }
        
        iteration = 0;
        while ((logpdf(xr) > z) && iteration < maxiter)
        {
            xr[0] += width;
            iteration += 1;
        }
    }
    for ( i = 0; i < n; i++ )
        xp[i] = RD[i]*(xr[i]-xl[i]) + xl[i];   
     
    /* Multi- and Uni-variate cases */   
    iteration = 0;
    while ((logpdf(xp) > z) && iteration < maxiter)
    {
        for ( i = 0; i < n; i++ )
        {
            if (xp[i] > py_x0[i])
                xr[i] = xp[i];
            else
                xl[i] = xp[i];
        }
        xp = rand_array(xp, n);
        for ( i = 0; i < n; i++ )
            xp[i] = (xp[i] * (xr[i] - xl[i])) + xl[i];

        iteration += 1;
    }
    
    for ( i = 0; i < n; i++ )
        py_out[i] = xp[i];

    
    free(xl);
    free(xr);
    free(xp);
    free(RW);
    free(RD);
    return PyArray_Return(vecout);
}
 
double *pyvector_to_Carrayptrs(PyArrayObject *arrayin)  
{
    return (double *) arrayin->data;  /* pointer to arrayin data as double */
} 
 
int is_double_vector(PyArrayObject *vec)  
{
    if (vec->descr->type_num != NPY_DOUBLE || vec->nd != 1)  {
        PyErr_SetString(PyExc_ValueError,
        "In not_doublevector: array must be of type Float and 1 dimensional (n).");
        return 0;  
    }
    return 1;
}

double *create1D_doubles(long n)  
{
    int i;
    double *v;
    v=(double *)malloc((size_t) (n*sizeof(double)));
    
    if (!v)   
    {
        printf("In **ptrintvector. Allocation of memory for int array failed.");
        exit(0);  
    }
    for ( i = 0; i < n; i++ )
    {
        v[i] = 0;
    }
    return v;
}


double rand_exponential(double lambda)
{
    return (-1.0f / lambda) * log(RANDF);
}

double* rand_array(double *v, long n)
{
    int i;
    for (i = 0; i < n; i++)
        v[i] = RANDF;
    return v;
}

double logpdf(double *v)
{
    double fx = 5.0f;
    return (fx > 0)? log(fx) : -INFINITY;
}