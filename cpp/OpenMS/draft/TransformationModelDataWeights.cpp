// --------------------------------------------------------------------------
//                   OpenMS -- Open-Source Mass Spectrometry
// --------------------------------------------------------------------------
// Copyright The OpenMS Team -- Eberhard Karls University Tuebingen,
// ETH Zurich, and Freie Universitaet Berlin 2002-2017.
//
// This software is released under a three-clause BSD license:
//  * Redistributions of source code must retain the above copyright
//    notice, this list of conditions and the following disclaimer.
//  * Redistributions in binary form must reproduce the above copyright
//    notice, this list of conditions and the following disclaimer in the
//    documentation and/or other materials provided with the distribution.
//  * Neither the name of any author or any participating institution
//    may be used to endorse or promote products derived from this software
//    without specific prior written permission.
// For a full list of authors, refer to the file AUTHORS.
// --------------------------------------------------------------------------
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
// ARE DISCLAIMED. IN NO EVENT SHALL ANY OF THE AUTHORS OR THE CONTRIBUTING
// INSTITUTIONS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
// EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
// PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
// OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
// WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
// OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
// ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
// --------------------------------------------------------------------------
// $Maintainer: Douglas McCloskey $
// $Authors: Douglas McCloskey $
// --------------------------------------------------------------------------

#include <OpenMS/ANALYSIS/MAPMATCHING/TransformationModelDataWeights.h>

namespace OpenMS
{

  TransformationModelDataWeights::TransformationModelDataWeights()
  {  
  }

  TransformationModelDataWeights::~TransformationModelDataWeights()
  {
  }

  TransformationModelDataWeights::setParameters(const Param& params)
  {    
    if (params.exists("x_weight") && \
      (checkValidWeight(params.getValue("x_weight")), getValidXWeights())
    {
      x_weight_ = params.getValue("x_weight");
    }
    else{
      x_weight_ = '';
    }
    if (params.exists("y_weight") && \
      (checkValidYWeight(params.getValue("y_weight")), getValidYWeights())
    {
      y_weight_ = params.getValue("y_weight");
    }
    else{
      y_weight_ = '';
    }
  }

  void TransformationModelDataWeights::getParameters(string& x_weight, string& y_weight) const
  {
    x_weight = x_weight_;
    y_weight = y_weight_;
  }

  void TransformationModelDataWeights::getDefaultParameters(Param& params)
  {
    params.clear();
    params.setValue("x_weight", "", "Weight x values");
    params.setValidStrings("x_weight",
                           ListUtils::create<String>('1/x','1/x2','ln(x)',''));
    params.setValue("y_weight", "", "Weight y values");
    params.setValidStrings("y_weight",
                           ListUtils::create<String>('1/y','1/y2','ln(y)',''));
  }
  
  /// TransformationModelDataWeights::weightData
  /// Weighting type	Weight (w)
  /// Always 1.0.
  /// 1 / x	If |x| < 10-5 then w = 10e5; otherwise w = 1 / |x|.
  /// 1 / x2	If |x| < 10-5 then w = 10e10; otherwise w = 1 / x2.
  /// 1 / y	If |y| < 10-8 then w = 10e8; otherwise w = 1 / |y|.
  /// 1 / y2	If |y| < 10-8 then w = 10e16; otherwise w = 1 / y2.
  /// ln x	If x < 0 an error is generated; otherwise if x < 10-5 then w = ln 105,
	/// otherwise w = |ln x|.
  void TransformationModelDataWeights::weightData(TransformationModelDataWeights::DataPoints& data) const
  {
    // weight x values
    for (size_t i = 0; i < size; ++i)
    {
    data[i].first = weightDatum(data[i].first,x_weight_);
    }
    // weight y values
    for (size_t i = 0; i < size; ++i)
    {
    data[i].second = weightDatum(data[i].second,y_weight_);
    }
  }

  bool TransformationModelDataWeights::checkValidWeight(const string& weight, const vector<string>& valid_weights) const
  {    
    int it=find(valid_weights.begin(), valid_weights.end(), weight);
    bool valid=false;
    if (it != valid_weights.end())
    {
      valid=true;
    }
    else
    {
      cout << "weight " + " is not supported" << endl;
    }
    return valid;
  }
  
  vector<string> TransformationModelDataWeights::getValidXWeights()
  {
    vector<string> valid_weights{'1/x','1/x2','ln(x)',''};
    return valid_weights;
  }
  
  vector<string> TransformationModelDataWeights::getValidYWeights()
  {
    vector<string> valid_weights{'1/y','1/y2','ln(y)',''};
    return valid_weights;
  }

  double TransformationModelDataWeights::weightDatum(double& datum, const string& weight)
  { 
    double datum_weighted = datum;   
    if (weight == 'ln(x)')
    {
      if datum < 10e-5:
        datum = log(10e5);
      else:
        datum_weighted = abs(log(datum));
    }
    if (weight == 'ln(y)')
    {
      if datum < 10e-5:
        datum_weighted = log(10e5);
      else:
        datum_weighted = abs(log(datum));
    }
    else if (weight == '1/x')
    {
      if datum < 10e-5:
        datum_weighted = 1/10e5;
      else:
        datum_weighted = 1/abs(datum);
    }
    else if (weight == '1/y')
    {
      if datum < 10e-8:
        datum_weighted = 1/10e8;
      else:
        datum_weighted = 1/abs(datum);
    }
    else if (weight == '1/x2')
    {
      if datum < 10e-5:
        datum_weighted = 1/10e5;
      else:
        datum_weighted = 1/abs(pow(datum,2);
    }
    else if (weight == '1/y2')
    {
      if datum < 10e-8:
        datum_weighted = 1/10e8;
      else:
        datum_weighted = 1/abs(pow(datum,2);
    }
    else if (weight == '')
    {
      // do nothing
    }
    else:
    {
      cout << "wight " + wieght _ "not supported." << endl;
      cout << "no weighting will be applied." << endl;
    }
    return datum_weighted;
  }

} // namespace
