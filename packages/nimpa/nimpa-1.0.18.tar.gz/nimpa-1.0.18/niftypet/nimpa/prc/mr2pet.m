function out = mr2pet(imref, imflo, costfun, sep, tol, fwhm, params, graphics)

	cflags.cost_fun = costfun;
	cflags.sep = sep;
	cflags.tol = tol;
	cflags.fwhm = fwhm;
	cflags.params = params;
	cflags.graphics = graphics;

	VG = strcat(imref,',1');
	VF = strcat(imflo,',1');
    disp(imref);
    disp(imflo);

    spm_jobman('initcfg')

    x = spm_coreg(VG,VF,cflags);
    M = spm_matrix(x);

    out = M;
end

