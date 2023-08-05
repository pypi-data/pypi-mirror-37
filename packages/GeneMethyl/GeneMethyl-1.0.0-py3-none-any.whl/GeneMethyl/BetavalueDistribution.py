import os
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot
matplotlib.pyplot.style.use('ggplot')

import seaborn as sns

def DrawDensityPlot(disease, roughness_cutoff, whether_histogram) :

    def GetOnlyValidBetavalueRow(line, length) :

        betavalue_row = []
        for k in range(length) :
            if(line[k] == "NA") : continue
            betavalue_row.append(float(line[k]))

        return betavalue_row

    input_tumor = open(disease + ".DNA_methylation_450K.tsv", 'r')
    input_tumor.readline() # sample line

    section_summation = [0 for i in range(int(1 / roughness_cutoff) + 1)]

    while(True) :

        line1 = input_tumor.readline().replace("\t\n", "\tNA\n").replace("\t\t", "\tNA\t").replace("\t\t", "\tNA\t").split()
        if(len(line1) == 0) : break
        
        site_id = line1.pop(0)

        betavalue_row = GetOnlyValidBetavalueRow(line1, len(line1)) # getting betavalue for each cpg site
        for value in betavalue_row : section_summation[int(value / roughness_cutoff)] += 1

    path = os.pwd() + "/Result"
    if not os.path.exists("Result/DistributionPlot") : os.mkdir("Result/DistributionPlot")

    sns.set()
    sns.distplot(section_summation, kde = True, hist = whether_histogram)

    matplotlib.pyplot.title(disease + " Betavalue Distribution Plot")
    matplotlib.pyplot.xlabel("Betavalue")
    matplotlib.pyplot.grid(True)
    figure = matplotlib.pyplot.gcf()
    matplotlib.pyplot.show()
    
    figure.savefig(path + "/DistributionPlot/" + disease + ".Betavalue.Distribution.Plot.pdf")

    return section_summation

#roughness_cutoff = float(0.001)
#disease = "PANCANCER"
#whether_histogram = True
#Draw(disease, roughness_cutoff, True)
