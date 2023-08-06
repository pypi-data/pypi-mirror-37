function out = mr2pet(n)
    f = prod(1:n);
end



%==SPM parameters==
Fgraph = spm_figure('GetWin','Graphics');
Finter = spm_figure('GetWin','Interactive');

%Coregistration parameters
cflags.cost_fun = 'nmi';
cflags.sep = [4 2];k
cflags.tol = [0.0200 0.0200 0.0200 0.0010 0.0010 0.0010 ...
             0.0100 0.0100 0.0100 0.0010 0.0010 0.0010];
cflags.fwhm = [7 7];
cflags.params = [0 0 0 0 0 0];
cflags.graphics = 1;

%Reslicing parameters
rflags.mask = 0;
rflags.mean = 0;
rflags.interp = 1;
rflags.which = 1;
rflags.wrap = [0 0 0];
rflags.prefix = 'r';




cpth = '/home/pawel/AIBL-2/'; 
fmri = fopen([cpth 'mri.txt'],'r');
a = textscan(fmri, '%s','delimiter', '\n');
fclose(fmri);

fpet = fopen([cpth 'pet.txt'],'r');
b = textscan(fpet, '%s','delimiter', '\n');
fclose(fpet);

if size(a{1},1)==size(b{1},1)
    disp('All is well')
else
    error('The number of PET and MRI images is different!')
    return
end


for i = 1:size(a{1},1)
    VG = a{1}{i};
    VF = b{1}{i};
    disp([num2str(i) '-th couple:']);
    disp(['MRI: ' VG]);
    disp(['PET: ' VF]);
    
    spm_jobman('initcfg')
    %coregistraion
    x = spm_coreg(VG,VF,cflags);     
    M  = spm_matrix(x);
    MM = zeros(4,4);
    MM(:,:) = spm_get_space(VF);
    spm_get_space(VF, M\MM(:,:));
    %reslicing (just for reference)
    P = {VG; VF};
    spm_reslice(P,rflags)
    disp('=================')
end

