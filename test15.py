import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns
config = {
    "font.family": 'Times New Roman',
}
rcParams.update(config)
df = pd.read_excel("FARFRR.xlsx")
plt.rcParams['font.size'] = 12
fig = plt.figure(figsize=(12, 8), clear=True, dpi=150)  # 设置画布大小
ax = fig.add_axes([0.2, 0.1, 0.8, 0.8])

h = sns.heatmap(df.values,  # 取数据
                vmin=4,
                annot=True,  # 图上显示数字
                fmt=".2f",

                cmap='Reds',  # RdYlGn
                cbar=False)

plt.axis('off')
# plt.title("r " + ' \u2011' + '10^-2')  # 标题
plt.tight_layout()
plt.savefig("result.png", dpi=150)
plt.show()