#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

struct st_darray_dbl {
	double * data;
	size_t size;
	size_t len;
};

typedef struct st_darray_dbl darray_dbl;

void darray_dbl_new(darray_dbl *d, size_t initialsize)
{
	d->data = malloc(sizeof(double) * initialsize);
	assert(d->data);
	d->len = 0;
	d->size = initialsize;
};

void darray_dbl_push(darray_dbl *d, double e)
{
	if (d->len == d->size) {
		d->size *= 2;
		printf("  Reallocating for %zu elements.\n", d->size);
		d->data = realloc(d->data, sizeof(double) * d->size);
		assert(d->data);
	}
	d->data[d->len++] = e;
};

void darray_dbl_remove(darray_dbl *d, size_t index)
{
	assert(index < d->len);
	size_t i;

	for (i = index + 1; i < d->len; i++) {
		d->data[i - 1] = d->data[i];
	}
	d->len--;
};

void darray_dbl_insert(darray_dbl *d, size_t index, double e)
{
	assert(index <= d->len);
	size_t i;

	if (d->len == d->size) {
		d->size *= 2;
		d->data = realloc(d->data, sizeof(double) * d->size);
		assert(d->data);
	}
	for (i = d->len; i > index; i--) {
		d->data[i] = d->data[i - 1];
	}
	d->data[index] = e;
	d->len++;
};

void darray_dbl_free(darray_dbl *d)
{
	free(d->data);
	d->size = 0;
	d->len = 0;
};
