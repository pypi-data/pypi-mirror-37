// Otherwise, compilation generates a warning.
// Unsure about the ripple effects of this on different numpy versions.
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

#include <Python.h>
#include <numpy/arrayobject.h>
#include <stdlib.h>
#include <stdio.h>
#include "dynamic-arrays-int.c"
#include "dynamic-arrays-dbl.c"
#include "rosetta-sutherland-hodgeman.c"

// If you edit this file, remember to re-build :
// $ sudo python setup.py install


/*** PYTHON 3 COMPATIBILITY **************************************************/

#if PY_MAJOR_VERSION >= 3
    #define PyInt_FromLong PyLong_FromLong
#endif


/*** MACROS ******************************************************************/

//#define LOG(f_, ...) printf("  [C] ", __VA_ARGS__)


/*** PURE C FUNCTIONS ********************************************************/

// The clipping nitty-gritty is defined in `rosetta-sutherland-hodgeman.c`.


// Because those are not defined in stdlib.
// https://answers.launchpad.net/ubuntu/+source/gnome-terminal/+question/82506
inline int min ( int a, int b ) { return a < b ? a : b; }
inline int max ( int a, int b ) { return a > b ? a : b; }


/**
 * Small util to make return a `PyList` with perfect size from a `list` that
 * may be longer because we do not know in advance the length of our results,
 * so we allocated to our upper bound and and now we just want to return to
 * python a nicely-sized PyList.
 *
 * Works ONLY with lists of `int`s.
 */
PyObject * make_int_pylist (int * list, int len)
{
    PyObject *pylist = PyList_New(len);
    if (!pylist) { return NULL; }

    int i; for (i = 0; i < len; i++) {
        PyObject *num = PyInt_FromLong((long)list[i]);
        if (!num) { Py_DECREF(pylist); return NULL; }
        PyList_SET_ITEM(pylist, i, num);   // reference to num stolen
    }

    return pylist;
}

/**
 * Small util to make return a `PyList` with perfect size from a `list` that
 * may be longer because we do not know in advance the length of our results,
 * so we allocated to our upper bound and and now we just want to return to
 * python a nicely-sized PyList.
 *
 * Works ONLY with lists of `double`s.
 */
PyObject * make_dbl_pylist (double * list, int len)
{
    PyObject *pylist = PyList_New(len);
    if (!pylist) { return NULL; }

    int i; for (i = 0; i < len; i++) {
        PyObject *num = PyFloat_FromDouble(list[i]);
        if (!num) { Py_DECREF(pylist); return NULL; }
        PyList_SET_ITEM(pylist, i, num);   // reference to num stolen
    }

    return pylist;
}


/*** PYTHON WRAPPERS *********************************************************/

/**
 * Returns a float, the area of the intersection between subject and clipper.
 *
 * About the vertices :
 * Provide at least 3.
 * The loop is closed automatically from the last vertice to the first, no
 * need for duplicates.
 *
 * subject: ndarray of shape (subject_len, 2)
 *   List of 2D vertices.
 * subject_len:
 *   Number of vertices of the subject.
 *   Usually 4, in drizzlib.
 *
 * ... same for clipper
 */
static PyObject * polyclip_intersection_area (PyObject *self, PyObject *args)
{
    // Convert our parameters from python to C
    PyObject * subject_obj, * clipper_obj;
    double ** subject_arr, ** clipper_arr;
    int subject_len, clipper_len;
    npy_intp dims[3]; /* PyArray_AsCArray is for ndim <= 3 */

    int parsing_ok;
    // Arguments: Object! Integer Object! Integer
    parsing_ok = PyArg_ParseTuple(args, "O!iO!i",
        &PyArray_Type, &subject_obj, &subject_len,
        &PyArray_Type, &clipper_obj, &clipper_len
    );

    if (! parsing_ok || NULL == subject_obj || NULL == clipper_obj) {
        PyErr_SetString(PyExc_TypeError, "Bad arguments.");
        return NULL;
    }

    int typenum = NPY_DOUBLE;
    PyArray_Descr * subject_descr = PyArray_DescrFromType(typenum);
    PyArray_Descr * clipper_descr = PyArray_DescrFromType(typenum);
    int subject_nd = PyArray_NDIM((PyArrayObject*)subject_obj);
    int clipper_nd = PyArray_NDIM((PyArrayObject*)clipper_obj);

    if (
        (PyArray_AsCArray(&subject_obj, (void *) &subject_arr, dims, subject_nd, subject_descr) < 0)
        | // or
        (PyArray_AsCArray(&clipper_obj, (void *) &clipper_arr, dims, clipper_nd, clipper_descr) < 0)
      ) {
        PyErr_SetString(PyExc_TypeError, "Error getting C array.");
        return NULL;
    }

    // Do the actual computation
    poly subject_poly = poly_new();
    poly clipper_poly = poly_new();

    int i; vec v;
    for (i=0; i<subject_len; i++) {
        v = vec_new();
        v->x = subject_arr[i][0];
        v->y = subject_arr[i][1];
        poly_append(subject_poly, v);
        free(v);
    }
    for (i=0; i<clipper_len; i++) {
        v = vec_new();
        v->x = clipper_arr[i][0];
        v->y = clipper_arr[i][1];
        poly_append(clipper_poly, v);
        free(v);
    }

    poly clipped_poly = poly_clip(subject_poly, clipper_poly);
    double area = poly_area(clipped_poly);

    // Clean up
    PyArray_Free(subject_obj, subject_arr);
    PyArray_Free(clipper_obj, clipper_arr);
    poly_free(subject_poly);
    poly_free(clipper_poly);
    poly_free(clipped_poly);

    return Py_BuildValue("d", area);
}


/**
 * Inner loop of wcs2healpix.
 * This is where all the polygon clipping happens.
 * There are no conversions or coordinates system awareness in this method.
 * All the input is already properly projected and sanitized if need be.
 * Parameters are described below in the code.
 *
 * Returns three same-sized lists, fit for sparse matrice initialization :
 *   - healpixels ids
 *   - y*x_dim+x : flattened wcs image pixel ids
 *   - weights (the shared area between the two corresponding pixels)
 * We flattened the second list because scipy's sparse matrices are 2D only.
 */
static PyObject * get_weights_for_hpixs (PyObject *self, PyObject *args, PyObject *kwargs)
{
    // Convert our parameters from python to C
    // Note that this is for (and only for) the python 2 version.
    // https://docs.python.org/2/extending/extending.html#keyword-parameters-for-extension-functions

    PyObject * hpix_polys_obj;
    PyObject * hpix_tally_obj;
    PyObject * wcs_image_obj;
    double *** hpix_polys_arr;
    double   * hpix_tally_arr;
    double  ** wcs_image_arr;
    int hpix_poly_len = 4;
    long hpix_cnt;
    int wcs_x_dim;
    int wcs_y_dim;
    long ignored_value;
    int should_ignore = 0;
    int is_origin_center = 0;

    static char *kwnames[] = {
        "hpix_polys",       /* Polygons, ndarray of shape (hpix_cnt,8,2) */
        "hpix_tally",       /* Tally of polygons per healpix, (hpix_cnt,) */
        "hpix_cnt",         /* total count of healpixels, aka npix */
        "wcs_data",         /* ndarray of shape (wcs_y_dim, wcs_x_dim) */
        "wcs_x_dim",        /* X dimension of the WCS data (int) */
        "wcs_y_dim",        /* Y dimension of the WCS data (int) */
        "ignored_value",    /* usually from BLANK (long) */
        "should_ignore",    /* only 1 (yes) or 0 (no), default 0 (int) */
        "is_origin_center", /* only 1 (yes) or 0 (no), default 0 (int) */
        NULL             /* sentinel (welcome to C) */
    };

    // See https://docs.python.org/2/c-api/arg.html
    static char *kwformat = "O!O!lO!ii|lii";

    int parsing_ok;
    parsing_ok = PyArg_ParseTupleAndKeywords(args, kwargs, kwformat, kwnames,
        &PyArray_Type, &hpix_polys_obj,
        &PyArray_Type, &hpix_tally_obj,
        &hpix_cnt,
        &PyArray_Type, &wcs_image_obj,
        &wcs_x_dim,
        &wcs_y_dim,
        &ignored_value,
        &should_ignore,
        &is_origin_center
    );

    if (! parsing_ok || NULL == hpix_polys_obj || NULL == hpix_tally_obj
                     || NULL == wcs_image_obj) {
        PyErr_SetString(PyExc_TypeError, "Bad arguments.");
        return NULL;
    }

    if (should_ignore) {
        printf("  Ignored Value is %ld.", ignored_value);
    } else {
        printf("  Won't ignore any value.");
    }

    // CONVERT INPUT AS C ARRAY ///////////////////////////////////////////////

    // Our input is mostly numpy ndarrays.
    // The conversion Python <=> C is really verbose, but it works.
    // We could probably remove more than half of the whole code of this file
    // by using a third-party lib that would handle all this clutter for us.

    int typenum = NPY_DOUBLE;
    // todo: inquire whether those descriptors are freed later (low priority)
    PyArray_Descr * hpix_polys_descr = PyArray_DescrFromType(typenum);
    PyArray_Descr * hpix_tally_descr = PyArray_DescrFromType(typenum);
    PyArray_Descr * wcs_image_descr = PyArray_DescrFromType(typenum);
    int hpix_polys_nd = PyArray_NDIM((PyArrayObject*)hpix_polys_obj);
    int hpix_tally_nd = PyArray_NDIM((PyArrayObject*)hpix_tally_obj);
    int wcs_image_nd = PyArray_NDIM((PyArrayObject*)wcs_image_obj);

    npy_intp hpix_polys_dims[3];
    npy_intp hpix_tally_dims[3];
    npy_intp wcs_image_dims[3];
    /* Note: PyArray_AsCArray is only for ndim <= 3 */
    if (
        (PyArray_AsCArray(&hpix_polys_obj, (void *) &hpix_polys_arr, hpix_polys_dims, hpix_polys_nd, hpix_polys_descr) < 0)
      ) {
        PyErr_SetString(PyExc_TypeError, "Error getting C array for hpix_polys.");
        return NULL;
    }
    if (
        (PyArray_AsCArray(&hpix_tally_obj, (void *) &hpix_tally_arr, hpix_tally_dims, hpix_tally_nd, hpix_tally_descr) < 0)
      ) {
        PyErr_SetString(PyExc_TypeError, "Error getting C array for hpix_tally.");
        return NULL;
    }
    if (
        (PyArray_AsCArray(&wcs_image_obj, (void *) &wcs_image_arr, wcs_image_dims, wcs_image_nd, wcs_image_descr) < 0)
      ) {
        PyErr_SetString(PyExc_TypeError, "Error getting C array for wcs_image.");
        return NULL;
    }


    // Prepare the output.
    // Three same-sized lists, fit for a sparse matrice initialization.
    darray_int hs;  // healpixels ids
    darray_int_new(&hs, hpix_cnt);
    darray_int ks;  // y * x_dim + x  <-- flattened wcs image pixel ids
    darray_int_new(&ks, hpix_cnt);
    darray_dbl ws;  // weights  (shared area between the two pixels above)
    darray_dbl_new(&ws, hpix_cnt);

    double x_off = 0.0;
    double y_off = 0.0;
    if (is_origin_center) {
        x_off = wcs_x_dim / 2.0;
        y_off = wcs_y_dim / 2.0;
    }

    printf("\n  Iterating...\n");


    // FOR EACH HEALPIXEL /////////////////////////////////////////////////////

    // Variables that will be used in the loop below
    int i, k; vec v; // `Locals for for` loops.
    int dbg_wcs_count = 0;
    long hpix_id; // From 0 to hpix_cnt-1, the HEALPix id of the cell.
    int x_min, x_max, y_min, y_max; // Boundaries of possible WCS pixels for each HEALPixel.

    // Cluttered syntax, but fastest I've tried.
    // We assume 4 sided polygons !
    // This poses problems, notably on the poles in full-sky projections, where
    // we may like to have 5 sided polygons in the future for better accuracy.
    // The idea of this is to do the memory allocation only once and reuse
    // those polygons and vectors on each loop with different values.
    // There's probably a way to do this and support 5-sided polygons too.
    poly wcs_poly = poly_new(); // Allocated once, reused on each WCS pixel.
    vec wcs_v_a = vec_new();
    vec wcs_v_b = vec_new();
    vec wcs_v_c = vec_new();
    vec wcs_v_d = vec_new();
    vec wcs_v;
    poly_append(wcs_poly, wcs_v_a);
    poly_append(wcs_poly, wcs_v_b);
    poly_append(wcs_poly, wcs_v_c);
    poly_append(wcs_poly, wcs_v_d);
    poly hpix_poly = poly_new(); // Allocated once, reused on each healpixel.
    vec hpix_v_a = vec_new();
    vec hpix_v_b = vec_new();
    vec hpix_v_c = vec_new();
    vec hpix_v_d = vec_new();
    vec hpix_v;
    poly_append(hpix_poly, hpix_v_a);
    poly_append(hpix_poly, hpix_v_b);
    poly_append(hpix_poly, hpix_v_c);
    poly_append(hpix_poly, hpix_v_d);
    poly clipped_poly;  // Instantiated by poly_clip.

    // We iterate over the healpixels
    for (hpix_id = 0 ; hpix_id < hpix_cnt ; hpix_id++) {

        // Because full-sky CAR projections are seamless on the left and right
        // edges, some healpixels must be projected twice.
        // To that effect, we sometimes packed multiple (2) polygons' vertices.
        // The hpix_tally keeps track for each healpixel of how many polygons
        // were packed.
        // We're now going to iterate on each polygon for this healpixel.
        // Note: there's usually only one.
        for (k = 0 ; k < hpix_tally_arr[hpix_id] ; k++) {

        // PREPARE HELPIX POLYGON /////////////////////////////////////////////

        // We need two `poly` structs to feed to `poly_clip`.
        // This will always be the subject polygon in the clipping.
        // It's a four-sided polygon that may have any convex shape.
        // Some concave shapes may be supported, but without crossing edges.

        hpix_v = hpix_poly->v;
        for (i=k; i<hpix_poly_len; i++) {
            hpix_v[i].x = ((hpix_polys_arr[hpix_id])[i])[0];
            hpix_v[i].y = ((hpix_polys_arr[hpix_id])[i])[1];
        }

        // LOOP ON THE WCS PIXELS IN THE REGION OF THE HEALPIX POLYGON ////////

        // Those are the WCS array indices boundaries, min inclusive, max
        // exclusive, for each healpixel.
        x_min = max((int) floor(min_x_of(hpix_poly)+x_off-1), 0);
        y_min = max((int) floor(min_y_of(hpix_poly)+y_off-1), 0);
        x_max = min((int) ceil(max_x_of(hpix_poly)+x_off+1), wcs_x_dim);
        y_max = min((int) ceil(max_y_of(hpix_poly)+y_off+1), wcs_y_dim);

        // Join east and west.
//        if (x_min == 0) { x_max = wcs_x_dim; }
//        if (x_max == wcs_x_dim) { x_min = 0; }
//        if (y_min == 0) { y_max = wcs_y_dim; }
//        if (y_max == wcs_y_dim) { y_min = 0; }

        //printf("  [C] Looping for x in [%d,%d[ and y in [%d,%d[\n", x_min, x_max, y_min, y_max);

//        int wcs_pixels_count = (x_max-x_min) * (y_max-y_min);
        // These arrays are pre-allocated with the upper bound of elements they may
        // hold, so there's some RAM wasted.
//        int * xs = malloc(sizeof(int) * wcs_pixels_count); // the X values, the
//        int * ys = malloc(sizeof(int) * wcs_pixels_count); // Y, also 0-indexed,
//        double * ws = (double *) malloc(sizeof(double) * wcs_pixels_count); // and the weights


    //    // debug
    //    ws[0] = 1.618;
    //    printf("LOOPING1 %f\n", ws[0]);
    //    free(ws);
    //    ws = malloc(sizeof(double) * wcs_pixels_count); // and the weights
    //    printf("LOOPING2 %f\n", ws[0]);

        // We're keeping track of how many values we actually are inserting in the
        // arrays above. One value for them all may suffice later, for a perf gain.
//        int xsi = 0;
//        int ysi = 0;
//        int wsi = 0;


        double x, y, area;
//        double wcs_poly_verts[4][2];

        dbg_wcs_count = 0;
        int x_ind, y_ind;
        // todo: benchmark X,Y loop vs Y,X loop (again)
        for (x_ind=x_min; x_ind<x_max; x_ind++)
        {
            for (y_ind=y_min; y_ind<y_max; y_ind++)
            {
                // FOR EACH WCS PIXEL /////////////////////////////////////////

                if (should_ignore) {
                    // Y,X order because it comes straight from third parties like
                    // astropy and they all seem to use Y,X order.
                    if (wcs_image_arr[y_ind][x_ind] == ignored_value) {
                        //printf("  [C] Ignored BLANK pixel (%d,%d)!\n", y_ind, x_ind);
                        continue; // skip that WCS pixel only
                    }
                }

                // Translate origin to center if CAR. We go to WCS pixel space.
                x = ((double)x_ind) - x_off;
                y = ((double)y_ind) - y_off;

                // Create its polygon vertices
                // We are defining square pixels of 1 because we are in WCS pixel
                // space. See utils._project_hpix_poly_to_wcs

//                wcs_poly_verts[0][0] = x;
//                wcs_poly_verts[0][1] = y;
//                wcs_poly_verts[1][0] = x;
//                wcs_poly_verts[1][1] = y+1;
//                wcs_poly_verts[2][0] = x+1;
//                wcs_poly_verts[2][1] = y+1;
//                wcs_poly_verts[3][0] = x+1;
//                wcs_poly_verts[3][1] = y;

                // Set the vertices of the pixel ABCD; bottom left, clockwise
                // This cluttered syntax is also very fast.
//                wcs_v_a->x=  x    ; wcs_v_a->y=  y    ;
//                wcs_v_b->x=  x    ; wcs_v_b->y=  y+1  ;
//                wcs_v_c->x=  x+1  ; wcs_v_c->y=  y+1  ;
//                wcs_v_d->x=  x+1  ; wcs_v_d->y=  y    ;
                wcs_v = wcs_poly->v;
                (wcs_v[0]).x=  x    ; (wcs_v[0]).y=  y    ;
                (wcs_v[1]).x=  x    ; (wcs_v[1]).y=  y+1  ;
                (wcs_v[2]).x=  x+1  ; (wcs_v[2]).y=  y+1  ;
                (wcs_v[3]).x=  x+1  ; (wcs_v[3]).y=  y    ;

                // fixme : WHICH IS IT ?!?!!!???
                // And if it can be both ; how to choose ? Which FITS header ?
                // Right now we are using the first one.
//                    { x    , y     },
//                    { x    , y + 1 },
//                    { x + 1, y + 1 },
//                    { x + 1, y     }
                // Or
//                    { x - .5, y - .5 },
//                    { x - .5, y + .5 },
//                    { x + .5, y + .5 },
//                    { x + .5, y - .5 },

                // Create its polygon struct
//                wcs_poly = poly_new();
//                for (i=0; i<4; i++) {
//                    v = vec_new();
//                    v->x = wcs_poly_verts[i][0];
//                    v->y = wcs_poly_verts[i][1];
//                    poly_append(wcs_poly, v);
//                    vec_free(v);
//                }


                // Compute the area of the intersection between the polygons.
                // The clipper is the WCS poly as we may rely on optimizations due
                // to its simple form of a square aligned with the axes.
                clipped_poly = poly_clip(hpix_poly, wcs_poly);
                area = poly_area(clipped_poly);

                if (area > 0.0) {
                    dbg_wcs_count++;
                    // The pixels intersect, let's add them to our output.
                    // darray stands for dynamic array, which is a naive but
                    // effective way of using arrays whose size we don't know
                    // in advance.
                    darray_int_push(&hs, hpix_id);
                    darray_int_push(&ks, y_ind * wcs_x_dim + x_ind);
                    darray_dbl_push(&ws, area);
                }

                poly_free(clipped_poly);
            }
        }

        }

        printf("  Done healpixel #%ld/%ld (%ld%%) with %d WCS pixels (area=%f).\n", hpix_id+1, hpix_cnt, 100 * (hpix_id+1) / hpix_cnt, dbg_wcs_count, poly_area(hpix_poly));

    } // end for each healpixel

    poly_free(hpix_poly);
    poly_free(wcs_poly);

    printf("\n");

    // Create the returned lists ; those are PyLists
    PyObject * w_pylist = make_dbl_pylist((&ws)->data, (&ws)->len);
    PyObject * h_pylist = make_int_pylist((&hs)->data, (&hs)->len);
    PyObject * k_pylist = make_int_pylist((&ks)->data, (&ks)->len);

    // Clean up

    PyArray_Free(hpix_polys_obj, hpix_polys_arr);
    PyArray_Free(hpix_tally_obj, hpix_tally_arr);
    PyArray_Free(wcs_image_obj, wcs_image_arr);

    darray_dbl_free(&ws);
    darray_int_free(&hs);
    darray_int_free(&ks);

    // I don't get why we don't need that.
    // Who's going to clean up ?
    // Py_DECREF(w_pylist);

    return Py_BuildValue("OOO", w_pylist, h_pylist, k_pylist);
}



/*** EXTENSION CONFIGURATION AND INITIALIZATION ******************************/


/*** COMMON ******************************************************************/

static PyMethodDef OptimizedMethods[] = {
    {
        "get_weights_for_hpixs",
        get_weights_for_hpixs,
        METH_VARARGS | METH_KEYWORDS,
        "Innermost loop of wcs2healpix, written in C for performance.\n"
        "WIP\n"
        "Parameters: TODO"
    },
    {
        "intersection_area",
        polyclip_intersection_area,
        METH_VARARGS,
        "Compute the area of the intersection between two polygons.\n"
        "Parameters: a_vertices, a_length, b_vertices, b_length"
    },
    {NULL, NULL, 0, NULL} /* Sentinel (because ... C) */
};


#if PY_MAJOR_VERSION >= 3
/*** PYTHON 3 ****************************************************************/

static struct PyModuleDef PolyclipModule =
{
    PyModuleDef_HEAD_INIT,
    /* module name */
    "optimized",
    /* module documentation, may be NULL */
    "Optimized calculus methods written in C for performance. Provides `intersection_area`.",
    /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    -1,
    /* module methods */
    OptimizedMethods

};

PyMODINIT_FUNC PyInit_optimized(void)
{
    // Enable support for numpy's arrays (defined in <numpy/arrayobject.h>)
    import_array();
    // Create the module and return it
    return PyModule_Create(&PolyclipModule);
}


#else
/*** PYTHON 2 ****************************************************************/

PyMODINIT_FUNC initoptimized (void)
{
    // Initialize our module with the methods described above
    (void) Py_InitModule("optimized", OptimizedMethods);
    // Enable support for numpy's arrays (defined in <numpy/arrayobject.h>)
    import_array();
}

#endif
