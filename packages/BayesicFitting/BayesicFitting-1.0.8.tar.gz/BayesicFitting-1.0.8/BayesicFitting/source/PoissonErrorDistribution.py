import numpy as numpy
import math

from .ErrorDistribution import ErrorDistribution
from .LogFactorial import logFactorial

__author__ = "Do Kester"
__year__ = 2017
__license__ = "GPL3"
__version__ = "0.9"
__maintainer__ = "Do"
__status__ = "Development"

#  *
#  * This file is part of the BayesicFitting package.
#  *
#  * BayesicFitting is free software: you can redistribute it and/or modify
#  * it under the terms of the GNU Lesser General Public License as
#  * published by the Free Software Foundation, either version 3 of
#  * the License, or ( at your option ) any later version.
#  *
#  * BayesicFitting is distributed in the hope that it will be useful,
#  * but WITHOUT ANY WARRANTY; without even the implied warranty of
#  * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  * GNU Lesser General Public License for more details.
#  *
#  * The GPL3 license can be found at <http://www.gnu.org/licenses/>.
#  *
#  * A JAVA version of this code was part of the Herschel Common
#  * Science System (HCSS), also under GPL3.
#  *
#  *    2010 - 2014 Do Kester, SRON (Java code)
#  *    2017        Do Kester


class PoissonErrorDistribution( ErrorDistribution ):
    """
    To calculate a Poisson likelihood.

    For one observation with n counts it holds
    ..math ::
        f( n,x ) = x^n / ( e^x * n! )

    where x is the expected counts

    The function is mostly used to calculate the likelihood L, or easier
    to use log likelihood, logL.
    .. math::
        logL = \sum( n * \log( x ) - x - \log( n! ) )

    Author       Do Kester.

    """

    PARNAMES = []

    #  *********CONSTRUCTORS***************************************************
    def __init__( self, xdata, data, weights=None, copy=None ):
        """
        Constructor.

        Parameters
        ----------
        xdata : array_like
            input data for the model
        data : array_like
            data to be fitted
        weights : array_like
            weights to be used (no weights are possible in Poisson)
        copy : PoissonErrorDistribution
            distribution to be copied.

        Raises
        ------
        ValueError when weights is not None

        """
        if weights is not None:
            raise ValueError( "Weights are not possible in Poisson distributions" )

        super( PoissonErrorDistribution, self ).__init__( xdata, data, copy=copy )

    def copy( self ):
        """ Return copy of this.  """
        return PoissonErrorDistribution( self.xdata, self.data, copy=self )

    def acceptWeight( self ):
        """
        True if the distribution accepts weights.
        Always false for this distribution.
        """
        return False

    def getChisq( self, residuals, scale ) :
        """
        Return chisq as Gaussian approximation
        .. math::
            \chi^2 = \sum( residuals^2 / data )

        Parameters
        ----------
        residuals : array-like
            difference between data and model
        scale : float
            scale factor. Not used.
        """
        return numpy.sum( numpy.square( residuals ) / self.data )

    def getScale( self, model ) :
        """
        Return the sqrt( chisq / npt )
        Gaussian approximation.

        """
        chi = self.getChisq( self.getResiduals( model ), 0.0 )
        return math.sqrt( chi / self.sumweight )


    #  *********LIKELIHOODS***************************************************
    def logLikelihoodXXX( self, model, param ):
        """
        Return the log( likelihood ) for a Poisson distribution.

        Parameters
        ----------
        model : Model
            model to calculate mock data
        param : array_like
            parameters of the model

        """
        self.ncalls += 1
        mock = model.result( self.xdata, param )
        if numpy.any( numpy.less_equal( mock, 0 ) ) :
            return -math.inf

        lfdata = logFactorial( self.data )

        logl = numpy.sum( self.data * numpy.log( mock ) - mock - lfdata )

        if math.isnan( logl ) :
            return -math.inf

        return logl

    def logLdata( self, model, param, mockdata=None ) :
        """
        Return the log( likelihood ) for each residual

        logL = sum( logLdata )

        Parameters
        ----------
        model : Model
            to be fitted
        param : array_like
            list of all parameters in the problem
        mockdata : array_like
            as calculated by the model

        """
        if mockdata is None :
            mockdata = model.result( self.xdata, param )
        lfdata = logFactorial( self.data )

        lld = self.data * numpy.log( mockdata ) - mockdata - lfdata
        lld = numpy.where( numpy.isfinite( lld ), lld, -math.inf )

        return lld

    def partialLogLXXX( self, model, param, fitIndex ):
        """
        Return the partial derivative of log( likelihood ) to the parameters.

        Parameters
        ----------
        model : Model
            model to calculate mock data
        param : array_like
            parameters of the model
        fitIndex : array_like
            indices of the params to be fitted
        """
        self.nparts += 1
        mock = model.result( self.xdata, param )
        dM = model.partial( self.xdata, param )
        dL = numpy.zeros( len( fitIndex ), dtype=float )

        i = 0
        for k in fitIndex :
            dL[i] = numpy.sum( ( self.data / mock - 1 ) * dM[:,k] )
            i += 1

        return dL

    def nextPartialData( self, model, param, fitIndex, mockdata=None ):
        """
        Return the partial derivative of log( likelihood ) to the parameters.

        Parameters
        ----------
        model : Model
            model to calculate mock data
        param : array_like
            parameters of the model
        fitIndex : array_like
            indices of the params to be fitted
        mockdata : array_like
            as calculated by the model
        """
        if mockdata is None :
            mockdata = model.result( self.xdata, param )
        dM = model.partial( self.xdata, param )
##      TBD import mockdata into partial
#        dM = model.partial( self.xdata, param, mockdata=mockdata )

        for k in fitIndex :
            yield ( self.data / mockdata - 1 ) * dM[:,k]

        return

    def __str__( self ) :
        return "Poisson error distribution"

