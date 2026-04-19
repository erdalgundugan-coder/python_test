import matplotlib.pyplot as plt
'''
yil =[2011,2012,2013,2014,2015]

oyuncu1 = [8,10,12,7,9]
oyuncu2 = [7,12,5,15,21]
oyuncu3 = [18,20,22,25,19]

#stack plot

plt.plot([],[],color='y',label='oyuncu1')
plt.plot([],[],color='r',label='oyuncu2')
plt.plot([],[],color='b',label='oyuncu3')

plt.stackplot(yil,oyuncu1,oyuncu2,oyuncu3,colors=["y","b","r"])
plt.title("yillara göre atılan goller")
plt.xlabel("yil")
plt.ylabel("gol sayisi")
plt.legend()
plt.show()

pay grafiği
goal_types ='penaltı','kaleye atılan şut','serbest vuruş'
goals =[12,35,7]

colors=['y','b','r']

plt.pie(goals,labels=goal_types,colors=colors, shadow=True,explode=(0.02,0.02,0.02),autopct='%1.1f%%')
plt.savefig('gol.png')
plt.show()
'''
plt.bar([2011,2012,2013,2015],[50,40,20,80],label="BMW",width=.8)
plt.bar([2009,2012,2014,2011],[25,15,55,10],label="Audi")

plt.legend()
plt.xlabel('gün')
plt.ylabel('Mesafe(Km)')
plt.title('Araç Bilgileri')
plt.show()
