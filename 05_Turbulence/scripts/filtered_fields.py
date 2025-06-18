import numpy as np
import matplotlib.pyplot as plt

# Set global font size
plt.rcParams.update({'font.size': 16})

# Domain
L = 1.0
N = 1000
x = np.linspace(0, L, N, endpoint=False)
dx = L / N

# Generate a richer high-frequency periodic field u(x)
np.random.seed(0)
k_values = np.arange(10, 60)  # more high-frequency content
amplitudes = np.random.rand(len(k_values)) - 0.5
u = sum(a * np.sin(2 * np.pi * k * x / L) for a, k in zip(amplitudes, k_values))

# Define narrower Gaussian filter in Fourier space
filter_width = 0.05 * L  # narrower filter
k = np.fft.fftfreq(N, d=dx) * 2 * np.pi
G_hat = np.exp(-0.5 * (k * filter_width)**2)

# Apply filter
u_hat = np.fft.fft(u)
u_bar = np.real(np.fft.ifft(u_hat * G_hat))

# Compute squares
u_squared = u**2
u_squared_hat = np.fft.fft(u_squared)
u_squared_bar = np.real(np.fft.ifft(u_squared_hat * G_hat))
u_bar_squared = u_bar**2

# Plot
fig, axs = plt.subplots(4, 1, figsize=(12, 12), sharex=True)

axs[0].plot(x, u, label='Original $u(x)$')
axs[0].set_ylabel('$u(x)$')
axs[0].legend()

axs[1].plot(x, u_bar, label='Filtered $\\bar{u}(x)$', color='orange')
axs[1].set_ylabel('$\\bar{u}(x)$')
axs[1].legend()

axs[2].plot(x, u_squared, label='$u(x)^2$', color='green')
axs[2].set_ylabel('$u^2$')
axs[2].legend()

axs[3].plot(x, u_squared_bar, label='$\\overline{u^2}(x)$', color='purple')
axs[3].plot(x, u_bar_squared, label='$\\bar{u}(x)^2$', color='red', linestyle='--')
axs[3].set_ylabel('Comparison')
axs[3].set_xlabel('x')
axs[3].legend(loc='center left', bbox_to_anchor=(0, 0.5))

plt.tight_layout()
plt.savefig("mean_square_vs_square_mean.png", dpi=300)
plt.show()
