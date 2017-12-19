.. highlight:: shell

==================
Tutorial 3: part 2
==================


Synopsis
-------- 
Relative quantitation of isotopomer distributions of Unknown samples by LC-MS/MS from enhanced product ion (EPI) scans using Data-Dependent Acqusition (DDA). example is located in the folder "examples/LCMS_MRM".

Step 1: Modify the workflow and spectrum filtering and selection parameters
---------------------------------------------------------------------------
1. Add in spectrum filtering parameters to the file "parameters.csv" in the section "TargetedSpectrumExtractor".
1. Set false for all sections in the "parameters.csv" except for the "AbsoluteQuantitation" section.
2. See "parameters_tutorial3.2.csv" for what the final "parameters.csv" file should look like.

Step 2: Specify the sequence of samples to run through the workflow
-------------------------------------------------------------------
1. Add filenames to run through the workflow to the file "sequence.csv".
2. Add additional metadata about the sample including the sample name and sample type (i.e., "Unknown").

Step 3: Run the workflow
------------------------
1. Ensure all files are saved
2. Start up Docker
3. Navigate the directory
4. Run the following command: `docker-compose up`