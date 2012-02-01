
/* Python vector methods */
static PyObject* slicesample(PyObject* self, PyObject* args);

/* C vector functions */
double  *pyvector_to_Carrayptrs(PyArrayObject *arrayin);
int     is_double_vector(PyArrayObject *vec);
double  *rand_array(double *v, long n);
double  logpdf(double *v);

double  *create1D_doubles(long n);


/* C utility functions */
double rand_exponential(double lambda);
