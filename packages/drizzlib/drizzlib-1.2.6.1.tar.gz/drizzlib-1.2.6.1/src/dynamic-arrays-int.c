#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

struct st_darray_int {
	int * data;
	size_t size;
	size_t len;
};

typedef struct st_darray_int darray_int;

void darray_int_new(darray_int *d, size_t initialsize)
{
	d->data = malloc(sizeof(int) * initialsize);
	assert(d->data);
	d->len = 0;
	d->size = initialsize;
};

void darray_int_push(darray_int *d, int e)
{
	if (d->len == d->size) {
		d->size *= 2;
		d->data = realloc(d->data, sizeof(int) * d->size);
		assert(d->data);
	}
	d->data[d->len++] = e;
};

void darray_int_remove(darray_int *d, size_t index)
{
	assert(index < d->len);
	size_t i;

	for (i = index + 1; i < d->len; i++) {
		d->data[i - 1] = d->data[i];
	}
	d->len--;
};

void darray_int_insert(darray_int *d, size_t index, int e)
{
	assert(index <= d->len);
	size_t i;

	if (d->len == d->size) {
		d->size *= 2;
		d->data = realloc(d->data, sizeof(int) * d->size);
		assert(d->data);
	}
	for (i = d->len; i > index; i--) {
		d->data[i] = d->data[i - 1];
	}
	d->data[index] = e;
	d->len++;
};

void darray_int_free(darray_int *d)
{
	free(d->data);
	d->size = 0;
	d->len = 0;
};
