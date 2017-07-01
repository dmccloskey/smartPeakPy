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
#include "/home/user/code/OpenMS/include/_TransformationModelTEST.h"
#include "/home/user/code/OpenMS/include/_TransformationModelLinearTEST.h"

#include <OpenMS/CONCEPT/ClassTest.h>

using namespace OpenMS;
using namespace std;

// code snippet testing
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

_TransformationModelLinearTEST* ptr = 0;
_TransformationModelLinearTEST* nullPointer = 0;

_TransformationModelTEST::DataPoints data, empty;
data.push_back(make_pair(0.0, 1.0));
data.push_back(make_pair(1.0, 2.0));
data.push_back(make_pair(1.0, 4.0));

  data.push_back(make_pair(2.0, 2.0));
  Param p_in;

  p_in.setValue("symmetric_regression", "true");
  p_in.setValue("x_weight", "");
  p_in.setValue("y_weight", "");
  _TransformationModelLinearTEST lm(data, p_in);
  Param p_out = p_in;
  p_out.setValue("slope", 0.5);
  p_out.setValue("intercept", 1.75);
  TEST_EQUAL(lm.getParameters(), p_out);

  p_in.clear();
  p_in.setValue("slope", 12.3);
  p_in.setValue("intercept", -45.6);
  p_in.setValue("x_weight", "ln(x)");
  p_in.setValue("y_weight", "");
  _TransformationModelLinearTEST lm2(empty, p_in);
  TEST_EQUAL(lm2.getParameters(), p_in);

  return 0;
} //end of main