import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
from pylab import rcParams

##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 11 Oct 2018
# Function: batsman4s
# This function plots the number of 4s vs the runs scored in the innings by the batsman
#

###########################################################################################
def batsman4s(file, name="A Hookshot"):
    '''
    Plot the numbers of 4s against the runs scored by batsman
    
    Description
    
    This function plots the number of 4s against the total runs scored by batsman. A 2nd order polynomial regression curve is also plotted. The predicted number of 4s for 50 runs and 100 runs scored is also plotted
    
    Usage
    
    batsman4s(file, name="A Hookshot")
    Arguments
    
    file	
    This is the <batsman>.csv file obtained with an initial getPlayerData()
    name	
    Name of the batsman
    
    Note

    Maintainer: Tinniam V Ganesh <tvganesh.85@gmail.com>
    
    Author(s)
    
    Tinniam V Ganesh
    
    References
    
    http://www.espncricinfo.com/ci/content/stats/index.html
    https://gigadom.wordpress.com/
    
    See Also
    
    batsman6s
    
    Examples
    
    # Get or use the <batsman>.csv obtained with getPlayerData()
    tendulkar  = getPlayerData(35320,dir="../",file="tendulkar.csv",type="batting")
    homeOrAway=[1,2],result=[1,2,4]
    
    '''   
    # Clean the batsman file and create a complete data frame
    df = clean(file)
    
    # Set figure size
    rcParams['figure.figsize'] = 10,6
    
    # Get numnber of 4s and runs scored
    x4s = pd.to_numeric(df['4s'])
    runs = pd.to_numeric(df['Runs'])
     
    atitle = name + "-" + "Runs scored vs No of 4s" 
    
    # Plot no of 4s and a 2nd order curve fit   
    plt.scatter(runs, x4s, alpha=0.5)
    plt.xlabel('Runs')
    plt.ylabel('4s')
    plt.title(atitle)
    
    # Create a polynomial of degree 2
    poly = PolynomialFeatures(degree=2)
    runsPoly = poly.fit_transform(runs.reshape(-1,1))
    linreg = LinearRegression().fit(runsPoly,x4s)
    
    plt.plot(runs,linreg.predict(runsPoly),'-r')
    
    # Predict the number of 4s for 50 runs
    b=poly.fit_transform((np.array(50)))
    c=linreg.predict(b)
    plt.axhline(y=c, color='b', linestyle=':')
    plt.axvline(x=50, color='b', linestyle=':')
    
    
    # Predict the number of 4s for 100 runs
    b=poly.fit_transform((np.array(100)))
    c=linreg.predict(b)
    plt.axhline(y=c, color='b', linestyle=':')
    plt.axvline(x=100, color='b', linestyle=':')
    
    plt.text(180, 0.5,'Data source-Courtesy:ESPN Cricinfo',
         horizontalalignment='center',
         verticalalignment='center',
         )
    plt.show()
    return

   
import matplotlib.pyplot as plt
import seaborn as sns
from pylab import rcParams
##########################################################################################
# Designed and developed by Tinniam V Ganesh
# Date : 13 Oct 2018
# Function: batsman6s
# This function plots the number of 6s vs the runs scored in the innings by the batsman
#
###########################################################################################

def batsman6s(file, name="A Hookshot") :
    '''
    Description

    Compute and plot the number of 6s in the total runs scored by batsman
    
    Usage
    
    batsman6s(file, name="A Hookshot")
    Arguments
    
    file	
    This is the <batsman>.csv file obtained with an initial getPlayerData()
    name	
    Name of the batsman
    
    Examples
    # Get or use the <batsman>.csv obtained with getPlayerData()
    # tendulkar = getPlayerData(35320,file="tendulkar.csv",type="batting", homeOrAway=c(1,2),result=c(1,2,4))


    '''
    x6s = []
    
    # Set figure size
    rcParams['figure.figsize'] = 10,6
    
    # Clean the batsman file and create a complete data frame
    df = clean (file)  
    
    # Remove all rows where 6s are 0
    a= df['6s'] !=0
    b= df[a]
    
    x6s=b['6s'].astype(int)
    runs=pd.to_numeric(b['Runs'])
    
    # Plot the 6s as a boxplot
    atitle =name + "-" + "Runs scored vs No of 6s" 
    df1=pd.concat([runs,x6s],axis=1)
    fig = sns.boxplot(x="6s", y="Runs", data=df1)
    plt.title(atitle)
    plt.text(2.2, 10,'Data source-Courtesy:ESPN Cricinfo',
         horizontalalignment='center',
         verticalalignment='center',
         )
    
