from pathlib import Path
import re
import numpy as np
import matplotlib.pyplot as plt

π      = np.pi
ri, ro = 0.89, 0.99
volume = 4*π * (ro**3 - ri**3 )/3

nHz = 2*π * 1e-9
day = 3600 * 24
Ω0  = 466  * nHz * day

μ0 = 4*π
ρ0 = 0.0309

shear = 1.0

fig = plt.figure(figsize=[7.3,3.5],dpi=600,constrained_layout=True,linewidth=2.0)

shears = []
gammas = []

for shear in np.arange(1.0, 15.0, 1.0):

    folder = Path('/home/lc876/dedalus_mri_code/MRI_Project/data/cont_shear_2/Shear_mult_{:.1f}/POLISHED_DATA/'.format(shear))
    if np.abs(shear-2.0) < 1e-8: #Shear of 2.0 produces an erroneous piece of data
        continue
    else:
        pattern = re.compile(r"polished_te(\d+)_Pnone")

        files = list(folder.glob("polished_te*_Pnone"))

        if not files:
            continue

        min_file = min(
            files,
            key=lambda f: int(pattern.search(f.name).group(1))
        )
        #print("Smallest file:", min_file)

        eig = np.load(str(min_file) + '/eigs.npy')
        γ, ω = eig[0].imag, eig[0].real

        growth =   1 / (γ*Ω0)
        period = 2*π / (ω*Ω0)

        #if growth > 400:
        #    continue

        shears.append(shear)
        gammas.append(γ)
m, b = np.polyfit(shears, gammas, 1)
x = np.float64(shears)
y_fit = m * x + b

plt.scatter(shears, gammas, marker='x', label='Calculated Mode')
plt.plot(shears, y_fit, color='red', linestyle='dashed', label='Line of Best Fit')
plt.xlabel("Shear Multiplier")
plt.ylabel("Growth (γ)")
plt.legend()
plt.savefig('/home/lc876/dedalus_mri_code/MRI_Project/' + 'Continuous_Shear_3.png')
