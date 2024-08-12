import matplotlib.pyplot as plt
import numpy as np
from nicegui import ui
import GlobalAlignment
import LocalAlignment



def alignStringsAndShowPrettyGraphics(isglobal, s1, s2, gapPenalty, matchScore, baseMatchScore, mismatchPenalty):
    if(isglobal):
        Aligner = GlobalAlignment.GlobalAlignment(s1, s2, int(gapPenalty), int(matchScore), int(baseMatchScore), int(mismatchPenalty))
        Aligner.alignStrands()
    
    if(not isglobal):
        Aligner = LocalAlignment.LocalAlignment(s1, s2, int(gapPenalty), int(matchScore), int(baseMatchScore), int(mismatchPenalty))
        Aligner.alignSubStrands()

    output.clear()
    with output:
        with ui.grid(columns=2):
            ui.label("Sequence One")
            ui.label("Sequence Two")
            for x in range(max(len(Aligner.alignedXAxisStrand), len(Aligner.alignedYAxisStrand))):
                ui.label(Aligner.alignedXAxisStrand[x])
                ui.label(Aligner.alignedYAxisStrand[x])
    
        with ui.pyplot(figsize=(6, 6)):
            plt.imshow(Aligner.optimalityGrid , cmap = 'magma')
            plt.title("Heat Map")
            plt.xlabel("Nth Character of " + "".join([x for x in Aligner.xAxisStrand])) 
            plt.ylabel("Nth Character of " + "".join([y for y in Aligner.yAxisStrand]))
            plt.colorbar()
        
        with ui.expansion("About the Heat Map"):
            ui.markdown('''
## Heat Map
                        
Visual representation of how the algorthim calculated the alignment. 
                        
To put it simply, it matches each character of each sequence and uses the scoring matrix 
                        
to determine the amount of points that the match will yield added to the amount of points gained/lost getting to that position.
                        
The overall score is indicated by a color (key on the right side). The algorthim then takes the 
                        
highest score and traces back to the origin in global alignment or until the sequence is not strong anymore in local alignment.
                        
There is a faint path which shows the path the algorithm took to reach its location

''')
            ui.link("Link to algorithm behind Local Alignment", "https://en.wikipedia.org/wiki/Smith%E2%80%93Waterman_algorithm#:~:text=best%20local%20alignment.-,Explanation,which%20are%20represented%20by%20dashes.")
            ui.link("Link to the algorithm behind Global Alignment", "https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm#:~:text=The%20Needleman%E2%80%93Wunsch%20algorithm%20is%20still%20widely%20used%20for%20optimal,alignments%20having%20the%20highest%20score.")




ui.markdown("# Global and Local Sequence Alignment Tool")
ui.link('Check out my blog', 'https://compbioodyssey.com')

sequenceOne = ui.input(label='Sequence One', placeholder='Input Sequence One Here', value='').props('clearable') 
sequenceTwo = ui.input(label='Sequence Two', placeholder='Input Sequence One Here', value='').props('clearable')

with ui.expansion("Edit the Scoring Function"):
    gapPenalty = ui.input(label= 'Gap Penalty', placeholder='Input an integer', value='-1').props('clearable')
    matchScore = ui.input(label= 'Match Score', placeholder='Input an integer', value='1').props('clearable')
    baseMatchScore = ui.input(label= 'Base Match Score', placeholder='Input an integer', value='0').props('clearable')
    mismatchPenalty = ui.input(label= 'Mismatch Penalty', placeholder='Input an integer', value='-1').props('clearable')
    
    ui.markdown('''
### Guide

**Gap Penalty**: The amount of points the algorithm awards for a gap. The lower it is the less gaps there will be, should always be negative.

**Match Score**: The amount of points the algorithm awards for a exact match of characters. The higher it is the easier it will be to find alignments, should always be positive.

**Base Match Score**: For DNA sequences, the amount of points awarded when the type of base matches (purines/pyrimidines). Should definitly be lower than the match score. Make it equal to the mismatch score if you are not using a DNA sequence.

**Mismatch Penalty**: The amount of points the algorithm deducts for a mismatch of charactes. The lower it is the harder it will be to find alignments, should always be negative.


''')

with ui.row():
    globalAlignButton = ui.button('Global Alignment')
    localAlignButton = ui.button('Local Alignment')

globalAlignButton.on('click', lambda: alignStringsAndShowPrettyGraphics(True, sequenceOne.value, sequenceTwo.value, gapPenalty.value, matchScore.value, baseMatchScore.value, mismatchPenalty.value))
localAlignButton.on('click', lambda: alignStringsAndShowPrettyGraphics(False, sequenceOne.value, sequenceTwo.value, gapPenalty.value, matchScore.value, baseMatchScore.value, mismatchPenalty.value))

output = ui.row()
ui.run(title='Sequence Alignment')
