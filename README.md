# Pandas-Ocean-Dat
Pandas library to illustrate the effectiveness of Pandas on time series oceanographic data.  This module will import oceanographic data such as wind and wave data, store the data into a pandas dataframe, and perform extremal analysis and plot the output using Pandas capability with matplotlib.


```python
import oceanData
od1=oceanData.oceanDataPlot()
od1.intersectDates()
od1.plotDates()
od1.fig.show()
```


![alt text for plot](https://github.com/derekawilson72/Pandas-Ocean-Dat/blob/master/new.png?raw=true "Ocean Data Plot")
