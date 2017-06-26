// // TEST: should never fail
// #include <cstdio>
// #include <iostream>

// int main()
// {
//     printf("hello");
//     std::cout << "hello";
//     return 0;
// }

#include <OpenMS/FILTERING/TRANSFORMERS/LinearResampler.h>
#include <OpenMS/FILTERING/SMOOTHING/SavitzkyGolayFilter.h>
#include <OpenMS/FORMAT/DTAFile.h>
#include <OpenMS/KERNEL/StandardTypes.h>
#include <iostream>
#include <string>
#include "/home/user/code/OpenMS/include/_Test.h"

#include <OpenMS/CONCEPT/ClassTest.h>

using namespace OpenMS;
using namespace std;

int main(int argc, const char** argv)
{
  // if (argc < 2) return 1;
  // // the path to the data should be given on the command line
  // string tutorial_data_path(argv[1]);
  
//   PeakSpectrum spectrum;

//   DTAFile dta_file;
//   dta_file.load(tutorial_data_path + "/data/Tutorial_SavitzkyGolayFilter.dta", spectrum);

//   LinearResampler lr;
//   Param param_lr;
//   param_lr.setValue("spacing", 0.01);
//   lr.setParameters(param_lr);
//   lr.raster(spectrum);

//   SavitzkyGolayFilter sg;
//   Param param_sg;
//   param_sg.setValue("frame_length", 21);
//   param_sg.setValue("polynomial_order", 3);
//   sg.setParameters(param_sg);
//   sg.filter(spectrum);

  _Test::DataPoints data, empty;
  data.push_back(make_pair(0.0, 1.0));
  data.push_back(make_pair(1.0, 2.0));
  data.push_back(make_pair(1.0, 4.0));

  Param param;
  _Test dw(data, param);
  string test;
  double datum;
  test = "ln(x)";
  datum = 0.0;
  dw.weightDatum(datum,test);
  TEST_REAL_SIMILAR(datum, log(10e5));
  datum = 2.0;
  dw.weightDatum(datum,test);
  TEST_REAL_SIMILAR(datum, abs(log(2.0)));
  test = "1/x";
  datum = 0.0;
  dw.weightDatum(datum,test);
  TEST_REAL_SIMILAR(datum, 1/10e5);
  datum = 2.0;
  dw.weightDatum(datum,test);
  TEST_REAL_SIMILAR(datum, 1/abs(2.0));
  test = "1/x2";
  datum = 0.0;
  dw.weightDatum(datum,test);
  TEST_REAL_SIMILAR(datum, 1/10e5);
  datum = 2.0;
  dw.weightDatum(datum,test);
  TEST_REAL_SIMILAR(datum, 1/abs(pow(2.0,2)));

  return 0;
} //end of main