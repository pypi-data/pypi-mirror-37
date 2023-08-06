import math
from .ABTest import *

class ZTest(ABTest.TestResults):
    
    def __init__(self, test_group=None, control_group=None, pooled=True):
        """ Class for performing two sample Z test for equality of proportions

        Attributes:
            test_group (TestGroup) TestGroup instance
            control_group (TestGroup) TestGroup instance
            pooled (bool) Calculate pooled (true) or unpooled (false) SE
            z (float) Test statistic
            
        """
        self.test_group = test_group
        self.control_group = control_group
        self.pooled = pooled
        self.__z = None
        self.df = 1
        
        ABTest.TestResults.__init__(self,
                                    delta=self.__calculate_difference(),
                                    test_statistic=self.__calculate_zscore(),
                                    pval=self.__calculate_pval(),
                                    cint_lower=self.__calculate_confidence_lwr(),
                                    cint_upper=self.__calculate_confidence_upr(),
                                    df=self.df)
        
    def __calculate_se(self):
        """ Calculation of standard error for test & control group
        
        You should choose to calculate a pooled version of the standard error
        when your null hypothesis says that the difference between proportions
        is equal to zero.
        
        Args: 
            None
        Returns:
            float: Standard error of test & control group
        """
        p1, n1 = self.test_group.mean, self.test_group.size
        p2, n2 = self.control_group.mean, self.control_group.size
        
        if self.pooled:
            p = (p1*n1 + p2*n2) / (n1 + n2)
            se = math.sqrt(p * (1 - p) * (1/n1 + 1/n2))
        else:
            se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
            
        return se

    def __calculate_difference(self):
        """ Calculation of difference between means between test and control group
        Args: 
            None
        Returns:
            float: Difference of means
        """
        self.difference = abs(self.test_group.mean - self.control_group.mean)
        
        return self.difference
    
    def __calculate_zscore(self):
        """ Calculation of Z score (test statistic)
        Args: 
            None
        Returns:
            float: Z score
        """
        self.difference = self.__calculate_difference()
        se = self.__calculate_se()
        self.__z = self.difference / se
        
        return self.__z
    
    def __calculate_pval(self):
        """ Calculation of P value for two sided test
        Args: 
            None
        Returns:
            float: p value
        """
        self.__z = self.__calculate_zscore()
        
        return ABTest.SpecialFunctions(-self.__z).cdf("abram")

    def __calculate_confidence_lwr(self):
        """ Calculation of lower bound of 95% confidence interval
        Args: 
            None
        Returns:
            float: Lower bound of 95% confidence interval
        """
        z = 1.959963984540054
        cint_lower = max(0, self.difference - z * self.__calculate_se())
        
        return cint_lower
    
    def __calculate_confidence_upr(self):
        """ Calculation of upper bound of 95% confidence interval
        Args: 
            None
        Returns:
            float: Upper bound of 95% confidence interval
        """
        # Z score for 95% confidence interval (based on z((1+.95)/2))
        z = 1.959963984540054
        cint_upper = min(self.difference + z * self.__calculate_se(), 1)
        
        return cint_upper
    
    def __repr__(self):
        summary = "Two sample Z test for equality of proportions (without continuity correction) \n\n" \
                  "Summary: \n----------------------------------- \n" \
                  "Sample means A = {:.4f}, B = {:.4f} \n" \
                  "Sample difference = {:.4f} \n95% confidence interval = ({:.4f}, {:.4f})\n" \
                  "Z = {:.4f} \np = {:.4f} \ndf = {}"
                    
        
        return summary.format(self.test_group.mean, self.control_group.mean, self.difference,
                              self.cint_lower, self.cint_upper, self.test_statistic, self.pval, self.df)