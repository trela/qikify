from __future__ import division
from scipy import c_, ones, dot, stats, diff
import scipy.linalg
from numpy import log, pi, sqrt, square, diagonal

class OLS(object):
    """
    Ordinary least squares multivariate regression.
    """

    def __init__(self):
        """
        Initializing the ols class. 
        """
        pass
        
    def train(self,X,y,useQR = True, addConstant = True):    
        '''
        Solve y = Xb.
        
        Parameters:
        x : array, shape (M, N)
        y : array, shape (M,)
        useQR : boolean
            Whether or not to use QR decomposition to fit regression line.
        addConstant: boolean
            Whether or not to add a constant column to X
        '''        
        if y.shape[0] != X.shape[0]:
            raise ValueError('incompatible dimensions')
        if addConstant:
            self.X       = c_[ones(X.shape[0]), X]

        self.y       = y
        self.X_columns = getattr(X,'columns', None)
        self.y_columns = getattr(y,'columns', None)
        
        if useQR:
            # TODO: Ehh, this is broken. Need to fix.
            Q,R = scipy.linalg.qr(self.X)
            Qty = dot(Q.T, y)
            self.b = scipy.linalg.solve(R,Qty)
        else:
            self.inv_xx = inv(dot(self.X.T,self.X))
            xy = dot(self.X.T,self.y)
            self.b = dot(self.inv_xx,xy)

        self.computeStatistics()
        
        
    def computeStatistics(self):        
        self.nobs  = self.y.shape[0]                     # number of observations
        self.ncoef = self.X.shape[1]                    # number of coef.
        self.df_e  = self.nobs - self.ncoef              # degrees of freedom, error 
        self.df_r  = self.ncoef - 1                      # degrees of freedom, regression 

        self.e = self.y - dot(self.X,self.b)            # residuals
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
        for i in range(len(self.X_columns)):
            output += '% -5s          % -5.6f     % -5.6f     % -5.6f     % -5.6f\n' % (self.X_columns[i],self.b[i+1],self.se[i+1],self.t[i+1],self.p[i+1]) 
        return output
        