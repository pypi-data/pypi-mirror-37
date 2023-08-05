#ifndef CGRACIO_SPLITBBOX_H_   /* Include guard */
#define CGRACIO_SPLITBBOX_H_

#include "twoth.h"


struct limits {         /* structure holds radial and azimuthal limits for the integration */
    float_ti azmin;     /* azimuthal low limit */
    float_ti azmax;     /* azimuthal high limit */
    float_ti rdmin;     /* radial low limit */
    float_ti rdmax;     /* radial low limit */
    int azimuth;        /* apply? */
    int radial;         /*        */
};


struct results {
    void *mem;          /* pointer to a memory block to free it at once */
    int bins;
    float_ti *merge;
    float_ti *sigma;
    float_ti *sum;
    float_ti *count;
    struct limits lm;
    enum integration_type type;
    int rbins;
    int abins;
};


int integrate_image_radial(struct integration *in, float_ti *image, struct results *res);
int integrate_image_azimuth(struct integration *in, float_ti *image, struct results *res);
int integrate_image_2d(struct integration *in, float_ti *image, struct results *res);
void destroy_results(struct results *res);

#endif /* CGRACIO_SPLITBBOX_H_ */
