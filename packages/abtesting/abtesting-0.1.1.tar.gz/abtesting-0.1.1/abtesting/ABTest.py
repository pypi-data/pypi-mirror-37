import math

class ABTest():
    
    class TestGroup():
    
        def __init__(self, size=None, mu=None, sigma=None):
            """ Generic class for evaluating A/B tests

            Attributes:
                size (int) Size of the test group
                mean (float) Mean value of test group
                stdev (float) Standard deviation of a test group
            """
            self.size = size
            self.mean = mu
            self.stdev = sigma

        def __repr__(self):
            summary = "A/B test group instance with: \nSize = {} \nMean = {:.4f}"

            return summary.format(self.size, self.mean)
        
    class TestResults():
    
        def __init__(self, delta=None, test_statistic=None,
                     pval=None, cint_lower=None, cint_upper=None, df=None):
            """ Generic class for A/B test results

            Attributes:
                difference (float) Difference of means between test and control group
                test_statistic (float) Test statistic (e.g. Z score)
                pval (float) P value of test
                cint_lower (float) Lower bound of confidence interval around difference of means
                cint_upper (float) Upper bound of confidence interval around difference of means
            """
            self.difference = delta
            self.test_statistic = test_statistic
            self.pval = pval
            self.cint_lower = cint_lower
            self.cint_upper = cint_upper
            self.df = df
            
    class SpecialFunctions():

        def __init__(self, x):
            self.x = x

        def erf_abram(self, x):
            """ Approximation of the error function (non-elementary).

            The numerical approximation of error function as shown in
            Abramowitz and Stegun (1964). It has a maximum error of 1.5×10e−7.

            Please note the approximation is only valid for x >= 0. For negative
            x values one can use the fact that erf(x) is an odd function, so:

                erf(-x) = -erf(x)

            The error function, also called Gauss error function, is a special
            function. For more details please see: https://en.wikipedia.org/wiki/Error_function

            Args:
                x (float): Z Score
            Returns:
                float: Approximated value of the error function for given x
            """
            # Sign of x
            sign = 1. if x >= 0 else -1.
            z = abs(x)

            # Constant parameters
            p = 0.3275911
            a1 = 0.254829592
            a2 = -0.284496736
            a3 = 1.421413741
            a4 = -1.453152027
            a5 = 1.061405429

            # Approximation
            t = 1. / (1. + p * z)
            erfx = 1. - t * (a1 + t * (a2 + t * (a3 + t * (a4 + t * a5)))) * math.exp(-z*z)

            return sign * erfx

        def erf_fort(self):
            """ Approximation of the error function (non-elementary).

            The numerical approximation of error function as shown in
            Press et al. (1992). It has a maximum error of 1.2×10e−7.

            Please note the approximation is only valid for x >= 0. For negative
            x values one can use the fact that erf(x) is an odd function, so:

                erf(-x) = -erf(x)

            The error function, also called Gauss error function, is a special
            function. For more details please see:
            - https://de.wikipedia.org/wiki/Fehlerfunktion#cite_note-2
            - https://websites.pmc.ucsc.edu/~fnimmo/eart290c_17/NumericalRecipesinF77.pdf
            - https://introcs.cs.princeton.edu/java/21function/ErrorFunction.java.html

            Args:
                x (float): Z Score
            Returns:
                float: Approximated value of the error function for given x
            """
            # Sign of x
            sign = 1. if x >= 0 else -1.
            z = abs(x)

            # Approximation
            t = 1. / (1. + p * z)    
            erfx = 1. - t * math.exp(-z*z -1.26551223 +
                                     t * ( 1.00002368 +
                                     t * ( 0.37409196 + 
                                     t * ( 0.09678418 + 
                                     t * (-0.18628806 + 
                                     t * ( 0.27886807 + 
                                     t * (-1.13520398 + 
                                     t * ( 1.48851587 + 
                                     t * (-0.82215223 + 
                                     t * ( 0.17087277))))))))))

            return sign * erfx

        def cdf(self, erf="abram"):
            """ Approximation of the CDF of the standard normal distribution

            The numerical approximation of the cumulative distribution function
            of the standard normal distribution (mean = 0, stdev = 1) of a real
            valued variable X based on its close relation to the error function.

            For more details please see:
            https://en.wikipedia.org/wiki/Normal_distribution#Cumulative_distribution_function

            Args:
                x (float): Z Score
                erf (string, optional): Approximation of error function (abram, fort)
            Returns:
                float: Probability that X will take a value less than or equal to x
            """
            if erf == "fort":
                return 0.5 + 0.5 * self.erf_fort(self.x / math.sqrt(2.))
            else:
                return 0.5 + 0.5 * self.erf_abram(self.x / math.sqrt(2.))