import numpy as np
import matplotlib.pyplot as plt


fig, axs =plt.subplots(1)
clust_data = np.random.random((10,3))
axs.axis('tight')
axs.axis('off')
the_table = axs.table(cellText=clust_data,loc='center')
plt.margins(0.0)
fig.tight_layout()
plt.show()