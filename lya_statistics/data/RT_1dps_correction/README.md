This routine calculates the patchy correction R_zR(z_dash,k) as defined in Eqn. 2, Molaro et al. in prep, for EoR history models ending at redshift zR (defined as redshift at which the neutral hydrogen fraction first falls below 10^-3) in observational redshift bin z_dash

User-defined parameters:
- Range of EoR history models zR for which R_zR(z_dash,k) is calculated can be selected through the user-defined range limits and interval zRmin, zRmax, and dzR respectively, while k values at which R_zR(z_dash,k) is calculated can be selected using logkmin, logkmax, and dlogk.
- Ranges of zR and logk for which this approximation safely holds are 5.3<=zR<=6.7 and -2.9<=log10k<=-0.7 (see Molaro et al. in prep for further details).

Outputs:
- log10k_range.dat: log10k values considered:
- zR_range.dat: zR models considered;
- R_correction.dat: R_zR(z_dash,k) values, with each column referring to values for a different zR model;

If you use this script for your scientific work, we kindly ask you to please reference: Molaro et al. in prep (https://arxiv.org/abs/2109.06897)
