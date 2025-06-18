import matplotlib.pyplot as plt
import numpy as np
import os

d = os.path.join('rundir', 'deardorff')

f = ['out_dec_turb_uvw_t0_m1.csv', 
     'out_dec_turb_uvw_t1_m1.csv', 
     'out_dec_turb_uvw_t2_m1.csv']

n = 32

plt.figure(figsize=(7,4))

for i in range(3):

    data = np.loadtxt(os.path.join(d,f[i]), skiprows=1, delimiter=',').reshape(n,n,n,3)

    u = data[:,:,:, 0]
    v = data[:,:,:, 1]
    w = data[:,:,:, 2]

    u_hat = np.fft.fftn(u)/n**3
    v_hat = np.fft.fftn(v)/n**3
    w_hat = np.fft.fftn(w)/n**3
    tke_hat = 0.5 * (u_hat * np.conj(u_hat) + v_hat * np.conj(v_hat) 
                    + w_hat * np.conj(w_hat))

    L = 9 * 2 * np.pi / 100
    k0 = 2 * np.pi / L
    kmax = n / 2
    wn = k0 * np.arange(0, n, 1)
    vt = np.zeros_like(wn)

    for kx in range(n):
        rkx = kx
        if kx > kmax: 
            rkx = rkx - n
        
        for ky in range(n):
            rky = ky
            if ky > kmax: 
                rky = rky - n

            for kz in range(n):
                rkz = kz
                if kz > kmax: 
                    rkz = rkz - n

                rk = np.sqrt(rkx**2 + rky**2 + rkz**2)
                k = round(rk)
            
                vt[k] += tke_hat[kx,ky,kz]/k0

    plt.loglog(wn[1:], vt[1:], 'o-', label=f"t{i}")

plt.ylim(bottom=1e-6)
plt.xlabel('Wave Number / $m^{-1}$')
plt.ylabel("Kinetic Energy / $m^2/s^2$")
plt.legend()
plt.grid()

# Nyquist wavelength
plt.axvline(x = k0 * n / 2)

# Plot reference data
ref_data = np.loadtxt('cbcdata.txt')
ref_k = ref_data[1:,0] * 1e2
ref_vt = ref_data[1:,1:] * 1e-6

for i in range(3):
    plt.loglog(ref_k, ref_vt[:,i], color='black', lw=0.5)

plt.savefig("KE_spectrum.png", dpi=300, bbox_inches='tight')

