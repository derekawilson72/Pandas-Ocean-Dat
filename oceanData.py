import pandas as pd
import datetime
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.pyplot import  Line2D 

class oceanDataPlot():
    """
    merge two datasets with intersecting (overlapping) date ranges.
    Plot the data as a single dataset and export as a netcdf.
    """
    
    fig=None
    axs=None

    WaveData=None
    WindData=None
    rng1=None
    rng2=None
    exRng1=None

    def __init__(self):

        self.setSampleData()


    def setSampleData(self):
        """set two arbitrary date ranges with overlapping dates"""

        rng1 = pd.date_range(start='1/1/2011', end='1/10/2011', freq='360S')
        rng2 = pd.date_range(start='1/2/2011', end='1/08/2011', freq='360S')

        WaveData=pd.DataFrame(rng1,columns=['date'])  ##initialize wave dataset
        WaveData['Wvht']=np.random.randn(len(WaveData), 1)*10  ##append values for column data
        WaveData['Wvdr']=np.random.randint(0,360,size=(len(WaveData),1))
        WaveData=WaveData.set_index('date')
        self.rng1=rng1
        self.WaveData=WaveData
        
        WindData=pd.DataFrame(rng2,columns=['date'])  ##do the same for wind data 
        WindData['Wspd']=np.random.rand(len(WindData), 1)*5
        WindData['Wndr']=np.random.randint(0,360,size=(len(WindData),1))
        WindData=WindData.set_index('date')
        self.rng2=rng2
        self.WindData=WindData
        

    def intersectDates(self):
        """
        determine common date range between two datasets
        """

        idx1 = pd.Index(self.rng1)
        idx2 = pd.Index(self.rng2)
        cdx=idx1.intersection(idx2) #set to intersection
        ##set two DataFrames to commonData
        commonData=self.WaveData.loc[cdx]
        commonData[self.WindData.columns]=self.WindData.loc[cdx]

        #extreme wind and wave Data
        #commonData[commonData['Wvht']>2] ##wave height above 2m
        #commonData[commonData['Wspd']>4] ##wave height above 4m/s

        self.exRng1=((commonData['Wvht']>2) & (commonData['Wspd']>4))  ##determine intersecting extreme range

    def plotDates(self):
        """
        plotting datasets of wind and wave data as well as the extreme events
        """

        
        
        ##determine common date range between two datasets
        idx1 = pd.Index(self.rng1)
        idx2 = pd.Index(self.rng2)
        cdx=idx1.intersection(idx2) #set to intersection
        ##set two DataFrames to commonData
        commonData=self.WaveData.loc[cdx]
        commonData[self.WindData.columns]=self.WindData.loc[cdx]

        #extreme wind and wave Data
        #commonData[commonData['Wvht']>2] ##wave height above 2m
        #commonData[commonData['Wspd']>4] ##wave height above 4m/s

        exRng1=self.exRng1
        
        
        fig = plt.figure(figsize=(12,4))
        ax1 = fig.add_subplot(211)
        
        l1=commonData['Wvht'].plot(ax=ax1,title='WaveHeight' )  ##create timeseries of wave data
        ax1.set_ylabel('WvHt [m]')


        ax2 = fig.add_subplot(212)
        l2=commonData['Wspd'].plot(ax=ax2,title='WindSpeed',color='green')
        ##change color anytime
        l2.lines[0].set_color('green')
        ax2.set_ylabel('Wspd [m/s]')
        ax2.set_xlabel('date')
        fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.15)

        redWave=Line2D(commonData[exRng1].index , commonData[exRng1]['Wvht'] , linestyle='',
                       color='r', marker='o', markersize=5, fillstyle='full')
        ax1.add_line(redWave)

        redWind=Line2D(commonData[exRng1].index , commonData[exRng1]['Wspd'] , linestyle='',
                       color='r', marker='o', markersize=5, fillstyle='full')
        ax2.add_line(redWind)

        self.fig=fig
        self.axs=[ax1,ax2]
        
        fig.canvas.draw()
        fig.savefig('new.png')

if __name__=='__main__':
    od1=oceanDataPlot()
    od1.intersectDates()
    od1.plotDates()
    od1.fig.show()
