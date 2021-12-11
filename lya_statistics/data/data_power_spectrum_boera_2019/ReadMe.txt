================================================================================
Title: Revealing reionization with the thermal history of the intergalactic 
       medium: new constraints from the Lyman-{alpha} flux power spectrum 
Authors: Boera E., Becker G.D., Bolton J.S., Nasir F. 
================================================================================
Description of contents: These files contain the covariance matrices
    associated with the power spectra results presented in the manuscript.
    Each of the files corresponds to a different redshift bin:
    
    Cov_Matrixz=4.2.dat
    Cov_Matrixz=4.6.dat
    Cov_Matrixz=5.0.dat
    
System requirements: The files are binary Numpy multi-arrays and have been
created using Python 2.7 and Numpy 1.12.1. They are loadable on different
installations of Python 2 and Python 3. 

  
    >>> from numpy import *
    >>> with open('Cov_Matrixz=4.2.dat', 'rb') as f:
        loaded_matrix=load(f)


Additional comments: See Appendix K in the manuscript for the corresponding
flux power spectrum values.

================================================================================
