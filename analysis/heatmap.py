import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

data_decameron = {
    "I": [0.9961, 0.2349, 0.1222, 0.2559, 0.0208, 0.2095, -0.2352, -0.2927, -0.4527, 0.1552],
    "II": [0.2284, 0.9954, 0.0374, 0.1734, 0.2262, 0.0075, -0.2645, -0.3492, -0.3254, 0.1454],
    "III": [0.1238, 0.0245, 0.9963, 0.1004, -0.2502, 0.1104, 0.2353, -0.2272, -0.2278, -0.0191],
    "IV": [0.2554, 0.1680, 0.0897, 0.9940, 0.1810, 0.0330, 0.0688, -0.1454, -0.1921, -0.1572],
    "V": [0.0273, 0.2422, -0.2483, 0.1619, 0.9930, -0.2016, -0.1347, -0.2559, -0.0893, 0.1546],
    "VI": [0.2262, -0.0108, 0.0972, 0.0267, -0.1803, 0.9920, 0.0985, -0.0185, -0.0355, -0.0613],
    "VII": [-0.2337, -0.2469, 0.2622, 0.0687, -0.1347, 0.0985, 0.9955, 0.1966, 0.1972, -0.2636],
    "VIII": [-0.2881, -0.3305, -0.2250, -0.1294, -0.2559, -0.0252, 0.1937, 0.9969, 0.6373, -0.3662],
    "IX": [-0.4622, -0.3157, -0.2195, -0.1977, -0.0893, -0.0355, 0.2073, 0.6373, 0.9947, -0.3498],
    "X": [0.1692, 0.1339, -0.0156, -0.1419, 0.1546, -0.0613, -0.2636, -0.3662, -0.3374, 0.9962]
}

df_decameron = pd.DataFrame(data_decameron, index=["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"])

# Reverse the order of the rows and columns to maintain symmetry
df_decameron = df_decameron.iloc[::-1, ::-1]

# Create a mask for the upper triangle, including the diagonal
mask = np.triu(np.ones_like(df_decameron, dtype=bool))

plt.figure(figsize=(10, 8))
sns.heatmap(df_decameron, mask=mask, annot=True, fmt=".4f", cmap="RdYlGn", linewidths=.5)
plt.title("Symmetric Similarity Scores Across Days in the Decameron")
plt.show()
