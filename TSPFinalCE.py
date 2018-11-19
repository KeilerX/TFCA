
# coding: utf-8

# In[16]:


import math
import heapq as hq
import csv
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
from datetime import datetime

start_time = datetime.now()
n1=100

#Leyendo el csv
def csvtxtCPR(CPdistsReg):
    textl = []
    with open('infoCE.csv','r') as ifile:
        reader = csv.reader(ifile)
        count = 0
        for row in reader:
            if count != 0:
                    name = str(count)+","+row[3]+","+row[5]+","+row[6]+"\n"
                    textl.append(name)
                    x = int(float(row[5])*100)
                    y = int(float(row[6])*100)
                    CPdistsReg.append((x,y))
            if count>n1:
                break
            count+=1
    with open('infoCPCE.txt','w') as ofile:
        ofile.truncate(0)
        for i in textl:
            ofile.write(str(i))
    
    file = open('infoCPCE.txt', 'r') 
    print(file.read())

#Calculando las distancias entre los puntos
def euclidean_distance(x1,y1,x2,y2):
    return math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))

#Haciendo las conexiones de cada punto a todos los demás
def connections(vertices):
    edges=[[] for _ in range(n1)]
    for i in range(n1-1):
        for j in range(i+1, n1):
            distance=euclidean_distance(vertices[i][0],vertices[i][1],vertices[j][0],vertices[j][1])
            edges[i].append((j,distance))
    #print(edges)
    return edges

w=[]
csvtxtCPR(w)
edges=connections(w)

#Algoritmo de MST
def find(t,a):
    if t[a]==a:
        return a
    else:
        grandpa=find(t,t[a])
        t[a]=grandpa
        return grandpa
    
def union(t,a,b):
    pa=find(t,a)
    pb=find(t,b)
    t[pb]=pa
    
def kruskal(G,vertices):
    n=len(G)
    q=[]
    cost=0 #costo total del recorrido
    p=[] #para las coordenadas
    for u in range(n):
        for v,w in G[u]:
            hq.heappush(q,(w,u,v))
            
    Gp=[[] for _ in range(n)]
    uf=[i for i in range(n)]
    
    while len(q)>0:
        w,u,v=hq.heappop(q)
        pu=find(uf,u)
        pv=find(uf,v)
        if pu!=pv:
            cost+=w
            union(uf,u,v)
            p.append((u,v))
            Gp[u].append((v,w))
            
    coordinates_path=[]
    for i,j in p:
        coordinates_path.append((vertices[i][0],vertices[i][1]))
        coordinates_path.append((vertices[j][0],vertices[j][1]))
    return Gp,cost,coordinates_path

#Agregando las coordenadas del camino obtenido
Gp,cost,coordinates_path=kruskal(edges,w)
x = []
y = []
for i in range(n1):
    x.append(coordinates_path[i][0]/100)
    y.append(coordinates_path[i][1]/100)
    
#Cambiar el tamaño del gráfico
fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 20
fig_size[1] = 16

#Graficando las coordenadas, el camino y el costo de viaje
plt.plot(x, y, 'b.')
plt.plot(x, y, 'g.--')
plt.show()
print(coordinates_path)
print(cost)

fig = plt.figure(num=None, figsize=(20, 16) ) 
m = Basemap(width=6000000,height=4500000,resolution='c',projection='aea',lat_1=2.,lat_2=2,lon_0=-75.311132,lat_0=-10.151093)
m.drawcoastlines(linewidth=0.5)
m.fillcontinents(color='tan',lake_color='lightblue')
# draw parallels and meridians.
m.drawparallels(np.arange(-90.,91.,15.),labels=[True,True,False,False],dashes=[2,2])
m.drawmeridians(np.arange(-180.,181.,15.),labels=[False,False,False,True],dashes=[2,2])
m.drawmapboundary(fill_color='lightblue')
m.drawcountries(linewidth=2, linestyle='solid', color='k' ) 
m.drawstates(linewidth=0.5, linestyle='solid', color='k')
m.drawrivers(linewidth=0.5, linestyle='solid', color='blue')

Gp,cost,coordinates_path=kruskal(edges,w)
xc = []
yc = []

for i in range(n1):
    xc.append(coordinates_path[i][0]/100)
    yc.append(coordinates_path[i][1]/100)
x,y=m(xc,yc)

m.plot(x,y,'b.', markersize=15)
m.plot(x,y, 'r--', linewidth=3)

plt.title("Perú")
plt.show()

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))

