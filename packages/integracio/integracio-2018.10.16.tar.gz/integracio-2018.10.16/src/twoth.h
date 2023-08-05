#ifndef CGRACIO_TWOTHETA_H_   /* Include guard */
#define CGRACIO_TWOTHETA_H_


#ifndef M_PI
#define M_PI       3.14159265358979323846
#endif  /* M_PI */
#define DSA_ORDER  3.0  /* by default we correct for 1/cos(2th), fit2d corrects for 1/cos^3(2th) */
#define R2D        180.0 / M_PI
#define D2R        M_PI / 180.0
#define M_PI2      2.0 * M_PI


#define QUOTE(name)       #name
#define STR(macro)        QUOTE(macro)
#define PPCAT_NX(A, B)    A ## B
#define PPCAT(A, B)       PPCAT_NX(A, B)
#define FLOAT_ID          f
#define DOUBLE_ID         d


#if !defined(USE_FLOATS) && !defined(USE_DOUBLES)
#define USE_FLOATS
#endif /* !defined(USE_FLOATS) && !defined(USE_DOUBLES) */


#ifdef USE_FLOATS
typedef float float_ti;
#define FLOAT_TYPE        FLOAT_ID
#endif /* USE_FLOATS */

#ifdef USE_DOUBLES
typedef double float_ti;
#define FLOAT_TYPE        DOUBLE_ID
#endif /* USE_DOUBLES */

#define SO_NAME           _cgracio
#define TP_NAME           STR(SO_NAME) "_" STR(FLOAT_TYPE)
#define TP_NAME_CGRACIO   TP_NAME "._integration"
#define TP_NAME_POS       TP_NAME "._positions"
#define TP_NAME_RESULTS   TP_NAME "._results"
#define TP_NAME_ERROR     TP_NAME ".Error"
#define MODULE_NAME       PPCAT(PPCAT(PPCAT(PyInit_, SO_NAME), _), FLOAT_TYPE)
#define EXPORT_TYPE       STR(FLOAT_TYPE)
#define IMPORT_TYPE       "OOi" STR(FLOAT_TYPE) STR(FLOAT_TYPE)


enum units_t {tth, q};


enum integration_type {
    radial,
    azimuthal,
    twodim
};


struct geometry {
    float_ti distance;
    float_ti poni1;
    float_ti poni2;
    float_ti pixelsize1;
    float_ti pixelsize2;
    float_ti rot1;
    float_ti rot2;
    float_ti rot3;
    float_ti wavelength;
    enum units_t units;
    float_ti radmin;
    float_ti radmax;
    float_ti pol;
    int sa;
    int bins;
    int abins;
};


struct positions {
    int nbins;         /* number of bins = sizeof(pos[]) */
    int s_pos_buf;     /* size of the bins buffer = bins * sizeof(float_ti) */
    float_ti start;    /* minimal bin value */
    float_ti stop;     /* maximal bin value */
    float_ti step;     /* step bin value */
    float_ti *pos;     /* array for bins */
    float_ti *lower;   /* array of min values for a certain bin */
    float_ti *upper;   /* array of max values for a certain bin */
};


struct integration {
    void *mem;                 /* pointer to a memory block to free it at once */
    int dim1;                  /* image array fastest dimension */
    int dim2;                  /* image array second dimension */
    int s_array;               /* size of the array = dim1 * dim2 */
    int s_array_buf;           /* size of the array buffer = s_array * sizeof(float_ti) */
    int use_sa;                /* use (1) or don't (0) solid angle correction */
    int use_pol;               /* use (1) or don't (0) polarization correction */
    float_ti radmin;           /* min radial value; both are copied from the geometry struct */
    float_ti radmax;           /* max radial value; there is no radial limits if radmin == radmax */
    float_ti *sa;              /* solid angle correction array */
    float_ti *pol;             /* polarization array */
    struct positions *radial;  /* radial bins */
    struct positions *azimuth; /* azimuthal bins */
};


int calculate_positions(struct integration *in, struct geometry *geo);
void destroy_integration(struct integration *in);
void destroy_positions(struct positions *pos);

#endif /* CGRACIO_TWOTHETA_H_ */
