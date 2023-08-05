import numpy as numpy
from astropy import units
import math
from . import Tools
from .Formatter import formatter as fmt
from .Formatter import fma

from .Engine import Engine
from .Engine import DummyPlotter

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
#  *    2003 - 2014 Do Kester, SRON (Java code)
#  *    2017        Do Kester

class GalileanEngine( Engine ):
    """
    Move all parameters in forward steps, with optional mirroring on the edge.

    Move the parameters in a random direction for N iterations; mirror the direction
    on the gradient of the logLikelihood when the parameters enter the zone of logLlow.

    Attributes
    ----------
    walkers : SampleList
        walkers to be diffused
    errdis : ErrorDistribution
        error distribution to be used
    nstep : int (10)
        average number of steps to be taken
    size : float (0.5)
        average normalized stepsize
    maxtrials : int
        maximum number of trials for various operations
    rng : numpy.random.RandomState
        random number generator


    Author       Do Kester.

    """

    #  *********CONSTRUCTORS***************************************************
    def __init__( self, walkers, errdis, copy=None, seed=4213 ):
        """
        Default Constructor.

        Parameters
        ----------
        walkers : SampleList
            walkers to be diffused
        errdis : ErrorDistribution
            error distribution to be used
        copy : GalileanEngine
            to be copied
        seed : int
            for random number generator
        """
        super( GalileanEngine, self ).__init__( walkers, errdis, copy=copy,
                        seed=seed  )
        self.nstep = 4
#        self.size = 0.5

        self.plotter = DummyPlotter( )

    def copy( self ):
        """ Return copy of this.  """
        engine = GalileanEngine( self.walkers, self.errdis, copy=self )
        engine.nstep = self.nstep
#        engine.size = self.size
        return engine

    def __str__( self ):
        """ Return the name of this engine.  """
        return str( "GalileanEngine" )

    #  *********EXECUTE***************************************************
    def execute( self, walker, lowLhood, fitIndex=None ):
        """
        Execute the engine by diffusing the parameters.

        Parameters
        ----------
        walker : Sample
            walker to diffuse
        lowLhood : float
            lower limit in logLikelihood
        fitIndex : array_like
            list of the/some parameters indices to be diffused

        Returns
        -------
        int : the number of successfull moves

        """
        model = walker.model
        Lhood = walker.logL
        allpars = walker.allpars
        fitIndex = walker.fitIndex

        npout = 0
        inside = 0
        Ltry = 0
        size = 0.5

        self.plotter.start( )
        um = UnitMovements( model, allpars, fitIndex, self, size )

        ptry = allpars.copy()
#        print( "GE0  ", fma( ptry ) )

        nstep = int( self.nstep * ( 1 + self.rng.rand() ) )
        maxtrial = self.maxtrials * nstep
        Lbest = self.walkers[-1].logL
        step = 0
        trial = 0

        while True:
            trial += 1
            um.setParameters( model, allpars )
            if inside == 0 :                            # safely inside lowLhood area
                ptry[fitIndex] = um.stepPars( 1.0 )

                self.plotter.move( allpars, ptry, 0 )
            elif inside == 1 :                          # first time outside -> mirror
                f = ( Lhood - lowLhood ) / ( Lhood - Ltry )     # lin interpolation to edge
#                print( "GE1  ", fmt(f), fmt(Lhood), fmt(lowLhood), fmt(Ltry) )
                pedge = ptry.copy()
                pedge[fitIndex] = um.stepPars( f )                # ptry on edge
#                print( "GE2  ", fma(pedge) )
#                [print( "edge  ", pt, math.frexp( pt ) ) for pt in pedge ]
#                print( "GE2  ", fma(pedge) )
                dLdp = self.errdis.partialLogL( model, pedge, fitIndex )
#                [print( "llde  ", pt, math.frexp( pt ) ) for pt in dLdp ]
                self.plotter.move( allpars, pedge, 1 )
#                print( "GE3  ", fma( dLdp ) )

                um.mirrorOnLowL( dLdp )
                ptry[fitIndex] = um.stepPars( 1 - f )
#                print( "GE4  ", ( ptry ) )

                self.plotter.move( pedge, ptry, 2 )
            else:                                       # mirroring failed; do reverse
                size *= 0.7
                um.reverseVelocity( size )
                ptry[fitIndex] = um.stepPars( 1.0 )
#                print( "GE5  ", ( ptry ) )

                self.plotter.move( allpars, ptry, 3 )

#            ## future extension
#            if self.constrain :
#                xdata = self.errdis.xdata
#                ptry = self.constrain( model, ptry, xdata )


#            print( "GEng  ", (ptry) )
#            [print( "ptry  ", pt, math.frexp( pt ) ) for pt in ptry ]

            Ltry = self.errdis.logLikelihood( model, ptry )

#            print( "Geng  ", self.rng.rand(), Ltry, math.frexp(Ltry), inside, (Ltry >= lowLhood) )

            if Ltry >= lowLhood:
                allpars = ptry.copy( )
                Lhood = Ltry
                self.reportSuccess( )
                npout = len( allpars )
                inside = 0
                step += 1
                if Ltry > Lbest :
                    Lbest = Ltry
                    self.setSample( self.walkers[-1], model, ptry.copy(), Lbest,
                                    fitindex=fitIndex )
                    self.reportBest()

            else:
                inside += 1
                if inside == 1:
                    self.reportReject( )
                else:
                    self.reportFailed( )

#            print( "GEng  ", fma(ptry), fmt(Ltry) )
#            print( "      ", fma( self.unitRange ), inside, step, fmt( size ) )

            if not ( step < nstep and trial < maxtrial ):
                break

        self.setSample( walker, model, allpars, Lhood, fitindex=fitIndex )

        self.plotter.stop()
        return npout

import matplotlib.pyplot as plt

class UnitMovements( object ):

    def __init__( self, model, allpars, fitIndex, engine, size ):
        self.model = model
        self.np = len( fitIndex )
        self.fitIndex = fitIndex
        self.engine = engine
        self.setParameters( model, allpars )

        if self.np > len( self.engine.unitRange ) :
            self.engine.unitRange = numpy.ones( self.np, dtype=float )

        self.upran = self.engine.unitRange[fitIndex]
        self.setVelocity( size )

    def setParameters( self, model, allpars ):
        self.upar = self.engine.domain2Unit( model, allpars, kpar=self.fitIndex )

    def mirrorOnLowL( self, dLdp ):
#        print( "dLdp  ", fmt( dLdp ) )
#        print( "uvel  ", fmt( self.uvel ) )
#        inprod = numpy.inner( dLdp, self.uvel )
        inprod = numpy.sum( dLdp * self.uvel )
#        print( "inpr  ", fmt( inprod ) )
#        sumsq  = numpy.inner( dLdp, dLdp )
        sumsq  = numpy.sum( dLdp * dLdp )
#        print( "sumq  ", fmt( sumsq ) )
        self.uvel -= 2 * dLdp * inprod / sumsq
#        print( "uvel  ", fmt( self.uvel ) )



    def setVelocity( self, size ):
        if self.model.isDynamic():
            self.setVelocityDynamic( size )
        else:
            self.setVelocityStatic( size )

    def allpars2unit( self, kw ) :
        allpars = self.engine.walkers[kw].allpars
        return self.engine.domain2Unit( self.model, allpars, kpar=self.fitIndex )

    def setVelocityStatic( self, size ):
        self.uvel  = self.uniform() * self.upran * size

        """
        # find two randomly chosen walkers
        nm = len( self.engine.walkers )
        k1 = k0 = self.engine.rng.randint( nm )
        while k1 == k0:
            k1 = self.engine.rng.randint( nm )

        # subtract the parameter postions to get a velocity
        self.uvel = ( self.allpars2unit( k0 ) - self.allpars2unit( k1 ) ) * size

        # add a random contibution
        rv = self.uniform() * self.upran * size
        self.uvel = ( nm * self.uvel + self.np * rv ) / ( nm + self.np )
        """

    def uniform( self ) :
        return self.engine.rng.rand( self.np ) - 0.5

    def setVelocityDynamic( self, size ):
#        print( "SVD   ", self.np, size, len( self.engine.walkers[0].allpars), self.engine.unitRange )
        self.uvel = self.uniform() * size * self.engine.unitRange[self.fitIndex]

    def reverseVelocity( self, size ):
        upv = self.uvel                 # keep original velocity
        self.setVelocity( size )        # get a new one to perturb
        nm = len( self.engine.walkers )
        self.uvel = size * ( self.np * self.uvel - nm * upv ) / ( nm + self.np )
#        self.uvel -= ( 0.5 * upv )      # subtract original

    def stepPars( self, f ):
        uv = self.uvel
        pv = self.upar + uv * f
        # check if outside [0,1]
        pv, uv = numpy.where( pv <= 0, ( -pv, -uv ), ( pv, uv ) )
        self.upar, self.uvel = numpy.where( pv >= 1, ( 2 - pv, -uv ), ( pv, uv ) )
        return self.engine.unit2Domain( self.model, self.upar, kpar=self.fitIndex )

