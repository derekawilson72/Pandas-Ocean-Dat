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

    rosePlotFig=None


    
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
        self.exRng1=((commonData['Wvht']>2) & (commonData['Wspd']>4))  ##determine intersecting extreme range

    def plotDates(self):
        """
        plotDates()

        plotting datasets of wind and wave data as well as the extreme
        events.  Uses Pandas inherent time series plotting tools.
        
        Parameters
        ----------
        None. Uses class variables

        Returns
        -------
        out : fig
        A matplotlib figure object of the timeseries plot

        Examples
        --------
        >>> self.plotDates()
        matplotlib fig

        """
        ##determine common date range between two datasets
        idx1 = pd.Index(self.rng1)
        idx2 = pd.Index(self.rng2)
        cdx=idx1.intersection(idx2) #set to intersection
        ##set two DataFrames to commonData
        commonData=self.WaveData.loc[cdx]
        commonData[self.WindData.columns]=self.WindData.loc[cdx]
        self.intersectDates() ##determine date intersection and analyze extremes.
        exRng1=self.exRng1    ##get the extreme wind and wave data
        
        fig = plt.figure(figsize=(12,4))

        ax1 = fig.add_subplot(211)
        l1=commonData['Wvht'].plot(ax=ax1,title='WaveHeight' )  ##create timeseries of wave data
        ax1.set_ylabel('WvHt [m]')

        ax2 = fig.add_subplot(212)
        l2=commonData['Wspd'].plot(ax=ax2,title='WindSpeed',color='green')
        l2.lines[0].set_color('green') ##change color anytime
        ax2.set_ylabel('Wspd [m/s]')
        ax2.set_xlabel('date')
        fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.15)

        redWave=Line2D(commonData[exRng1].index , commonData[exRng1]['Wvht'] , linestyle='', color='r', marker='o', markersize=5, fillstyle='full')  ##times series points of the extreme wave heights
        ax1.add_line(redWave)

        redWind=Line2D(commonData[exRng1].index , commonData[exRng1]['Wspd'] , linestyle='',  color='r', marker='o', markersize=5, fillstyle='full') ##times series points of the extreme wind speeds
        ax2.add_line(redWind)

        self.fig=fig
        self.axs=[ax1,ax2]
        
        fig.canvas.draw()
        fig.savefig('timeseries.png')


    def createWaveRose(self):
        """
        create a rose plot with the WaveData parameter in both magnitude and direction
        """
        magn=self.WaveData.Wvht
        dirs=self.WaveData.Wvdr
        fig=self.rosePlot(magn, dirs)
        fig.savefig('WaveRose.png')
        

    def createWindRose(self):
        """
        create a rose plot with the WindData parameter in both magnitude and direction
        """
        
        magn=self.WindData.Wspd
        dirs=self.WindData.Wndr
        fig=self.rosePlot(magn, dirs)
        fig.savefig('WindRose.png')
        
    def rosePlot(self,magn=None, dirs=None):
        """
        rosePlot(magn, dirs)
        
        generate a rose plot with the class values for WaveData or Winddata. A rose plot will display the magnitude and direction of both wind and waves.  The rose plots will appear as wedges in the direction of the wave or wind.  The magnitude of the wave or wind will appear as the diameter of the wedge and a cumulative distribution function will appear as color codes of the wedge.  
        
        Parameters
        ----------
        magn:  array-like 
        magnitude of wind or waves
        dirs:  array-like
        direction of wind or waves

        Returns
        -------
        out : fig
        A matplotlib figure object of the roseplot

        Examples
        --------
        >>> self.rosePlot(self.WaveData.Wvht, self.WaveData.Wvdr)
        matplotlib fig

        >>> self.rosePlot(self.WindData.Wnsp, self.WaveData.Wndr)
        matplotlib fig

        >>> self.rosePlot()  ##return random dataset for testing
        matplotlib fig

        """

        N=16
        ##load default random data if none provided
        if magn is None:
            magn=np.random.rand(100)*np.random.randint(1,100)
        if dirs is None:
            dirs=np.random.randint(0,360,size=(len(magn),1))
        
        
        theta= np.linspace(0.0, 2*np.pi, N , endpoint=False)-np.pi/16.0  #divide circle into 16(N) sectors.
        width= 2*np.pi / N  #np.pi /4.0 * np.random.rand(N)
        bins=[1.0, 0.75, 0.5, 0.25] ##bin the radii
        colors=['red', 'orange', 'yellow', 'green']##color codes for the radii with red the highest
        theta_i=0.0

        fig=plt.figure()

        ##set the second axis as a colorbar of the bins 
        ax2=plt.subplot(122)
        ax2.bar([0,0,0,0],[0.25,0.25,0.25,0.25],
                width=.8, bottom=[0, 0.25,0.5,0.75],
                color=colors[-1::-1]
)
        ax2.set_yticks([0, 0.25,0.5, 0.75, 1.0])
        ax2.set_yticklabels(["0%", "25%","50%", "75%","100%"])
        ax2.set_xticks([])
        ax2.set_xlim([0, 0.8])
        ax2.set_position([.85, .1, .075,.6])#set position and size of axis in left, bottom, width, height 

        ##set the first axis as the polar plot or the rose plot
        ax=plt.subplot(121, projection='polar')
        bars=[]
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)
        d_theta=360.0/N
        for theta_i in theta:
            theta_d=theta_i*180/np.pi
            if theta_d<0:
                idxs=(dirs>=(360+theta_d)) | (dirs<(theta_d+d_theta))
            else:
                idxs=(dirs>=(theta_d)) & (dirs<(theta_d+d_theta))
            wvs0=magn[idxs].values
            #wvs0=np.random.rand(100)*np.random.randint(1,100)
            wvs0.sort()
            
            if len(wvs0)>0:
                inds=np.linspace(0,1.0, len(wvs0))
                wv_bdys=np.interp(bins, inds, wvs0, left=None, right=None)
            else:
                wv_bdys=np.zeros(len(bins))
            bars_0=ax.bar(theta_i*np.ones(len(bins)), wv_bdys,
                          width=width, color=colors, bottom=0.0)
            bars.append(bars_0)
        ax.set_position([.05, .1, .65,.80])#set position and size of axis in left, bottom, width, height 
        self.rosePlotFig=fig
        return fig


if __name__=='__main__':
    odp1=oceanDataPlot()
    odp1.intersectDates()
    odp1.plotDates()
    odp1.fig.show()

    odp1.createWaveRose()
    odp1.createWindRose()

    wd1=pd.read_csv('data/windate.csv')


    wd1=wd1.set_index('date')
    wd1['Wndr']=wd1['WD']
    wd1['Wspd']=wd1['WSPD']
    odp1.WindData =   wd1[['Wndr','Wspd']]

    odp1.createWindRose()
    odp1.rosePlotFig.show()

