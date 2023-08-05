#include <stdlib.h>
#include <math.h>
#include "twoth.h"


struct geotri {
    float_ti s1;
    float_ti s2;
    float_ti s3;
    float_ti c1;
    float_ti c2;
    float_ti c3;
    float_ti c2c3;
    float_ti c3s1s2;
    float_ti c1s3;
    float_ti c1c3s2;
    float_ti s1s3;
    float_ti c2s3;
    float_ti c1c3;
    float_ti s1s2s3;
    float_ti c3s1;
    float_ti c1s2s3;
    float_ti c2s1;
    float_ti c1c2;
    float_ti dt1;
    float_ti dt2;
    float_ti dt3;
    float_ti c3s1s2c1s3;
    float_ti c1c3s1s2s3;
    float_ti pp1;
    float_ti pp2;
    float_ti dist2;
    float_ti tth2q;
    enum units_t units;
};


struct corners {
    void *mem;               /* pointer to a memory block to free it at once */
    int s_array;             /* size of the corners array = (dim1 + 1) * (dim2 + 2) */
    int s_array_buf;         /* size of the corners array buffer = s_array * sizeof(float_fi) */
    float_ti *rtth;          /* real two theta [q] calculated from poni */
    float_ti *rchi;          /* real chi (azimuthal angle) calculated from poni */
    float_ti *_dchi;         /* corner chi values */
    float_ti *_dtth;         /* corner tth values */
    float_ti *tth[4];        /* */
    float_ti *chi[4];        /* */
    float_ti *deltatth[4];   /* */
    float_ti *_deltatth[4];  /* */
    float_ti *deltachi[4];   /* */
    float_ti *_deltachi[4];  /* */
    float_ti *dtth[4];       /* */
    float_ti *dchi[4];       /* */
};


static int init_corners(struct integration *in, struct corners *crn)
{
    int i;
    float_ti *m;

    crn->s_array = (in->dim1 + 1) * (in->dim2 + 1);
    crn->s_array_buf = crn->s_array * sizeof(float_ti);

    crn->mem = malloc(crn->s_array_buf * 2 + in->s_array_buf * 10);
    if (!crn->mem)
        return 0;

    crn->rtth = (float_ti *)crn->mem;
    crn->rchi = crn->rtth + in->s_array;
    crn->_dtth = crn->rchi + in->s_array;
    crn->_dchi = crn->_dtth + crn->s_array;

    m = crn->_dtth + crn->s_array * 2;
    for (i=0; i<4; ++i) {
        crn->tth[i]       = crn->rtth;
        crn->chi[i]       = crn->rchi;
        crn->dtth[i]      = crn->_dtth;
        crn->dchi[i]      = crn->_dchi;
        crn->deltatth[i]  = m + in->s_array * i;
        crn->deltachi[i]  = m + in->s_array * 4 + in->s_array * i;
        crn->_deltatth[i] = crn->deltatth[i];
        crn->_deltachi[i] = crn->deltachi[i];
    }
    return 1;
}


static struct positions *alloc_positions(int nbins)
{
    int size;
    struct positions *pos;

    size = nbins * sizeof(float_ti);
    pos = malloc(sizeof(struct positions) + size);
    if (!pos)
        return NULL;

    pos->pos = (float_ti *)(pos + 1);
    pos->nbins = nbins;
    pos->s_pos_buf = size;
    pos->start = pos->stop = pos->step = 0;
    pos->lower = pos->upper = NULL;
    return pos;
}


static int init_positions(struct integration *in, struct geometry *geo)
{
    float_ti m;
    int anbins, rnbins;

    in->s_array = in->dim1 * in->dim2;
    in->s_array_buf = sizeof(float_ti) * in->s_array;

    if (geo->bins > 0)
        rnbins = geo->bins;
    else
        rnbins = (in->dim1 >= in->dim2 ? in->dim1 : in->dim2) * 2;
    anbins = geo->abins > 0 ? geo->abins : 360;

    /* these two objects may live much longer than the integration itself, thus, we have to allocate and
       destroy them separatelly */
    in->azimuth = alloc_positions(anbins);
    in->radial = alloc_positions(rnbins);
    if (!in->azimuth || !in->radial)
        return -1;

    in->use_sa = geo->sa;
    in->use_pol = (geo->pol >= -1 && geo->pol <= 1) ? 1 : 0;

    if (geo->radmax != geo->radmin) {
        m = geo->units == tth ? D2R : 1.0;
        in->radmax = geo->radmax * m;
        in->radmin = geo->radmin * m;
    } else {
        in->radmax = 0;
        in->radmin = 0;
    }

    in->mem = malloc(in->s_array_buf * 6);
    if (!in->mem)
        return 0;

    in->radial->lower = (float_ti *)in->mem;
    in->radial->upper = in->radial->lower + in->s_array;
    in->azimuth->lower = in->radial->upper + in->s_array;
    in->azimuth->upper = in->azimuth->lower + in->s_array;
    in->sa = in->azimuth->upper + in->s_array;
    in->pol = in->sa + in->s_array;
    return 1;
}


static void destroy_corners(struct corners *crn)
{
    if (crn->mem)
        free(crn->mem);
}


void destroy_integration(struct integration *in)
{
    if (in->mem)
        free(in->mem);
    in->dim1 = in->dim2 = in->s_array = in->s_array_buf = in->use_sa = in->use_pol = 0;
    in->radmax = in->radmin = 0;
    in->mem = in->sa = in->pol = NULL;
}


static void calc_sincos(struct geometry *geo, struct geotri *geo3)
{
    geo3->c1 = cos(geo->rot1);
    geo3->c2 = cos(geo->rot2);
    geo3->c3 = cos(geo->rot3);
    geo3->s1 = sin(geo->rot1);
    geo3->s2 = sin(geo->rot2);
    geo3->s3 = sin(geo->rot3);
    geo3->c2c3 = geo3->c2 * geo3->c3;
    geo3->c3s1s2 = geo3->c3 * geo3->s1 * geo3->s2;
    geo3->c1s3 = geo3->c1 * geo3->s3;
    geo3->c1c3s2 = geo3->c1 * geo3->c3 * geo3->s2;
    geo3->s1s3 = geo3->s1 * geo3->s3;
    geo3->c2s3 = geo3->c2 * geo3->s3;
    geo3->c1c3 = geo3->c1 * geo3->c3;
    geo3->s1s2s3 = geo3->s1 * geo3->s2 * geo3->s3;
    geo3->c3s1 = geo3->c3 * geo3->s1;
    geo3->c1s2s3 = geo3->c1 * geo3->s2 * geo3->s3;
    geo3->c2s1 = geo3->c2 * geo3->s1;
    geo3->c1c2 = geo3->c1 * geo3->c2;
    geo3->dt1 = geo->distance * (geo3->c1c3s2 + geo3->s1s3);
    geo3->dt2 = geo->distance * (geo3->c3s1 - geo3->c1s2s3);
    geo3->dt3 = geo->distance * geo3->c1c2;
    geo3->c3s1s2c1s3 = geo3->c3s1s2 - geo3->c1s3;
    geo3->c1c3s1s2s3 = geo3->c1c3 + geo3->s1s2s3;
    geo3->pp1 = geo->pixelsize1 * 0.5 - geo->poni1;
    geo3->pp2 = geo->pixelsize2 * 0.5 - geo->poni2;
    geo3->dist2 = geo->distance * geo->distance;
    geo3->tth2q = 4e-9 * M_PI / geo->wavelength;
    geo3->units = geo->units;
}


static void calc_part(int i, struct corners *crn)
{
    *crn->deltatth[i] = fabs(*crn->dtth[i] - *crn->tth[i]);
    *crn->deltachi[i] = fmod(fabs(*crn->dchi[i] - *crn->chi[i]), M_PI2);
    crn->deltatth[i]++; crn->dtth[i]++; crn->tth[i]++;
    crn->deltachi[i]++; crn->dchi[i]++; crn->chi[i]++;
}


static void calc_corners(struct integration *in, struct corners *crn, int i, int j)
{
    if (i == 0 || j == 0) {
        crn->dtth[2]++;
        crn->dchi[2]++;
    } else {
        calc_part(2, crn);
    }
    if (i == 0 || j == in->dim2) {
        crn->dtth[1]++;
        crn->dchi[1]++;
    } else {
        calc_part(1, crn);
    }
    if (i == in->dim1 || j == 0) {
        crn->dtth[3]++;
        crn->dchi[3]++;
    } else {
        calc_part(3, crn);
    }
    if (i == in->dim1 || j == in->dim2) {
        crn->dtth[0]++;
        crn->dchi[0]++;
    } else {
        calc_part(0, crn);
    }
}


static void maxd(struct corners *crn, int i, float_ti *tth, float_ti *chi)
{
    int j;

    *tth = crn->_deltatth[0][i];
    *chi = crn->_deltachi[0][i];
    for (j=1; j<4; j++) {
        if (*tth < crn->_deltatth[j][i])
            *tth = crn->_deltatth[j][i];
        if (*chi < crn->_deltachi[j][i])
            *chi = crn->_deltachi[j][i];
    }
}


static void calc_bin_borders(struct positions *dst, struct positions *src)
{
    dst->nbins = src->nbins;
    dst->s_pos_buf = src->s_pos_buf;
    dst->pos = src->pos;
    src->step = (src->stop - src->start) / src->nbins;
    dst->start = src->start + 0.5 * src->step;
    dst->stop = src->stop - 0.5 * src->step;
    dst->step = (dst->stop - dst->start) / (dst->nbins - 1);
}


static void up_low(struct positions *pos, int i, float_ti *src, float_ti max)
{
    pos->upper[i] = src[i] + max;
    pos->lower[i] = src[i] - max;
    if (pos->lower[i] < pos->start)
        pos->start = pos->lower[i];
    if (pos->upper[i] > pos->stop)
        pos->stop = pos->upper[i];
}


static void linspace(struct positions *pos, float_ti coef)
{
    int i;

    for (i=0; i<pos->nbins; i++)
        pos->pos[i] = (pos->start + pos->step * i) * coef;
}


static void calc_bins(struct integration *in, struct corners *crn, struct geometry *geo)
{
    int i;
    float_ti maxdtth, maxdchi;
    struct positions rpos, apos;

    for (i=0; i<in->s_array; i++) {
        maxd(crn, i, &maxdtth, &maxdchi);
        up_low(in->radial, i, crn->rtth, maxdtth);
        up_low(in->azimuth, i, crn->rchi, maxdchi);
    }
    if (in->radial->start < 0)
        in->radial->start = 0;
    if (in->azimuth->stop > M_PI)
        in->azimuth->stop = M_PI;
    if (in->azimuth->start < -M_PI)
        in->azimuth->start = -M_PI;
    calc_bin_borders(&rpos, in->radial);
    calc_bin_borders(&apos, in->azimuth);
    linspace(&rpos, geo->units == tth ? R2D : 1);
    linspace(&apos, R2D);
}


static float_ti tth2q(float_ti value, struct geotri *geo3)
{
    return geo3->units == q ? geo3->tth2q * sin(0.5 * value) : value;
}


static void calc_pos(struct integration *in, struct corners *crn, struct geometry *geo, struct geotri *geo3)
{
    int i, j;
    float_ti p1, p2, t1, t2, t3, t11, t21, t31, dp1, dp2, *dtth, *dchi, *pol;
    float_ti dt11, dt21, dt31, dt1, dt2, dt3, p1i, p2j, p11, *tth, *sa, *chi, ctth;

    tth = crn->rtth;
    sa = in->sa;
    chi = crn->rchi;
    pol = in->pol;
    dtth = crn->_dtth;
    dchi = crn->_dchi;
    for (i=0; i<=in->dim1; i++) {
        p1i = geo->pixelsize1 * i;
        p1 = p1i + geo3->pp1;
        p11 = geo3->dist2 + p1 * p1;
        dp1 = p1i - geo->poni1;
        t11 = p1 * geo3->c2c3 - geo3->dt1;
        dt11 = dp1 * geo3->c2c3 - geo3->dt1;
        t21 = p1 * geo3->c2s3 + geo3->dt2;
        dt21 = dp1 * geo3->c2s3 + geo3->dt2;
        t31 = p1 * geo3->s2 + geo3->dt3;
        dt31 = dp1 * geo3->s2 + geo3->dt3;
        for (j=0; j<=in->dim2; j++) {
            p2j = geo->pixelsize2 * j;
            p2 = p2j + geo3->pp2;
            dp2 = p2j - geo->poni2;
            t1 = t11 + p2 * geo3->c3s1s2c1s3;
            dt1 = dt11 + dp2 * geo3->c3s1s2c1s3;
            t2 = t21 + p2 * geo3->c1c3s1s2s3;
            dt2 = dt21 + dp2 * geo3->c1c3s1s2s3;
            t3 = t31 - p2 * geo3->c2s1;
            dt3 = dt31 - dp2 * geo3->c2s1;
            *dtth++ = tth2q(atan2(sqrt(dt1 * dt1 + dt2 * dt2), dt3), geo3);
            *dchi++ = atan2(dt1, dt2);
            if (i != in->dim1 && j != in->dim2) {
                *sa++ = pow(geo->distance / sqrt(p11 + p2 * p2), DSA_ORDER);
                *tth = atan2(sqrt(t1 * t1 + t2 * t2), t3);
                *chi = atan2(t1, t2);
                ctth = pow(cos(*tth), 2);
                *pol++ = 0.5 * (1. + ctth - geo->pol * cos(2. * (*chi)) * (1. - ctth));
                *tth = tth2q(*tth, geo3);
                chi++;
                tth++;
            }
            calc_corners(in, crn, i, j);
        }
    }
    /* store first values as max and min bins */
    in->radial->start = in->radial->stop = *crn->rtth;
    in->azimuth->start = in->azimuth->stop = *crn->rchi;
}


int calculate_positions(struct integration *in, struct geometry *geo)
{
    struct geotri geo3;
    struct corners crn;

    crn.mem = NULL;
    if (!init_positions(in, geo))
        return 0;
    if (!init_corners(in, &crn)) {
        destroy_integration(in);
        return 0;
    }
    calc_sincos(geo, &geo3);
    calc_pos(in, &crn, geo, &geo3);
    calc_bins(in, &crn, geo);
    destroy_corners(&crn);
    return 1;
}


void destroy_positions(struct positions *pos)
{
    if (pos)
        free(pos);
}
