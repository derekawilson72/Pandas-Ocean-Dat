import pandas as pd
import datetime
import numpy as  np
from matplotlib import pyplot as plt



rng  = pd.date_range('1/1/2011', periods=72, freq='H')
rng1 = pd.date_range(start='1/1/2011', end='1/10/2011', freq='360S')
rng2 = pd.date_range(start='1/2/2011', end='1/08/2011', freq='360S')

WaveData=pd.DataFrame(rng1,columns=['date'])
WaveData['Wvht']=np.random.randn(len(WaveData), 1)*10
WaveData['Wvdr']=np.random.randint(0,360,size=(len(WaveData),1))
WaveData=WaveData.set_index('date')

WindData=pd.DataFrame(rng2,columns=['date'])
WindData['Wspd']=np.random.rand(len(WindData), 1)*5
WindData['Wndr']=np.random.randint(0,360,size=(len(WindData),1))
WindData=WindData.set_index('date')



##determine common date range
idx1 = pd.Index(rng1)
idx2 = pd.Index(rng2)
cdx=idx1.intersection(idx2)  #set to intersection


##set two DataFrames to commonData
commonData=WaveData.loc[cdx]
commonData[WindData.columns]=WindData.loc[cdx]



##extreme wind and wave Data
commonData[commonData['Wvht']>2]  ##wave height above 2m
commonData[commonData['Wspd']>4]  ##wave height above 4m/s





fig = plt.figure(figsize=(12,4))
ax = fig.add_subplot(211)
l1=commonData['Wvht'].plot(ax=ax,title='WaveHeight' )
ax.set_ylabel('WvHt [m]')
ax.set_xlabel('date')

ax = fig.add_subplot(212)
l2=commonData['Wspd'].plot(ax=ax,title='WindSpeed',color='green')
##change color anytime
l2.lines[0].set_color('green')

ax.set_ylabel('WvHt [m]')
ax.set_xlabel('date')

fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.15)
fig.canvas.draw()
fig.savefig('new.png')
ax.set_xlabel('date')
