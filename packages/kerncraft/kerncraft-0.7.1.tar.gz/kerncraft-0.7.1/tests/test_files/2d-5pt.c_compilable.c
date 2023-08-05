#include "kerncraft.h"
#include <stdlib.h>

void dummy(void *);
extern int var_false;
int main(int argc, char **argv)
{
  const int M = atoi(argv[2]);
  const int N = atoi(argv[1]);
  double *a = aligned_malloc((sizeof(double)) * (M * N), 32);
  for (int i = 0; i < (M * N); ++i)
    a[i] = 0.49795506534730005;

  double *b = aligned_malloc((sizeof(double)) * (M * N), 32);
  for (int i = 0; i < (M * N); ++i)
    b[i] = 0.4150803324887108;

  double s;
  s = 0.7607425694244915;
  if (var_false)
  {
    dummy(a);
    dummy(b);
    dummy(&s);
  }

  for (int j = 1; j < (M - 1); ++j)
    for (int i = 1; i < (N - 1); ++i)
    b[i + (j * N)] = (((a[(i - 1) + (j * N)] + a[(i + 1) + (j * N)]) + a[i + ((j - 1) * N)]) + a[i + ((j + 1) * N)]) * s;


  if (var_false)
  {
    dummy(a);
    dummy(b);
    dummy(&s);
  }

}

