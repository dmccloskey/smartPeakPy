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
// $Maintainer: $
// $Authors: Hendrik Weisser $
// --------------------------------------------------------------------------

#include <OpenMS/ANALYSIS/MAPMATCHING/TransformationModel.h>

namespace OpenMS
{

  TransformationModel::TransformationModel(const TransformationModel::DataPoints&, const Param&) :
    params_()
  {
  }

  TransformationModel::~TransformationModel()
  {
  }

  double TransformationModel::evaluate(double value) const
  {
    return value;
  }

  const Param& TransformationModel::getParameters() const
  {
    return params_;
  }

  void TransformationModel::getDefaultParameters(Param& params)
  {
    params.clear();
  }
  
  /// TransformationModel::weightData
  /// Weighting type	Weight (w)
  /// Always 1.0.
  /// 1 / x	If |x| < 10-5 then w = 10e5; otherwise w = 1 / |x|.
  /// 1 / x2	If |x| < 10-5 then w = 10e10; otherwise w = 1 / x2.
  /// 1 / y	If |y| < 10-8 then w = 10e8; otherwise w = 1 / |y|.
  /// 1 / y2	If |y| < 10-8 then w = 10e16; otherwise w = 1 / y2.
  /// ln x	If x < 0 an error is generated; otherwise if x < 10-5 then w = ln 105,
	/// otherwise w = |ln x|.
  void TransformationModel::weightData(TransformationModel::DataPoints& data) const
  {
    // weight x values 
    if (params.exists("x_weight") && \
      (checkValidWeight(params.getValue("x_weight")), getValidXWeights())
    {
      x_weight_ = params.getValue("x_weight");
      for (size_t i = 0; i < size; ++i)
      {
      data[i].first = weightDatum(data[i].first,x_weight_);
      }
    }
    else{
      x_weight_ = "";
    }
    // weight y values
    if (params.exists("y_weight") && \
      (checkValidYWeight(params.getValue("y_weight")), getValidYWeights())
    {
      y_weight_ = params.getValue("y_weight");
      for (size_t i = 0; i < size; ++i)
      {
      data[i].second = weightDatum(data[i].second,y_weight_);
      }
    }
    else{
      y_weight_ = "";
    }
  }

  bool TransformationModel::checkValidWeight(const std::string& weight, const std::vector<std::string>& valid_weights) const
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
  
  vector<std::string> TransformationModel::getValidXWeights()
  {
    std::vector<std::string> valid_weights{"1/x","1/x2","ln(x)",""};
    return valid_weights;
  }
  
  std::vector<std::string> TransformationModel::getValidYWeights()
  {
    std::vector<std::string> valid_weights{"1/y","1/y2","ln(y)",""};
    return valid_weights;
  }

  double TransformationModel::weightDatum(double& datum, const std::string& weight)
  { 
    double datum_weighted = datum;   
    if (weight == "ln(x)")
    {
      if datum < 10e-5:
        datum = log(10e5);
      else:
        datum_weighted = abs(log(datum));
    }
    if (weight == "ln(y)")
    {
      if datum < 10e-5:
        datum_weighted = log(10e5);
      else:
        datum_weighted = abs(log(datum));
    }
    else if (weight == "1/x")
    {
      if datum < 10e-5:
        datum_weighted = 1/10e5;
      else:
        datum_weighted = 1/abs(datum);
    }
    else if (weight == "1/y")
    {
      if datum < 10e-8:
        datum_weighted = 1/10e8;
      else:
        datum_weighted = 1/abs(datum);
    }
    else if (weight == "1/x2")
    {
      if datum < 10e-5:
        datum_weighted = 1/10e5;
      else:
        datum_weighted = 1/abs(pow(datum,2);
    }
    else if (weight == "1/y2")
    {
      if datum < 10e-8:
        datum_weighted = 1/10e8;
      else:
        datum_weighted = 1/abs(pow(datum,2);
    }
    else if (weight == "")
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

}
