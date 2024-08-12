import numpy as np;
import matplotlib.pyplot as plt

class GlobalAlignment:

    def __init__(self, s1, s2, gapPenalty = -4, matchScore = 3, baseMatchScore = 1, mismatchPenalty = -3):

        self.gapPenalty = gapPenalty
        self.matchScore = matchScore
        self.baseMatchScore = baseMatchScore
        self.mismatchPenalty = mismatchPenalty

        self.diagonal = '\\'
        self.vertical = '|'
        self.horizontal = '-'


        self.yAxisStrand = s2
        self.xAxisStrand = s1

        self.alignedYAxisStrand = ""
        self.alignedXAxisStrand = ""



    def _calcScore(self, a, b):
        if a == b:
            return self.matchScore
        elif (a == 'T' and b == 'C') or (a == 'C' and b == 'T') or (a == 'G' and b == 'A') or (a == 'A' and b == 'G'):
            return self.baseMatchScore
        else:
            return self.mismatchPenalty
        
    def _createScoreGrid(self):
        self.scoresForGrid = np.array([[0 for char in self.xAxisStrand] for char in self.yAxisStrand])
        for yVal, row in enumerate(self.scoresForGrid):
            for xVal in range(len(row)):
                   self.scoresForGrid[yVal][xVal] = self._calcScore(self.yAxisStrand[yVal], self.xAxisStrand[xVal])
        return

    def _createPointerGrid(self):
        self.pointerGrid = np.array([[' ' for char in range(len(self.xAxisStrand) +1)] for char in range(len(self.yAxisStrand)+1)]) # \ = diagonal, | = Upward, - = Leftward
        return
    
    def _createOptimalityGrid(self):
        self.optimalityGrid = np.array([[0 for char in range(len(self.xAxisStrand) +1)] for char in range(len(self.yAxisStrand)+1)])
        return
    
    def _fillGrids(self):
        self._createOptimalityGrid()
        self._createScoreGrid()
        self._createPointerGrid()

        for yVal, row in enumerate(self.optimalityGrid):
            for xVal in range(len(row)):
                
                if yVal == 0 and xVal == 0: # Corner Case (literally)
                    self.optimalityGrid[yVal][xVal] = 0
                    continue
                
                leftScore = self.optimalityGrid[yVal][xVal - 1] + self.gapPenalty

                if yVal == 0:
                    self.optimalityGrid[yVal][xVal] = leftScore 
                    self.pointerGrid[yVal][xVal] = self.horizontal
                    continue
                
                upScore = self.optimalityGrid[yVal - 1][xVal]  + self.gapPenalty
                
                if xVal == 0:
                    self.optimalityGrid[yVal][xVal] = upScore
                    self.pointerGrid[yVal][xVal] = self.vertical
                    continue
                
                diagonalScore = self.optimalityGrid[yVal - 1][xVal - 1]  + self.scoresForGrid[yVal-1][xVal-1]

                self.optimalityGrid[yVal][xVal] = max(leftScore, upScore, diagonalScore)

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

        while x > 0 and y > 0:
            
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
        
        self.alignedXAxisStrand = self.alignedXAxisStrand[::-1]
        self.alignedYAxisStrand = self.alignedYAxisStrand[::-1]

        print(self.alignedYAxisStrand)
        print(self.alignedXAxisStrand)
    
    def alignStrandsAndShowGraph(s1, s2): #intended for usage with ipython or command-line

        s = GlobalAlignment(s1, s2)
        s._fillGrids()
        s._traceBack()
        plt.imshow( s.optimalityGrid , cmap = 'magma' )
  
        # Adding details to the plot
        plt.title( "Optimality Matrix Heat Map" )
        plt.xlabel("".join([x for x in s.xAxisStrand])) 
        plt.ylabel(("".join([y for y in s.yAxisStrand])) )
        plt.colorbar()
        plt.show()

    def alignStrands(self):
        self._fillGrids()
        self._traceBack()
        

        



