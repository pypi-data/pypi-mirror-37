#include <stdio.h>
#include <stdlib.h>
#include <float.h>
#include <math.h>

// From http://rosettacode.org/wiki/Sutherland-Hodgman_polygon_clipping#C
// with some additions.

// If you edit this file, remember to re-build :
// $ sudo python setup.py build
// $ sudo python setup.py install

typedef struct { double x, y; } vec_t, *vec;

vec vec_new(void)
{
	return (vec)calloc(1, sizeof(vec_t));
}

void vec_free(vec v)
{
	free(v);
}

inline double dot(vec a, vec b)
{
	return a->x * b->x + a->y * b->y;
}

inline double cross(vec a, vec b)
{
	return a->x * b->y - a->y * b->x;
}

inline vec vsub(vec a, vec b, vec res)
{
	res->x = a->x - b->x;
	res->y = a->y - b->y;
	return res;
}

/**
 * Tells if vec c lies on the left side of directed edge a->b.
 * Returns 1 if left, -1 if right, 0 if colinear.
 */
int left_of(vec a, vec b, vec c)
{
	vec_t tmp1, tmp2;
	double x;
	vsub(b, a, &tmp1);
	vsub(c, b, &tmp2);
	x = cross(&tmp1, &tmp2);
	return x < 0 ? -1 : x > 0;
}

int line_sect(vec x0, vec x1, vec y0, vec y1, vec res)
{
	vec_t dx, dy, d;
	vsub(x1, x0, &dx);
	vsub(y1, y0, &dy);
	vsub(x0, y0, &d);
	/* x0 + a dx = y0 + b dy ->
	   x0 X dx = y0 X dx + b dy X dx ->
	   b = (x0 - y0) X dx / (dy X dx) */
	double dyx = cross(&dy, &dx);
	if (!dyx) return 0;
	dyx = cross(&d, &dx) / dyx;
	if (dyx <= 0 || dyx >= 1) return 0;

	res->x = y0->x + dyx * dy.x;
	res->y = y0->y + dyx * dy.y;
	return 1;
}

/** POLYGONS *****************************************************************/

// We optimized them a bit for 4 vertices, but they support any number of
// vertices.

typedef struct { int len, alloc; vec v; } poly_t, *poly;

poly poly_new(void)
{
	return (poly)calloc(1, sizeof(poly_t));
}

void poly_free(poly p)
{
	free(p->v);
	free(p);
}

void poly_append(poly p, vec v)
{
	if (p->len >= p->alloc) {
		p->alloc *= 2;
		if (!p->alloc) p->alloc = 4;
		p->v = (vec)realloc(p->v, sizeof(vec_t) * p->alloc);
	}
	p->v[p->len++] = *v;
}

/**
 * This works only if all of the following are true:
 *   1. poly has no colinear edges;
 *   2. poly has no duplicate vertices;
 *   3. poly has at least three vertices;
 *   4. poly is convex (implying 3).
 */
int poly_winding(poly p)
{
	return left_of(p->v, p->v + 1, p->v + 2);
}

void poly_edge_clip(poly sub, vec x0, vec x1, int left, poly res)
{
	int i, side0, side1;
	vec_t tmp;
	vec v0 = sub->v + sub->len - 1, v1;
	res->len = 0;

	side0 = left_of(x0, x1, v0);
	if (side0 != -left) poly_append(res, v0);

	for (i = 0; i < sub->len; i++) {
		v1 = sub->v + i;
		side1 = left_of(x0, x1, v1);
		if (side0 + side1 == 0 && side0)
			/* last point and current straddle the edge */
			if (line_sect(x0, x1, v0, v1, &tmp))
				poly_append(res, &tmp);
		if (i == sub->len - 1) break;
		if (side1 != -left) poly_append(res, v1);
		v0 = v1;
		side0 = side1;
	}
}

poly poly_clip(poly sub, poly clip)
{
	int i;
	poly p1 = poly_new(), p2 = poly_new(), tmp;

	int dir = poly_winding(clip);
	poly_edge_clip(sub, clip->v + clip->len - 1, clip->v, dir, p2);
	for (i = 0; i < clip->len - 1; i++) {
		tmp = p2; p2 = p1; p1 = tmp;
		if (p1->len == 0) {
			p2->len = 0;
			break;
		}
		poly_edge_clip(p1, clip->v + i, clip->v + i + 1, dir, p2);
	}

	poly_free(p1);

	return p2;
}

double poly_area(poly p)
{
    int i,k;
    vec vi, vk;
    int n = p->len;
    double area = 0.0;

    for (i=0; i<n; i++) {
        k = (i == n-1 ? 0 : i+1); // faster than k = (i+1) % n;
        vi = p->v + i;
        vk = p->v + k;
        area += vi->x * vk->y - vi->y * vk->x;
    }
    if (area < 0.) area = -area;

    return area / 2.0;
}

double min_x_of(poly p)
{
    int i;
    vec v;
    double min = DBL_MAX;

    for (i=0; i<p->len; i++) {
        v = p->v + i;
        if (v->x < min) min = v->x;
    }

    return min;
}

double min_y_of(poly p)
{
    int i;
    vec v;
    double min = DBL_MAX;

    for (i=0; i<p->len; i++) {
        v = p->v + i;
        if (v->y < min) min = v->y;
    }

    return min;
}

double max_x_of(poly p)
{
    int i;
    vec v;
    double max = DBL_MIN;

    for (i=0; i<p->len; i++) {
        v = p->v + i;
        if (v->x > max) max = v->x;
    }

    return max;
}

double max_y_of(poly p)
{
    int i;
    vec v;
    double max = DBL_MIN;

    for (i=0; i<p->len; i++) {
        v = p->v + i;
        if (v->y > max) max = v->y;
    }

    return max;
}
