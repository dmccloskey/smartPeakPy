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

  _Test::DataPoints data;
  _Test::DataPoints test;
  Param param;
  _Test::getDefaultParameters(param);
  _Test dw(data, param);

  param.setValue("x_weight", "ln(x)");
  param.setValue("y_weight", "");
  test.clear();
  test.push_back(make_pair(std::log(0.0), 1.0));
  test.push_back(make_pair(std::abs(std::log(1.0)), 2.0));
  test.push_back(make_pair(std::abs(std::log(2.0)), 4.0));  
  data.clear();
  data.push_back(make_pair(0.0, 1.0));
  data.push_back(make_pair(1.0, 2.0));
  data.push_back(make_pair(2.0, 4.0));
  dw.weightData(data,param);
  for (size_t i = 0; i < data.size(); ++i)
  {
    TEST_REAL_SIMILAR(data[i].first,test[i].first);
  }
  // param.setValue("x_weight", "1/x")

  param.setValue("x_weight", "");
  param.setValue("y_weight", "ln(y)");
  test.clear();
  test.push_back(make_pair(0.0, std::abs(std::log(1.0))));
  test.push_back(make_pair(1.0, std::abs(std::log(2.0))));
  test.push_back(make_pair(2.0, std::abs(std::log(4.0))));  
  data.clear();
  data.push_back(make_pair(0.0, 1.0));
  data.push_back(make_pair(1.0, 2.0));
  data.push_back(make_pair(2.0, 4.0));
  dw.weightData(data,param);
  for (size_t i = 0; i < data.size(); ++i)
  {
    TEST_REAL_SIMILAR(data[i].second,test[i].second);
  }
  // param.setValue("x_weight", "1/x2")
  // test = "";
  // TEST_REAL_SIMILAR(dw.weightDatum(0.0,test), 1/10e5);
  // TEST_REAL_SIMILAR(dw.weightDatum(2.0,test), 1/abs(pow(2.0,2)));

  return 0;
} //end of main