import matplotlib.pyplot as plt
import numpy as np
# x = [1,2,3,4]
# y= [1,4,9,16]
# plt.plot(x,y,"o--r")
# plt.axis([0,6,0,20])
# plt.title("Grafik Başlığı")
# plt.xlabel('X düzlemi')
# plt.ylabel('Y düzlemi')
# plt.show()
# x=np.linspace(0,2,100)
# plt.plot(x,x,label='linear',color='yellow')
# plt.plot(x,x**2,label='quadratic')
# plt.plot(x,x**3,label='cubic')
# plt.xlabel('x label')
# plt.ylabel('Y label')
# plt.title('erdal')
# plt.legend()
# plt.show()
# x=np.linspace(0,2,100)
# fig,axs = plt.subplots(5)
# axs[0].plot(x,x,color='red')
# axs[1].plot(x,x**2,color='blue')
# axs[2].plot(x,x**2,color='yellow')
# axs[3].plot(x,x**2,color='blue',)

# axs[4].plot(x,x**2,color='yellow')
# plt.show()
import pandas as pd
df = pd.read_csv('nba.csv')
df = df.drop(['Number','Weight'], axis = 1).groupby('Team').mean().head(3)
df.plot(subplots=True)

plt.title('NBA')
plt.tight_layout()
plt.legend()

plt.show()
