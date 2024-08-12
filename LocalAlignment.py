import numpy as np;
import matplotlib.pyplot as plt
from GlobalAlignment import GlobalAlignment

class LocalAlignment(GlobalAlignment):
    
    def __init__(self, s1, s2, gapPenalty = -4, matchScore = 3, baseMatchScore = 1, mismatchPenalty = -3):
        super().__init__(s1, s2, gapPenalty, matchScore, baseMatchScore, mismatchPenalty)
        self.terminatePointer = 'X'

    def _fillGrids(self):
        self._createOptimalityGrid()
        self._createScoreGrid()
        self._createPointerGrid()

        for yVal, row in enumerate(self.optimalityGrid):
            for xVal in range(len(row)):

                if yVal == 0:
                    self.optimalityGrid[yVal][xVal] = 0
                    self.pointerGrid[yVal][xVal] = self.terminatePointer
                    continue

                if xVal == 0:
                    self.optimalityGrid[yVal][xVal] = 0
                    self.pointerGrid[yVal][xVal] = self.terminatePointer
                    continue
                
                leftScore = self.optimalityGrid[yVal][xVal - 1] + self.gapPenalty
                diagonalScore = self.optimalityGrid[yVal - 1][xVal - 1]  + self.scoresForGrid[yVal-1][xVal-1]
                upScore = self.optimalityGrid[yVal - 1][xVal]  + self.gapPenalty

                self.optimalityGrid[yVal][xVal] = max(leftScore, upScore, diagonalScore, 0)

                if self.optimalityGrid[yVal][xVal] == 0:
                    self.pointerGrid[yVal][xVal] = self.terminatePointer

                if self.optimalityGrid[yVal][xVal] == leftScore:
                    self.pointerGrid[yVal][xVal] = self.horizontal
                
                if self.optimalityGrid[yVal][xVal] == upScore:
                    self.pointerGrid[yVal][xVal] = self.vertical
                
                if self.optimalityGrid[yVal][xVal] == diagonalScore:
                    self.pointerGrid[yVal][xVal] = self.diagonal
    
    def _traceBack(self):

        maxVal = -9e99
        coordOfMaxVal = np.array([0, 0])

        for yVal, row in enumerate(self.optimalityGrid):
            for xVal in range(len(row)):

                rowMax = max(maxVal, row[xVal])

                if(maxVal < rowMax):
                    maxVal = rowMax
                    coordOfMaxVal[0] = yVal
                    coordOfMaxVal[1] = xVal
        
        #Traceback
        x = coordOfMaxVal[1]
        y = coordOfMaxVal[0]

        notTerminated = True
        while notTerminated:
            
            if self.pointerGrid[y][x] == self.diagonal:
                self.alignedXAxisStrand += self.xAxisStrand[x-1]
                self.alignedYAxisStrand += self.yAxisStrand[y-1]
            
                x -= 1
                y -= 1
                continue
            
            if self.pointerGrid[y][x] == self.horizontal:
                self.alignedXAxisStrand += self.xAxisStrand[x-1]
                self.alignedYAxisStrand += '-'

                x -= 1
                continue
            
            if self.pointerGrid[y][x] == self.vertical:
                self.alignedXAxisStrand += '-'
                self.alignedYAxisStrand += self.yAxisStrand[y-1]

                y -= 1
                continue
            
            if self.pointerGrid[y][x] == self.terminatePointer:
                notTerminated = False
        
        self.alignedXAxisStrand = self.alignedXAxisStrand[::-1]
        self.alignedYAxisStrand = self.alignedYAxisStrand[::-1]

        print(self.alignedYAxisStrand)
        print(self.alignedXAxisStrand)
    
    def alignSubStrandsAndShowGraph():

        s = LocalAlignment()
        s._fillGrids()
        s._traceBack()
        
        plt.imshow( s.optimalityGrid , cmap = 'magma' )
  
        # Adding details to the plot
        plt.title( "Optimality Matrix Heat Map" )
        plt.xlabel("".join([x for x in s.xAxisStrand])) 
        plt.ylabel(("".join([y for y in s.yAxisStrand])) )
        plt.colorbar()
        plt.show()
    
    def alignSubStrands(self):
        self._fillGrids()
        self._traceBack()
