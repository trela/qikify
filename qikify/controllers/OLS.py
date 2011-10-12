from __future__ import division
from scipy import c_, ones, dot, stats, diff
from scipy.linalg import inv, solve, det, qr
from numpy import log, pi, sqrt, square, diagonal

class OLS:
    """
    ###
    ### Modified! Removed extraneous code, refactored to handle DataStruct-style inputs.
    ### 
    
    Author: Vincent Nijs (+ ?)
    Email: v-nijs at kellogg.northwestern.edu
    Dependencies: See import statement at the top of this file
    Doc: Class for multi-variate regression using OLS

    For usage examples of other class methods see the class tests at the bottom of this file. To see the class in action
    simply run this file using 'python ols.py'. This will generate some simulated data and run various analyses.
    
    Input:
        y = dependent variable
        x = independent variables, note that a constant is added by default
        
    Output:
        There are no values returned by the class. Summary provides printed output.
        All other measures can be accessed as follows:

        Step 1: Create an OLS instance by passing data to the class

            m = ols(y,x,y_varnm = 'y',x_varnm = ['x1','x2','x3','x4'])

        Step 2: Get specific metrics

            To print the coefficients: 
                >>> print m.b
            To print the coefficients p-values: 
                >>> print m.p
    
    """

    def __init__(self):
        """
        Initializing the ols class. 
        """
        pass
        
    def train(self,x,y):    
        '''
        Uses QR decomposition to solve XB = Y.
        '''
        self.x       = c_[ones(x.nrow), x.data]
        self.y       = y.data[:,0]
        self.x_varnm = x.names
        self.y_varnm = y.names
        
        Q,R = linalg.qr(self.x)
        Qty = dot(Q.T, y.data[:,0])
        self.b = linalg.solve(R,Qty)
        
        self.inv_xx = inv(dot(self.x.T,self.x))
        xy = dot(self.x.T,self.y)
        
        self.computeStatistics()
        
    def run(self,x,y): 
        '''
        NOTE: this just solves traditional least squares! susceptible to singular matrix issues.
        '''
        # Standardize X matrix
        #self.scaleFactors = dotdict({'mean': x.data.mean(axis = 0), 'std': x.data.std(axis = 0)})
        #self.x            = c_[ones(x.nrow),scale(x.data, self.scaleFactors)]
        self.x       = c_[ones(x.nrow), x.data]
        self.y       = y.data[:,0]
        self.x_varnm = x.names
        self.y_varnm = y.names
        
        # estimating coefficients, and basic stats
        self.inv_xx = inv(dot(self.x.T,self.x))
        xy = dot(self.x.T,self.y)
        self.b = dot(self.inv_xx,xy)                    # estimate coefficients
        
        self.computeStatistics()
        
    def computeStatistics(self):        
        self.nobs = self.y.shape[0]                     # number of observations
        self.ncoef = self.x.shape[1]                    # number of coef.
        self.df_e = self.nobs - self.ncoef              # degrees of freedom, error 
        self.df_r = self.ncoef - 1                      # degrees of freedom, regression 

        self.e = self.y - dot(self.x,self.b)            # residuals
        self.sse = dot(self.e,self.e)/self.df_e         # SSE
        self.se = sqrt(diagonal(self.sse*self.inv_xx))  # coef. standard errors
        self.t = self.b / self.se                       # coef. t-statistics
        self.p = (1-stats.t.cdf(abs(self.t), self.df_e)) * 2    # coef. p-values

        self.R2 = 1 - self.e.var()/self.y.var()         # model R-squared
        self.R2adj = 1-(1-self.R2)*((self.nobs-1)/(self.nobs-self.ncoef))   # adjusted R-square

        self.F = (self.R2/self.df_r) / ((1-self.R2)/self.df_e)  # model F-statistic
        self.Fpv = 1-stats.f.cdf(self.F, self.df_r, self.df_e)  # F-statistic p-value


    def dw(self):
        """
        Calculates the Durbin-Waston statistic
        """
        de = diff(self.e,1)
        dw = dot(de,de) / dot(self.e,self.e)

        return dw

    def omni(self):
        """
        Omnibus test for normality
        """
        return stats.normaltest(self.e) 
    
    def JB(self):
        """
        Calculate residual skewness, kurtosis, and do the JB test for normality
        """

        # Calculate residual skewness and kurtosis
        skew = stats.skew(self.e) 
        kurtosis = 3 + stats.kurtosis(self.e) 
        
        # Calculate the Jarque-Bera test for normality
        JB = (self.nobs/6) * (square(skew) + (1/4)*square(kurtosis-3))
        JBpv = 1-stats.chi2.cdf(JB,2);

        return JB, JBpv, skew, kurtosis

    def ll(self):
        """
        Calculate model log-likelihood and two information criteria
        """
        
        # Model log-likelihood, AIC, and BIC criterion values 
        ll = -(self.nobs*1/2)*(1+log(2*pi)) - (self.nobs/2)*log(dot(self.e,self.e)/self.nobs)
        aic = -2*ll/self.nobs + (2*self.ncoef/self.nobs)
        bic = -2*ll/self.nobs + (self.ncoef*log(self.nobs))/self.nobs

        return ll, aic, bic
    
    def __str__(self):
        # extra stats
        ll, aic, bic = self.ll()
        JB, JBpv, skew, kurtosis = self.JB()
        omni, omnipv = self.omni()

        output = GREEN + \
               '==============================================================================\n'                           + \
               'OLS Fit                                                                       \n'                           + \
               'Dependent Variable: ' + self.y_varnm  + '\nN: %5.0f \np: %5.0f                \n' % (self.nobs, self.ncoef) + \
               'Models stats                         Residual stats                           \n'                           + \
               '==============================================================================\n' + ENDCOLOR                + \
               'R-squared            % -5.6f         Durbin-Watson stat  % -5.6f              \n' % (self.R2, self.dw())    + \
               'Adjusted R-squared   % -5.6f         Omnibus stat        % -5.6f              \n' % (self.R2adj, omni)      + \
               'F-statistic          % -5.3f         Prob(Omnibus stat)  % -5.6f              \n' % (self.F, omnipv)        + \
               'Prob (F-statistic)   % -5.6f		 JB stat             % -5.6f              \n' % (self.Fpv, JB)          + \
               'Log likelihood       % -5.3f		 Prob(JB)            % -5.6f              \n' % (ll, JBpv)              + \
               'AIC criterion        % -5.6f         Skew                % -5.6f              \n' % (aic, skew)             + \
               'BIC criterion        % -5.6f         Kurtosis            % -5.6f              \n' % (bic, kurtosis)+GREEN   + \
               '==============================================================================\n' + \
               'variable            coefficient     std. Error      t-statistic     prob      \n' + \
               '==============================================================================\n' + ENDCOLOR
        output += 'Intercept\t          % -5.6f     % -5.6f     % -5.6f     % -5.6f\n' % (self.b[0],self.se[0],self.t[0],self.p[0]) 
        for i in range(len(self.x_varnm)):
            output += '% -5s          % -5.6f     % -5.6f     % -5.6f     % -5.6f\n' % (self.x_varnm[i],self.b[i+1],self.se[i+1],self.t[i+1],self.p[i+1]) 
        return output
        