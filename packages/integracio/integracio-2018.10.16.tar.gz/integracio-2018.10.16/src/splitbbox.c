#include <stdlib.h>
#include <math.h>
#include "twoth.h"
#include "splitbbox.h"


void destroy_results(struct results *res)
{
    if (res->mem)
        free(res->mem);
    res->bins = res->lm.radial = res-> lm.azimuth = 0;
    res->lm.rdmax = res->lm.rdmin = res->lm.azmax = res->lm.azmin = 0;
    res->mem = res->merge = res->sigma = res->sum = res->count = NULL;
}


static int init_results(struct results *res, int bins)
{
    res->bins = bins;
    if (!(res->mem = calloc(res->bins * 2, sizeof(float_ti))))
        return 0;
    res->merge = (float_ti *)res->mem;
    res->sigma = res->merge + res->bins;
    res->count = res->merge;
    res->sum = res->sigma;
    return 1;
}


static void set_limits(struct limits *lm)
{
    if (lm->azmin != lm->azmax) {       /* worry about the azimuthal angles */
        if (lm->azmin > 180)
            lm->azmin -= 360;
        if (lm->azmax > 180)
            lm->azmax -= 360;
        lm->azmin *= D2R;
        lm->azmax *= D2R;
        if (lm->azmax < lm->azmin)
            lm->azmax += M_PI2;
        lm->azimuth = 1;
    } else {
        lm->azimuth = 0;
    }
    lm->radial = lm->rdmin == lm->rdmax ? 0 : 1;
}


static float_ti get_bin(float_ti start, float_ti stop, float_ti step)
{
    return (stop - start) / step;
}


static int in_limits(int i, float_ti *image, struct integration *in, struct results *res)
{
    if (image[i] < 0) /* intensity is unreasonable */
        return 0;
    if (res->lm.azimuth && (in->azimuth->lower[i] < res->lm.azmin || in->azimuth->upper[i] > res->lm.azmax))
        return 0;
    if (res->lm.radial && (in->radial->lower[i] < res->lm.rdmin || (in->radial->upper[i] > res->lm.rdmax)))
        return 0;
    return 1;
}


static void apply_corrections(int i, float_ti *image, struct integration *in)
{
    if (in->use_sa)
        image[i] /= in->sa[i];

    if (in->use_pol)
        image[i] /= in->pol[i];
}


static void sum_bins(struct results *res)
{
    int j;
    float_ti merge, sigma;

    for (j=0; j<res->bins; j++)
        if (res->count[j] > 0) {
            merge = res->sum[j] / res->count[j];
            sigma = sqrt(res->sum[j]) / res->count[j];
            res->merge[j] = merge;
            res->sigma[j] = sigma;
        }
}


struct bins {
    int      binmax;
    int      binmin;
    int      nbins;
    float_ti fbinmax;
    float_ti fbinmin;
};


static int get_bins(int i, struct positions *pos, struct bins *b)
{
    b->fbinmin = get_bin(pos->start, pos->lower[i], pos->step);
    b->fbinmax = get_bin(pos->start, pos->upper[i], pos->step);
    if (b->fbinmax < 0 || b->fbinmin >= pos->nbins)
        return 0;
    b->binmax = b->fbinmax >= pos->nbins ? pos->nbins - 1 : (int)b->fbinmax;
    b->binmin = b->fbinmin < 0 ? 0 : (int)b->fbinmin;
    return 1;
}


static void split_pixel(float_ti intensity, struct bins *b, struct results *res)
{
    int j;
    float_ti dA, dL, dR;

    if (b->binmin == b->binmax) {
        /* the whole pixel is within a single bin */
        res->count[b->binmin] += 1;
        res->sum[b->binmin] += intensity;
    } else {
        /* pixel is splitted */
        dA = 1 / (b->fbinmax - b->fbinmin);
        dL = (float_ti)(b->binmin + 1) - b->fbinmin;
        dR = b->fbinmax - (float_ti)b->binmax;
        res->count[b->binmin] += dA * dL;
        res->sum[b->binmin] += intensity * dA * dL;
        res->count[b->binmax] += dA * dR;
        res->sum[b->binmax] += intensity * dA * dR;
        if (b->binmin + 1 < b->binmax)
            for (j=b->binmin + 1; j<b->binmax; j++) {
                res->count[j] += dA;
                res->sum[j] += intensity * dA;
            }
    }
}


static int integrate_image(struct integration *in, float_ti *image, struct results *res, struct positions *pos)
{
    int i;
    struct bins b;

    if (!init_results(res, pos->nbins))
        return 0;

    set_limits(&res->lm);
    for (i=0; i<in->s_array; i++)
        if (in_limits(i, image, in, res) && get_bins(i, pos, &b)) {
            apply_corrections(i, image, in);
            split_pixel(image[i], &b, res);
        }
    sum_bins(res);
    return 1;

}


static void split_pixel2d(float_ti intensity, struct bins *r, struct bins *a, struct results *res)
{
    int i, j, k, l, m, n, o, p, q, s;
    float_ti dA, dL, dR, dU, dD;

    i = r->binmin * a->nbins;
    j = i + a->binmin;
    k = i + a->binmax;
    n = r->binmax * a->nbins;
    o = n + a->binmin;
    p = n + a->binmax;
    if (r->binmin == r->binmax) {
        if (a->binmin == a->binmax) {
            res->count[j] += 1;
            res->sum[j] += intensity;
        } else {
            dD = ((float_ti)(a->binmin + 1)) - a->fbinmin;
            dU = a->fbinmax - (float_ti)a->binmax;
            dA = 1. / (a->fbinmax - a->fbinmin);
            res->count[j] += dA * dD;
            res->sum[j] += intensity * dA * dD;
            res->count[k] += dA * dU;
            res->sum[k] += intensity * dA * dU;
            for (l=a->binmin+1; l<a->binmax; l++) {
                m = i + l;
                res->count[m] += dA;
                res->sum[m] += intensity * dA;
            }
        }
    } else {
        if (a->binmin == a->binmax) {
            dA = 1. / (r->fbinmax - r->fbinmin);
            dL = ((float_ti)(r->binmin + 1)) - r->fbinmin;
            dR = r->fbinmax - ((float_ti)r->binmax);
            res->count[j] += dA * dL;
            res->sum[j] += intensity * dA * dL;
            res->count[o] += dA * dR;
            res->sum[o] += intensity * dA * dR;
            for (l=r->binmin+1; l<r->binmax; l++) {
                m = l * a->nbins + a->binmin;
                res->count[m] += dA;
                res->sum[m] += intensity * dA;
            }
        } else {
            dL = ((float_ti)(r->binmin + 1)) - r->fbinmin;
            dR = r->fbinmax - ((float_ti)r->binmax);
            dD = ((float_ti)(a->binmin + 1)) - a->fbinmin;
            dU = a->fbinmax - ((float_ti)a->binmax);
            dA = 1. / ((r->fbinmax - r->fbinmin) * (a->fbinmax - a->fbinmin));
            res->count[j] += dA * dL * dD;
            res->sum[j] += intensity * dA * dL * dD;
            res->count[k] += dA * dL * dU;
            res->sum[k] += intensity * dA * dL * dU;
            res->count[o] += dA * dR * dD;
            res->sum[o] += intensity * dA * dR * dD;
            res->count[p] += dA * dR * dU;
            res->sum[p] += intensity * dA * dR * dU;
            for(l=r->binmin+1; l<r->binmax; l++) {
                m = l * a->nbins + a->binmin;
                res->count[m] += dA * dD;
                res->sum[m] += intensity * dA * dD;
                for (q=a->binmin+1; q<a->binmax; q++) {
                    s = l * a->nbins + q;
                    res->count[s] += dA;
                    res->sum[s] += intensity * dA;
                }
                s = l * a->nbins + a->binmax;
                res->count[s] += dA * dU;
                res->sum[s] += intensity * dA * dU;
            }
            for (l=a->binmin+1; l<a->binmax; l++) {
                    q = i + l;
                    s = n + l;
                    res->count[q] += dA * dL;
                    res->sum[q] += intensity * dA * dL;
                    res->count[s] += dA * dR;
                    res->sum[s] += intensity * dA * dR;
            }
        }
    }
}

static void sum_bins2d(struct results *res) {
    int i, j, k;

    for (i=0; i<res->rbins; i++)
        for (j=0; j<res->abins; j++) {
            k = i * res->abins + j;
            if (res->count[k] > 0)
                res->merge[k] = res->sum[k] / res->count[k];
        }
}

int integrate_image_2d(struct integration *in, float_ti *image, struct results *res)
{
    int i;
    struct bins a, r;

    res->type = twodim;
    res->rbins = r.nbins = in->radial->nbins;
    res->abins = a.nbins = in->azimuth->nbins;
    if (!init_results(res, r.nbins * a.nbins))
        return 0;

    set_limits(&res->lm);
    for(i=0; i<in->s_array; i++)
        if (in_limits(i, image, in, res) && get_bins(i, in->radial, &r) && get_bins(i, in->azimuth, &a)) {
            apply_corrections(i, image, in);
            split_pixel2d(image[i], &r, &a, res);
        }
    sum_bins2d(res);
    return 1;
}


int integrate_image_radial(struct integration *in, float_ti *image, struct results *res)
{
    res->type = radial;
    return integrate_image(in, image, res, in->radial);
}


int integrate_image_azimuth(struct integration *in, float_ti *image, struct results *res)
{
    res->type = azimuthal;
    return integrate_image(in, image, res, in->azimuth);
}
