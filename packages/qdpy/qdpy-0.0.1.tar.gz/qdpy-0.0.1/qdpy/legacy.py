#    This file is part of qdpy.
#
#    qdpy is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    qdpy is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with qdpy. If not, see <http://www.gnu.org/licenses/>.

"""Old preliminary code. It is not documented and will be removed in the future."""


import math
import numpy as np
import multiprocessing
import sys
import copy
import os
import pickle
import time
#import asyncio
import gc
from scipy.spatial.distance import euclidean
from sklearn.cluster import KMeans
from sklearn.gaussian_process import GaussianProcessRegressor
import itertools
from timeit import default_timer as timer



def mutateUniformInt(ind, mutationPb, indBounds):
    for i in range(len(ind)):
        if np.random.random() < mutationPb:
            ind[i] = np.random.randint(indBounds[0], indBounds[1])

def mutateUniform(ind, mutationPb, indBounds):
    for i in range(len(ind)):
        if np.random.random() < mutationPb:
            ind[i] = np.random.uniform(indBounds[0], indBounds[1])

def generateUniformInt(dimension, indBounds, nb):
    res = []
    for i in range(nb):
        res.append(np.random.randint(indBounds[0], indBounds[1] + 1, dimension))
    return res

def generateUniform(dimension, indBounds, nb):
    res = []
    for i in range(nb):
        res.append(np.random.uniform(indBounds[0], indBounds[1], dimension))
    return res






########### MAP-Elites ########### {{{1
class MapElites(object):
    def __init__(self, dimension, evalFn, nbBins, featuresBounds = [(0., 1.)], initBatchSize = 120, batchSize=40, nbIterations = 10, indBounds = (0, 100), mutationPb = 0.2, savePeriod = 0, logBasePath = ".", reevalTimeout = None, mutate = None, initiate = None, iterationFilenames = "iteration-%i.p", finalFilename = "final.p", fitnessBounds = (0., 1.)):
        self.dimension = dimension
        self.evalFn = evalFn
        self.nbBins = nbBins
        self.featuresBounds = featuresBounds
        self.initBatchSize = initBatchSize
        self.nbIterations = nbIterations
        self.batchSize = batchSize
        self.indBounds = indBounds
        self.mutationPb = mutationPb
        self.savePeriod = savePeriod
        self.logBasePath = logBasePath
        self.reevalTimeout = reevalTimeout
        self.mutate = mutate
        self.initiate = initiate
        self.iterationFilenames = iterationFilenames
        self.finalFilename = finalFilename
        self.fitnessBounds = fitnessBounds
        self.callEvalFnOnEntierBatch = False
        self.reinit()

    def __del__(self):
        self._closePool()

    def __getstate__(self):
        odict = self.__dict__.copy()
        del odict['pool']
        del odict['map']
        del odict['_queueEvals']
        return odict

    def _closePool(self):
        if hasattr(self, 'pool'):
            self.pool.close()
            self.pool.terminate()

    def _defaultMutate(self, ind):
        #return mutateUniformInt(ind, self.mutationPb, self.indBounds)
        return mutateUniformInt

    def reinit(self):
        if not hasattr(self, '_infoToSave'):
            self._infoToSave = {}
        self._closePool()
        self.pool = multiprocessing.Pool()
        self.map = self.pool.starmap
        self._queueEvals = multiprocessing.Queue()
        #self._evalQueue = multiprocessing.Queue()
        self._unfinishedEvals = 0
        self._evalId = itertools.count()
        if not self.mutate:
            self.mutate = self._defaultMutate
        if not self.initiate:
            self.initiate = self._defaultInitiation
        self.totalElapsed = 0.

        self.initPop = []
        assert(self.nbIterations > 0)
        self.currentIteration = 0
        self.currentEvaluation = 0
        if self.nbBins == None:
            self.nbBins = np.repeat(10, len(self.featuresBounds))
        assert(len(self.featuresBounds) == len(self.nbBins))
        #self._binsSize = [(self.featuresBounds[1] - self.featuresBounds[0]) / float(b) for b in self.nbBins] 
        self._binsSize = [(self.featuresBounds[bi][1] - self.featuresBounds[bi][0]) / float(self.nbBins[bi]) for bi in range(len(self.nbBins))]
        assert(len(self.nbBins))
        self.performances = np.full(self.nbBins, self.fitnessBounds[0]) #np.zeros(shape=self.nbBins)
        self.features = np.zeros(shape=list(self.nbBins) + [len(self.nbBins)])
        self.solutions = {}
        self.bestInIteration = None
        self.bestInIterationFitness = self.fitnessBounds[0]
        self.bestEver = None
        self.bestEverFitness = self.fitnessBounds[0]

    def _valsToElitesIndex(self, vals):
        index = []
        assert(len(vals) == len(self.nbBins))
        for i in range(len(vals)):
            normalisedVal = vals[i] - self.featuresBounds[i][0]
            if normalisedVal == self.featuresBounds[i][1] - self.featuresBounds[i][0]:
                partial = self.nbBins[i] - 1
            elif normalisedVal > self.featuresBounds[i][1] - self.featuresBounds[i][0]:
                print("WARNING: feature %i out of bounds: %s" % (i, vals))
                return None
            else:
                partial = int(normalisedVal / self._binsSize[i])
            index.append(partial)
        return tuple(index)

    def _evalFnWrapper(self, ind, expeId):
        def startEval(newInd):
            startTime = timer()
            res = self.evalFn(ind, expeId)
            endTime = timer()
            elapsed = endTime - startTime
            return elapsed, res
        totalElapsed = 0.
        currentInd = ind
        while(True): # XXX bad !
            elapsed, res = startEval(currentInd)
            totalElapsed += elapsed
            if self.reevalTimeout and self.reevalTimeout > totalElapsed:
                fitness = res[0]
                if fitness <= 0.000001:
                    # Perform a reevaluation
                    print("Performed a Reevaluation after:%f sec" % totalElapsed)
                    self.mutate(currentInd, self.mutationPb, self.indBounds)
                    sys.stdout.flush()
                    continue
                else:
                    return currentInd, res
            else:
                return currentInd, res


    def _evaluatePop(self, pop):
        startTime = timer()
        pop = np.unique(pop, axis=0)
        listEvalIds = list(next(self._evalId) for _ in pop)
        # Evaluate the individuals
        #popFitnesses = np.array(self.map(self.evalFn, pop)) #self.toolbox.map(self.toolbox.evaluate, pop)
        #popFitnesses = np.array(self.map(self.evalFn, list(zip(pop, listEvalIds)))) #self.toolbox.map(self.toolbox.evaluate, pop)
        #resFromEvals = self.map(self._evalFnWrapper, list(zip(pop, listEvalIds)))
        #popFinalInds, popFitnesses = zip(*resFromEvals)

        if self.callEvalFnOnEntierBatch:
            popFitnesses = np.array(list(self.evalFn(pop, listEvalIds)))
        else:
            popFitnesses = self.map(self.evalFn, list(zip(pop, listEvalIds)))
        #nbMaxEvalsPerRound = 1000
        #if len(listEvalIds) > nbMaxEvalsPerRound:
        #    nbRounds = int(len(listEvalIds) / nbMaxEvalsPerRound)
        #    popFitnesses = []
        #    for i in range(nbRounds):
        #        fitList = self.map(self.evalFn, list(zip(pop[i * nbMaxEvalsPerRound: (i+1) * nbMaxEvalsPerRound], listEvalIds[i * nbMaxEvalsPerRound: (i+1) * nbMaxEvalsPerRound])))
        #        popFitnesses += fitList
        #        # Perform garbage collection
        #        while gc.collect() > 0:
        #            pass
        #else:
        #    popFitnesses = self.map(self.evalFn, list(zip(pop, listEvalIds)))
        while gc.collect() > 0:
            pass

        popFitnesses = np.array(list(popFitnesses))
        popPerformances = popFitnesses[:,0]
        popFeatures = popFitnesses[:,1:]
        # Record individuals
        for indIndex in range(len(pop)):
            ind = pop[indIndex]
            elitesIndex = self._valsToElitesIndex(popFeatures[indIndex])
            if elitesIndex == None:
                continue
            if self.performances[elitesIndex] < popPerformances[indIndex]:
                self.solutions[elitesIndex] = ind
                self.performances[elitesIndex] = popPerformances[indIndex]
                self.features[elitesIndex] = popFeatures[indIndex]
            if popPerformances[indIndex] > self.bestInIterationFitness:
                self.bestInIterationFitness = popPerformances[indIndex]
                self.bestInIteration = ind
        if self.bestInIterationFitness > self.bestEverFitness:
            self.bestEverFitness = self.bestInIterationFitness
            self.bestEver = self.bestInIteration
        endTime = timer()
        elapsed = endTime - startTime
        #return popFinalInds, self.bestInIterationFitness, elapsed
        return self.bestInIterationFitness, elapsed


    def _evaluateIndAsync(self, ind = None):
        if ind is None:
            currentElites = list(self.solutions.values())
            if not len(currentElites):
                raise ValueError("No elites were found in initial batch !")
            ind = copy.deepcopy(currentElites[np.random.randint(0, len(currentElites))])
            self.mutate(ind, self.mutationPb, self.indBounds)
        #print("DEBUGasync: ", ind)
        evalId = next(self._evalId)
        self._unfinishedEvals += 1
        asyncResFromEval = self.pool.apply_async(self._evalFnWrapper, [ind, evalId], callback = self._evaluateIndAsyncCallback)
        return asyncResFromEval

    def _evaluateIndAsyncCallback(self, param):
        ind, res = param
        #print("DEBUGasyncC1: ", res)
        performance = res[0]
        features = res[1:]
        elitesIndex = self._valsToElitesIndex(features)
        if self.performances[elitesIndex] < performance:
            self.solutions[elitesIndex] = ind
            self.performances[elitesIndex] = performance
            self.features[elitesIndex] = features
        if performance > self.bestInIterationFitness:
                self.bestInIterationFitness = performance
                self.bestInIteration = ind
        # Update bestever
        if self.bestInIterationFitness > self.bestEverFitness:
            self.bestEverFitness = self.bestInIterationFitness
            self.bestEver = self.bestInIteration

        self._unfinishedEvals -= 1
        self.currentEvaluation += 1
        #print("DEBUGasyncC2: ", self._unfinishedEvals, self.currentEvaluation, (self.currentEvaluation - self.initBatchSize) % self.batchSize)
        sys.stdout.flush()
        if self.currentEvaluation == self.initBatchSize:
            # Verify if the initial batch is finished
            print("#0 bestInBatch:%f bestEver:%f" % (self.bestInIterationFitness, self.bestInIterationFitness))
            sys.stdout.flush()
        elif self.currentEvaluation > self.initBatchSize and (self.currentEvaluation - self.initBatchSize) % self.batchSize == 0:
            # Verify if this iteration is finished
            self.currentIteration += 1
            print("#%i bestInBatch:%f bestEver:%f" % (self.currentIteration, self.bestInIterationFitness, self.bestEverFitness))
            sys.stdout.flush()
            if self.savePeriod and np.mod(self.currentIteration, self.savePeriod) == 0:
                #print("DEBUGasyncC3: ", self.iterationFilenames, self.currentIteration)
                self.save(os.path.join(self.logBasePath, self.iterationFilenames % self.currentIteration))

        # Verify if a new eval must be launched
        if self.currentEvaluation + self._unfinishedEvals >= self.initBatchSize + self.nbIterations * self.batchSize:
            if self._unfinishedEvals == 0:
                # All evaluation are finished
                self.save(os.path.join(self.logBasePath, self.finalFilename))
        else:
            # Launch new eval
            self._evaluateIndAsync()



    def _defaultInitiation(self, dimension, indBounds, nb):
        return generateUniformInt(dimension, self.indBounds, nb)

    def _generateInitBatch(self):
        self.initPop = np.unique(self.initiate(self.dimension, self.indBounds, self.initBatchSize), axis=0)
        #self.initPop = []
        #for i in range(self.initBatchSize):
        #    #self.initPop.append(np.random.randint(self.indBounds[0], self.indBounds[1], self.dimension))
        #    #self.initPop.append(np.random.uniform(self.indBounds[0], self.indBounds[1], self.dimension))
        #    self.initPop.append(self.initiate(self.dimension, self.indBounds))
        return self.initPop

    def _iterationMessage(self, prefixLogs, iteration, batch, bestInIterationFitness, bestEverFitness, elapsed):
        #print("%s%i batchSize:%i bestInBatch:%f bestEver:%f elapsed:%f" % (prefixLogs, iteration, len(batch), bestInIterationFitness, bestEverFitness, elapsed))
        print("%s%i batchSize:%i bestEver:%f elapsed:%f" % (prefixLogs, iteration, len(batch), bestEverFitness, elapsed))

    def run(self, initBatch = None, nbIterations = None, disableLogs = False, prefixLogs = "#"):
        startTime = timer()
        if initBatch:
            self.initPop = initBatch
        else:
            self._generateInitBatch()
        if nbIterations == None:
            nbIterations = self.nbIterations
        #self.initPop, self.bestInIterationFitness, elapsed = self._evaluatePop(self.initPop)
        self.bestInIterationFitness, elapsed = self._evaluatePop(self.initPop)
        self.bestEverFitness = self.bestInIterationFitness
        self.currentEvaluation = len(self.initPop)
        self._iterationMessage(prefixLogs, 0, self.initPop, self.bestInIterationFitness, self.bestEverFitness, elapsed)
        sys.stdout.flush()
        for iteration in range(1, nbIterations):
            self.currentIteration = iteration
            self.currentEvaluation += self.batchSize
            currentElites = list(self.solutions.values())
            if not len(currentElites):
                raise ValueError("No elites were found in initial batch !")
            newPop = []
            for i in range(self.batchSize):
                ind = copy.deepcopy(currentElites[np.random.randint(0, len(currentElites))])
                self.mutate(ind, self.mutationPb, self.indBounds)
                newPop.append(ind)
            #newPop, self.bestInIterationFitness, elapsed = self._evaluatePop(newPop)
            self.bestInIterationFitness, elapsed = self._evaluatePop(newPop)
            #print("%s%i bestInBatch:%f bestEver:%f elapsed:%f elapsedPerInd:%f" % (prefixLogs, iteration, self.bestInIterationFitness, self.bestEverFitness, elapsed, elapsed / len(newPop)))
            self._iterationMessage(prefixLogs, iteration, newPop, self.bestInIterationFitness, self.bestEverFitness, elapsed)
            sys.stdout.flush()
            if not disableLogs and self.savePeriod and np.mod(self.currentIteration, self.savePeriod) == 0:
                self.save(os.path.join(self.logBasePath, self.iterationFilenames % iteration))
            # Perform garbage collection
            while gc.collect() > 0:
                pass
        if not disableLogs and self.finalFilename:
            self.save(os.path.join(self.logBasePath, self.finalFilename))
        endTime = timer()
        self.totalElapsed += endTime - startTime
        print("Total elapsed:%f" % (self.totalElapsed))
        return (self.bestEver, self.bestEverFitness)


    def runAsync(self, initBatch = None):
        if initBatch:
            self.initPop = initBatch
        else:
            self._generateInitBatch()
        evalsFuturesList = []
        for i in range(len(self.initPop)):
            evalsFuturesList.append(self._evaluateIndAsync(self.initPop[i]))
            #self._evaluateIndAsync(self.initPop[i])
        # Main loop
        while(True):
            #print("DEBUG1:", self.currentEvaluation, self.initBatchSize + self.nbIterations * self.batchSize)
            #print("DEBUG1b: ", [x.ready() for x in evalsFuturesList])
            if self.currentEvaluation >= self.initBatchSize + self.nbIterations * self.batchSize:
                break
            time.sleep(1)
        return (self.bestEver, self.bestEverFitness)


    def generateOutputDict(self):
        outputDict = {}
        outputDict['performances'] = self.performances
        outputDict['features'] = self.features
        outputDict['solutions'] = self.solutions
        outputDict['dimension'] = self.dimension
        outputDict['nbBins'] = self.nbBins
        outputDict['featuresBounds'] = self.featuresBounds
        outputDict['initBatchSize'] = self.initBatchSize
        outputDict['nbIterations'] = self.nbIterations
        outputDict['batchSize'] = self.batchSize
        outputDict['indBounds'] = self.indBounds
        outputDict['mutationPb'] = self.mutationPb
        outputDict['currentIteration'] = self.currentIteration
        outputDict['initPop'] = self.initPop
        outputDict['bestEver'] = self.bestEver
        outputDict['bestEverFitness'] = self.bestEverFitness
        outputDict = {**outputDict, **self._infoToSave}
        return outputDict

    def save(self, outputFile):
        outputDict = self.generateOutputDict()
        with open(outputFile, "wb") as f:
            pickle.dump(outputDict, f)

    def addSavingInfo(self, key, value):
        self._infoToSave[key] = value



########### CVT-MAP-Elites ########### {{{1
class CVTMapElites(MapElites):
    def __init__(self, dimension, evalFn, nbBins, nbClusters, featuresBounds = [(0.0, 1.0)], initBatchSize = 120, batchSize=40, nbIterations = 10, indBounds = (0, 100), mutationPb = 0.2, savePeriod = 0, logBasePath = ".", nbSampledPoints = 50000, reevalTimeout = 5., mutate = None, initiate = None, iterationFilenames = "iteration-%i.p", finalFilename = "final.p", fitnessBounds = (0., 1.)):
        self.nbClusters = nbClusters
        self.nbSampledPoints = nbSampledPoints
        super().__init__(dimension, evalFn, nbBins, featuresBounds, initBatchSize, batchSize, nbIterations, indBounds, mutationPb, savePeriod, logBasePath, reevalTimeout, mutate, initiate, iterationFilenames, finalFilename, fitnessBounds)

    def reinit(self):
        super().reinit()
        self.performances = np.zeros(shape=self.nbClusters)
        self.features = np.zeros(shape=[self.nbClusters, len(self.nbBins)])
        # Init clusters
        sample = np.random.uniform(self.featuresBounds[0][0], self.featuresBounds[0][1], (self.nbSampledPoints, len(self.nbBins)))
        kmeans = KMeans(init="k-means++", n_clusters=self.nbClusters, n_init=1, n_jobs=1, verbose=0)
        kmeans.fit(sample)
        self.clusterCenters = kmeans.cluster_centers_

    def _valsToElitesIndex(self, vals):
        closestDist = float("inf")
        closestCluster = 0
        for i in range(len(self.clusterCenters)):
            dist = euclidean(self.clusterCenters[i], vals)
            if dist < closestDist:
                closestDist = dist
                closestCluster = i
        return (closestCluster,)

    def generateOutputDict(self):
        outputDict = super().generateOutputDict()
        outputDict['nbClusters'] = self.nbClusters
        outputDict['nbSampledPoints'] = self.nbSampledPoints
        outputDict['clusterCenters'] = self.clusterCenters
        outputDict = {**outputDict, **self._infoToSave}
        return outputDict







########### Factory ########### {{{1

class AlgorithmFactory(object):
    def __init__(self, algoType = "map-elites", nbDim = 50, evalFn = None, nbBins = None, nbClusters = 30, nbSampledPoints = 50000, featuresBounds = [(0., 1.)], indBounds = (0, 100), initBatchSize = 10000, batchSize = 4000, nbIterations = 500, mutationPb = 0.2, nbCenters = 20, savePeriod = 0, logBasePath = ".", reevalTimeout = None, mutate = None, initiate = None, iterationFilenames = "iteration-%i.p", finalFilename = "final.p",  instanceName = "", fitnessBounds = (0., 1.)):
        self.algoType = algoType
        self.nbDim = nbDim
        self.evalFn = evalFn
        self.nbBins = nbBins
        self.nbClusters = nbClusters
        self.nbSampledPoints = nbSampledPoints
        self.featuresBounds = featuresBounds
        self.indBounds = indBounds
        self.initBatchSize = initBatchSize
        self.batchSize = batchSize
        self.nbIterations = nbIterations
        self.mutationPb = mutationPb
        self.nbCenters = nbCenters
        self.savePeriod = savePeriod
        self.logBasePath = logBasePath
        self.reevalTimeout = reevalTimeout
        self.mutate = mutate
        self.initiate = initiate
        self.iterationFilenames = iterationFilenames
        self.finalFilename = finalFilename
        self.instanceName = instanceName
        self.fitnessBounds = fitnessBounds
        self.algo = None

    def build(self):
        if self.algoType == "map-elites":
            self.algo = MapElites(self.nbDim, self.evalFn, self.nbBins, self.featuresBounds, self.initBatchSize, self.batchSize, self.nbIterations, self.indBounds, self.mutationPb, self.savePeriod, self.logBasePath, self.reevalTimeout, self.mutate, self.initiate, self.iterationFilenames, self.finalFilename, fitnessBounds = self.fitnessBounds)
        elif self.algoType == "cvt-map-elites":
            self.algo = CVTMapElites(self.nbDim, self.evalFn, self.nbBins, self.nbClusters, self.featuresBounds, self.initBatchSize, self.batchSize, self.nbIterations, self.indBounds, self.mutationPb, self.savePeriod, self.logBasePath, self.nbSampledPoints, self.reevalTimeout, self.mutate, self.initiate, self.iterationFilenames, self.finalFilename, fitnessBounds = self.fitnessBounds)
        else:
            raise ValueError("Unknown algoType: '%s'" % self.algoType)
        return self.algo


    def fromConfig(self, config):
        def setIfExists(key):
            o = config.get(key)
            if o:
                self.__dict__[key] = o
        def buildIfExists(key):
            o = config.get(key)
            if o:
                fact = AlgorithmFactory()
                fact.fromConfig(o)
                fact.evalFn = self.evalFn
                fact.featuresBounds = self.featuresBounds
                self.__dict__[key] = fact.build()
        setIfExists('algoType')
        setIfExists('nbDim')
        setIfExists('nbBins')
        setIfExists('nbClusters')
        setIfExists('nbSampledPoints')
        setIfExists('featuresBounds')
        setIfExists('indBounds')
        setIfExists('fitnessBounds')
        setIfExists('initBatchSize')
        setIfExists('batchSize')
        setIfExists('nbIterations')
        setIfExists('mutationPb')
        setIfExists('nbCenters')
        setIfExists('savePeriod')
        setIfExists('reevalTimeout')



# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
