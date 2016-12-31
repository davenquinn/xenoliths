I haven't found the model input files of the 2009 paper (not sure I've ever saved them), but did find some old files, which would do (almost) the same thing. Please be aware that the environment file is old format (pre-alphaMELTS), so you'll have to implement the equivalent options in your own alphaMELTS env. file.

The files I send you here are:

1. the environment file 'adiabat_env.dat' (you'll have to make an alphamelts_env.dat file setting the equivalent options and invoke it with the -f key, something like 'run_alphamelts.command -f alphamelts_env.dat'

2. the file with trace element partitioning values 'N&H97_trace.dat' invoked by 'adiabat_env.dat' (Niu, Y. L., and R. He´kinian (1997), Basaltic liquids and harzburgitic residues in the Garrett Transform: A case study at fast-spreading ridges, Earth Planet. Sci. Lett., 146, 243 – 258, doi:10.1016/S0012-821X(96)00218-X.) This is what I've used in that paper, though not the best / up to date option. Alternatively you can also try the attached 'Lee_trace.dat' (Lee, C. T. A., A. Harbert, and W. P. Leeman (2007), Extension of lattice strain theory to mineral/mineral rare-earth element partitioning: An approach for assessing disequilibrium and developing internally consistent partition coefficients between olivine, orthopyroxene, clinopyroxene and basaltic melt, Geochimica Et Cosmochimica Acta, 71, 481-496.)

3. files 'SMD_oPM_REE.melts' and 'WH_oDMM_REE-x.melts' representing primitive mantle and depleted morb mantle starting compositions.

In order to run the isentropic fractional melting scenario set in the environment file, you have to set initial T,P as close to the solidus as possible. Temps in the *.melts files are set to near solidus conditions at 2.5 GPa, but you should check the initial equilibrium (option 3 in alphaMELTS) and see if F is close to 0. 

