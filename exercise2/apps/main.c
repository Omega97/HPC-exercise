/*
 * Mandelbrot Set Generation using OpenMP
 */

#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include "mandelbrot.h"

#define DIM_X 1000
#define DIM_Y 1000
#define X_L -2.0
#define Y_L -1.0
#define X_R 0.5
#define Y_R 1.0
#define MAX_ITERATIONS 65535
#define OUTPUT_IMAGE "image.pgm"

int main(int argc, char **argv) {
  int n_x = (argc > 1) ? atoi(argv[1]) : DIM_X;
  int n_y = (argc > 2) ? atoi(argv[2]) : DIM_Y;
  double x_L = (argc > 3) ? atof(argv[3]) : X_L;
  double y_L = (argc > 4) ? atof(argv[4]) : Y_L;
  double x_R = (argc > 5) ? atof(argv[5]) : X_R;
  double y_R = (argc > 6) ? atof(argv[6]) : Y_R;
  int I_max = (argc > 7) ? atoi(argv[7]) : MAX_ITERATIONS;
  const char *output_image =
      (argc > 8) ? argv[8] : OUTPUT_IMAGE;

  omp_set_dynamic(0);

  printf("Number of OMP threads: %d\n", omp_get_max_threads());
  printf("Image dimensions: %d x %d\n", n_x, n_y);
  printf("Complex plane region: [%.2f, %.2f] x [%.2f, %.2f]\n", x_L, x_R, y_L,
         y_R);
  printf("Maximum number of iterations: %d\n", I_max);

  void *image = NULL;
  if (I_max < 256) {
    image = calloc((size_t)n_x * (size_t)n_y, sizeof(char));
  } else {
    image = calloc((size_t)n_x * (size_t)n_y, sizeof(short int));
  }

  if (image == NULL) {
    fprintf(stderr, "Failed to allocate image buffer\n");
    return 1;
  }

  double start_time = omp_get_wtime();

  generate_mandelbrot(n_x, n_y, 0, n_y, x_L, y_L, x_R, y_R, I_max, image);

  double end_time = omp_get_wtime();

  printf("Total Walltime (s): %f\n", end_time - start_time);

  write_pgm_image(image, I_max, n_x, n_y, output_image);
  printf("Wrote image to %s\n", output_image);

  free(image);
  return 0;
}