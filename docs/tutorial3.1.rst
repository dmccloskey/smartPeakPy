.. highlight:: shell

==================
Tutorial 3: part 1
==================


Synopsis
-------- 
Relative quantitation of isotopomer distributions of Unknown samples by LC-MS/MS using multiple reaction monitoring (MRM). example is located in the folder "examples/LCMS_MRM".

Step 1: File conversion
-----------------------
1. Use proteoWizard to convert the raw data file to the open-source format .mzML (already done).
2. Drop the converted files in the folder "mzML".

Step 2: Define the target transitions
-------------------------------------
1. Add the target transition definition into the file "traML.csv".

Step 3: Compound and transition filtering and QC parameters
-----------------------------------------------------------
1. Add compound and transition filtering criteria to the file "featureFilters.csv".
2. Add compound and transition QC criteria to the file "featureQCs.csv".

Step 4: Define workflow and peak picking and selecting parameters
-----------------------------------------------------------------
1. Add workflow, peak picking, peak filter, peak selection, peak plotting, and peak QC parameters to the file "parameters.csv".

Step 5: Specify the sequence of samples to run through the workflow
-------------------------------------------------------------------
1. Add filenames to run through the workflow to the file "sequence.csv".
2. Add additional metadata about the sample including the sample name and sample type (i.e., "Unknown").

Step 6: Run the workflow
------------------------
1. Ensure all files are saved
2. Start up Docker
3. Navigate the directory
4. Run the following command: `docker-compose up`