.. highlight:: shell

=================================================================
example LCMS MRM metabolomics (2): calibration curve optimization
=================================================================


Synopsis
--------
Calibration curve optimization of Standard samples by LC-MS/MS using multiple reaction monitoring (MRM) and stable isotope dilution mass spectrometry (IDMS).  The example is located in the folder "examples/LCMS_MRM".

Step 1: File conversion
-----------------------
1. Use proteoWizard to convert the raw data file to the open-source format .mzML (already done).
2. Drop the converted files in the folder "mzML".

Step 2: Specify the sequence of samples to run through the workflow
-------------------------------------------------------------------
1. Add filenames to run through the workflow to the file "sequence.csv".
2. Add additional metadata about the sample including the sample name and sample type (i.e., "Standard").

Step 3: Specify concentrations for each metabolite in each of the individual runs
---------------------------------------------------------------------------------
1. Add the run_id, component_name, actual_concentration, etc., to the file "standardsConcentrations.csv".
2. Ensure the "run_id" matches the name of the resulting featureXML sample name from Tutorial 1: part 1

Step 4: Define the parameters of the calibration curve fitting algorithm
------------------------------------------------------------------------
1. Specify the transformationModel, x_weight, y_weight, and x/y_min/max_weight for each of the transitions in the file "quantitationMethods.csv".
2. Specify the parameters of the calibration curve fitting algorithm in the file "parameters.csv" in the section "AbsoluteQuantitation"

Step 5: Modify the workflow parameters file
-------------------------------------------
1. Set false for all sections in the "parameters.csv" except for the "AbsoluteQuantitation" section.
2. See "parameters_tutorial1.2.csv" for an example.

Step 6: Run the workflow
------------------------
1. Ensure all files are saved
2. Start up Docker
3. Navigate the directory
4. Run the following command: `docker-compose up`