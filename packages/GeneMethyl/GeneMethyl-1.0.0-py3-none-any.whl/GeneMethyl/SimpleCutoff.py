import os
import numpy
import math
from scipy import stats

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot
import matplotlib.pylab

matplotlib.pyplot.style.use('ggplot')

sample_id = []
cytoact = []

path = os.getcwd() + "/Result/SimpleCutoff"
        
def TargetGeneActivity(disease, target_gene) :

    if not os.path.exists(disease + ".RNAseq.tsv") :
        print("Error : " + disease + ".RNAseq.tsv is not found.")
        return False
        
    RNAseq_file = open(disease + ".RNAseq.tsv", 'r')
    gene_score_file = open(path + "/" + disease + ".TargetGeneActivity.txt", 'w')

    gene_length = len(target_gene)

    header = RNAseq_file.readline().split()[1:]
    sample_length = len(header)
    for i in range(sample_length) : header[i] = header[i].replace('"', '')

    expression_level = numpy.zeros((sample_length, len(target_gene)), dtype = float)
    gene_check = [False for i in range(len(target_gene))]

    while(True) : 
        line = RNAseq_file.readline().replace("\t\n", "\tNA\n").replace("\t\t", "\tNA\t").replace("\t\t", "\tNA\t").split()
        if(len(line) == 0) : break

        gene_id = line.pop(0).replace('"', '')
        if(gene_id.find('|') != -1) : gene_id = gene_id[:gene_id.index('|')]

        if(gene_id in target_gene) :
            gene_check[target_gene.index(gene_id)] = True
            gene_index = target_gene.index(gene_id)
            for i in range(len(line)) : expression_level[i][gene_index] = float(line[i])
            
    if(False in gene_check) :
    
        missing_gene = []
        for i in range(len(target_gene)) :
            if(gene_check[i] == False) : missing_gene.append(target_gene[i])
            
        if(len(missing_gene) == 1) : print("Error : " + " ".join(missing_gene) + " gene is not found in " + disease + ".RNAseq.tsv.")
        else : print("Error : " + " ".join(missing_gene) + " genes are not found in " + disease + ".RNAseq.tsv.")
        
        return False 

    gene_score_file.write("Sample\t" + "\t".join(target_gene) + "\tPseudocount1_Activity(log)" + "\n")

    pseudocount_score = []
    for i in range(sample_length) :
        if(len(target_gene) != 1) :
            pseudocount_score.append(math.log(sum(expression_level[i]) + gene_length, gene_length))
            gene_score_file.write(header[i] + "\t" + "\t".join(map(str, expression_level[i])) + "\t" + str(pseudocount_score[i]) + "\n")

        else :
            pseudocount_score.append(expression_level[i][0] + 1)
            gene_score.write(header[i] + "\t" + str(expression_level[i][0]) + "\t" + "\t" + str(pseudocount_score[i]) + "\n")
            
    return True

def View_Correlation_AND_ScatterPlot(disease, gene_name, cutoff, Type, whether_FoldChange) :

    if not os.path.exists("Result/SimpleCutoff") : os.makedirs(path)
    if not os.path.exists("Result/SimpleCutoff/FC_CpGsites") and whether_FoldChange == True : os.makedirs(path + "/FC_CpGsites")
    if not os.path.exists("Result/SimpleCutoff/Summation") : os.makedirs(path + "/Summation")
    if not os.path.exists("Result/SimpleCutoff/ScatterPlot") : os.makedirs(path + "/ScatterPlot")
    if not os.path.exists("Result/SimpleCutoff/Correlation") : os.makedirs(path + "/Correlation")
    
    if(Type not in ["Lower", "Higher", "Both", "All"]) :
        print("Error : Type %s is not valid. Valid Types are Lower, Higher, Both and All." % Type)
        return
        
    new_cutoff = []
    for i in range(len(cutoff)) :
        if(cutoff[i] > 1 or cutoff[i] < 0) :
            print("%s cutoff is not valid. Cutoff must be in [0, 1]." % str(cutoff[i]))
            continue
        new_cutoff.append(cutoff[i])
            
    cutoff = new_cutoff
    
    def GetSampleScoreData(disease) :
    
        cytoact_file = open(path + "/" + disease + ".TargetGeneActivity.txt", 'r')
        header = cytoact_file.readline().split() # getting header
    
        id_posit = header.index("Sample") # sample ID positioning
        cytoact_posit = header.index("Pseudocount1_Activity(log)") # CytAct positioning
        cytodata = cytoact_file.readlines() # read data table
        cytoact_file.close()
    
        count = 0
    
        global sample_id
        global cytoact
    
        for line in cytodata :
            line = line.split()
            sample_id.append(line[id_posit].replace('-', '').replace('_', '')[:12]) # sample ID extraction
            cytoact.append(float(line[cytoact_posit])) # CytAct extraction

            count += 1
            
        return count # Sample number return
    
    def MedianInSortedRow(betavalue_row, new_length) :
        
        betavalue_median = betavalue_row[int(new_length / 2)][0]
        if(new_length % 2 == 0) : betavalue_median = (betavalue_median + betavalue_row[int(new_length / 2) - 1][0]) / 2
        
        return betavalue_median

    def GetValidBetavalueRowAndSorted(line, length, sample_index) :

        betavalue_row = []
        new_length = length
        
        for k in range(length) :
            if(line[k] == "NA" or sample_index[k] == -1) :
                new_length -= 1
                continue
            betavalue_row.append([float(line[k]), k])

        betavalue_row.sort(key = lambda x : x[0])

        return betavalue_row, new_length

    def GetSampleHeader(sample_header, length) :

        global sample_id

        sample_index = []
        original_sample_header = []
    
        for j in range(0, length) :
        
            original_sample_header.append(sample_header[j])
            sample_header[j] = sample_header[j].replace('-', '').replace('_', '')[:12]
        
            if(sample_header[j] in sample_id) : sample_index.append(sample_id.index(sample_header[j]))
            else : sample_index.append(-1)
        
        return sample_header, sample_index, original_sample_header
    
    if not os.path.exists(disease + ".DNA_methylation_450K.tsv") :
        print("Error : " + disease + ".DNA_methylation_450K.tsv is not found.")
        return

    input_tumor = open(disease + ".DNA_methylation_450K.tsv", 'r')
        
    MissingCheck = TargetGeneActivity(disease, gene_name)
    if(MissingCheck == False) : return
    
    sample_number = GetSampleScoreData(disease)
    sample_header = input_tumor.readline().split() # sample line

    sample_index = []
    sample_binary_table = []

    length = len(sample_header)

    sample_header, sample_index, original_sample_header = GetSampleHeader(sample_header, length)
    sample_binary_table = numpy.zeros((len(cutoff), 3, length), dtype = int)

    if(whether_FoldChange == True) :

        output_FC_cutoff = []

        for i in range(len(cutoff)) :
            output_FC_cutoff.append([])
            if(Type == "Lower" or Type == "All") :
                output_FC_cutoff[i].append(open(path + "/FC_CpGsites/" + "WholeSites.Cutoff." + str(cutoff[i]) + "." + disease + ".Lower.FC.CpGsites.txt", 'w'))
                output_FC_cutoff[i][0].write("Site\tFC(high_median/low_median)\tFC(high_mean/low_mean)\tP-value\n")
            else : output_FC_cutoff[i].append(None)
                
            if(Type == "Higher" or Type == "All") :
                output_FC_cutoff[i].append(open(path + "/FC_CpGsites/" + "WholeSites.Cutoff." + str(cutoff[i]) + "." + disease + ".Higher.FC.CpGsites.txt", 'w'))
                output_FC_cutoff[i][1].write("Site\tFC(high_median/low_median)\tFC(high_mean/low_mean)\tP-value\n")
            else : output_FC_cutoff[i].append(None)
                
            if(Type == "Both" or Type == "All") :
                output_FC_cutoff[i].append(open(path + "/FC_CpGsites/" + "WholeSites.Cutoff." + str(cutoff[i]) + "." + disease + ".Both.FC.CpGsites.txt", 'w'))
                output_FC_cutoff[i][2].write("Site\tFC(high_median/low_median)\tFC(high_mean/low_mean)\tP-value\n")
            else : output_FC_cutoff[i].append(None)
    
    j = 1
    while(True) :

        line1 = input_tumor.readline().replace("\t\n", "\tNA\n").replace("\t\t", "\tNA\t").replace("\t\t", "\tNA\t").split()
        if(len(line1) == 0) : break

        site_id = line1.pop(0)

        betavalue_row, new_length = GetValidBetavalueRowAndSorted(line1, length, sample_index) # getting betavalue for each cpg site

        if(new_length > 0) :

            if(Type == "Lower" or Type == "All") :
                    
               for cutoff_i in range(len(cutoff)) :

                    breaking_point = new_length
                    for l in range(new_length) :
                            
                        if(betavalue_row[l][0] > cutoff[cutoff_i]) :
                            breaking_point = l
                            break
                            
                        sample_binary_table[cutoff_i][0][betavalue_row[l][1]] += 1
                        
                    if(whether_FoldChange == True) :
                            
                        chosen_cytact = []; notchosen_cytact = []
                            
                        for l in range(breaking_point) : chosen_cytact.append(cytoact[sample_index[betavalue_row[l][1]]])
                        for l in range(breaking_point, new_length) : notchosen_cytact.append(cytoact[sample_index[betavalue_row[l][1]]])

                        FC_median, FC_mean = numpy.median(chosen_cytact) / numpy.median(notchosen_cytact), numpy.mean(chosen_cytact) / numpy.mean(notchosen_cytact)
                        manwhitney_pair = stats.mannwhitneyu(chosen_cytact, notchosen_cytact)
                        
                        output_FC_cutoff[cutoff_i][0].write(site_id + "\t%s\t%s\t%s\n" % (str(FC_median), str(FC_mean), str(manwhitney_pair[1])))        
                    
            if(Type == "Higher" or Type == "All") :
                                    
               for cutoff_i in range(len(cutoff)) :

                    breaking_point = new_length
                    for l in range(new_length) :
                            
                        if(betavalue_row[new_length - l - 1][0] < cutoff[cutoff_i]) :
                            breaking_point = l
                            break
                            
                        sample_binary_table[cutoff_i][1][betavalue_row[new_length - l - 1][1]] += 1
                        
                    if(whether_FoldChange == True) :
                            
                        chosen_cytact = []; notchosen_cytact = []
                            
                        for l in range(breaking_point) : chosen_cytact.append(cytoact[sample_index[betavalue_row[new_length - l - 1][1]]])
                        for l in range(breaking_point, new_length) : notchosen_cytact.append(cytoact[sample_index[betavalue_row[new_length - l - 1][1]]])

                        FC_median, FC_mean = numpy.median(chosen_cytact) / numpy.median(notchosen_cytact), numpy.mean(chosen_cytact) / numpy.mean(notchosen_cytact)
                        manwhitney_pair = stats.mannwhitneyu(chosen_cytact, notchosen_cytact)
                        
                        output_FC_cutoff[cutoff_i][1].write(site_id + "\t%s\t%s\t%s\n" % (str(FC_median), str(FC_mean), str(manwhitney_pair[1])))        

            if(Type == "Both" or Type == "All") :
                
               for cutoff_i in range(len(cutoff)) :

                    breaking_point1 = new_length
                    for l in range(new_length) :
                            
                        if(betavalue_row[l][0] < cutoff[cutoff_i] / 2) :
                            breaking_point = l
                            break
                            
                        sample_binary_table[cutoff_i][2][betavalue_row[l][1]] += 1

                    breaking_point2 = new_length
                    for l in range(new_length) :
                            
                        if(betavalue_row[new_length - l - 1][0] < cutoff[cutoff_i] / 2) :
                            breaking_point2 = l
                            break
                            
                        sample_binary_table[cutoff_i][2][betavalue_row[new_length - l - 1][1]] += 1
                        
                    if(whether_FoldChange == True) :
                            
                        chosen_cytact = []; notchosen_cytact = []

                        for l in range(breaking_point1) : chosen_cytact.append(cytoact[sample_index[betavalue_row[l][1]]])
                        for l in range(breaking_point1, new_length) : notchosen_cytact.append(cytoact[sample_index[betavalue_row[l][1]]])
                            
                        for l in range(breaking_point2) : chosen_cytact.append(cytoact[sample_index[betavalue_row[new_length - l - 1][1]]])
                        for l in range(breaking_point2, new_length) : notchosen_cytact.append(cytoact[sample_index[betavalue_row[new_length - l - 1][1]]])

                        FC_median, FC_mean = numpy.median(chosen_cytact) / numpy.median(notchosen_cytact), numpy.mean(chosen_cytact) / numpy.mean(notchosen_cytact)
                        manwhitney_pair = stats.mannwhitneyu(chosen_cytact, notchosen_cytact)
                        
                        output_FC_cutoff[cutoff_i][2].write(site_id + "\t%s\t%s\t%s\n" % (str(FC_median), str(FC_mean), str(manwhitney_pair[1])))
                        
        if(j % 10000 == 0) : print("%dth sites completed." % j)
        j += 1

    input_tumor.close()
    output_left_skewed.close()
    output_right_skewed.close()

    output_correlation_table = []

    if(Type == "Lower" or Type == "All"):
        output_correlation_table.append(open(path + "/Correlation/" + "WholeSites." + disease + "." + "Lower" + ".Correlation.Summation.And." + "TargetGeneActivity.txt", 'w'))
        output_correlation_table[0].write("Cutoff\tCor\tPvalue\n")
    else : output_correlation_table.append(None)
            
    if(Type == "Higher" or Type == "All") :
        output_correlation_table.append(open(path + "/Correlation/" + "WholeSites." + disease + "." + "Higher" + ".Correlation.Summation.And." + "TargetGeneActivity.txt", 'w'))
        output_correlation_table[1].write("Cutoff\tCor\tPvalue\n")
    else : output_correlation_table.append(None)
        
    if(Type == "Both" or Type == "All") :
        output_correlation_table.append(open(path + "/Correlation/" + "WholeSites." + disease + "." + "Both" + ".Correlation.Summation.And." + "TargetGeneActivity.txt", 'w'))
        output_correlation_table[2].write("Cutoff\tCor\tPvalue\n")
    else : output_correlation_table.append(None)

    correlation_table = []
    correlation_table = numpy.zeros((len(cutoff), 3, 2), dtype = float)

    Type_array = []
    Type_dic = ["Lower", "Higher", "Both"]

    if(Type == "Lower" or Type == "All") : Type_array.append(0)
    if(Type == "Higher" or Type == "All") : Type_array.append(1)
    if(Type == "Both" or Type == "All") : Type_array.append(2)

    for k in range(len(cutoff)) :

        for type_i in range(len(Type_array)) : 
        
            output_file = open(path + "/Summation/" + "WholeSites.Cutoff." + str(cutoff[k]) + "." + disease + "." + Type_dic[type_i] + ".Binarization.Summation.txt", 'w')
            
            header = "Site\t#%sMethylation\tTargetGeneActivity\n" % Type_dic[type_i]
            output_file.write(header)

            summation = []
            cytact = []
        
            for l in range(length) :
                
                if(sample_index[l] == -1) : printline = original_sample_header[l] + "\tNA\tNA\tNA\tNA\n"
                else :
                    printline = original_sample_header[l] + "\t%s\t%s\n" % (str(sample_binary_table[k][Type_array[type_i]][l]), str(cytoact[sample_index[l]]))
                    summation.append(sample_binary_table[k][Type_array[type_i]][l]); cytact.append(cytoact[sample_index[l]])
                output_file.write(printline)
    
            params = {'legend.fontsize': 'x-large',
                      'figure.figsize': (10, 10),
                      'axes.labelsize': 'x-large',
                      'axes.titlesize':'x-large',
                      'xtick.labelsize':'x-large',
                      'ytick.labelsize':'x-large'}
            matplotlib.pylab.rcParams.update(params)
    
            matplotlib.pyplot.hold(False)
            matplotlib.pyplot.xlabel("Summation")
            matplotlib.pyplot.ylabel("".join(gene_name) + "Activity")
            matplotlib.pyplot.legend()
            matplotlib.pyplot.grid(True)
    
            spearman_pair = stats.spearmanr(summation, cytact)
    
            correlation_table[k][Type_array[type_i]][0] = spearman_pair[0]
            correlation_table[k][Type_array[type_i]][1] = spearman_pair[1]
    
            spearman_cor = "{0:.3f}".format(spearman_pair[0])
            spearman_P = "{0:.3f}".format(spearman_pair[1])
    
            matplotlib.pyplot.scatter(summation, cytact, marker = '.', c = 'b')
            matplotlib.pyplot.title(disease + ".WholeSites." + Type_dic[type_i] + ".Cutoff.%s" % str(cutoff[k]) + "   Spearman Cor = %s, P = %s" % (spearman_cor, spearman_P))
            matplotlib.pyplot.hold(True)
            matplotlib.pylab.plot(summation, cytact, '.')
            z = numpy.polyfit(summation, cytact, 1)
            p = numpy.poly1d(z)
            matplotlib.pylab.plot(summation, p(summation), "r--")
        
            figure = matplotlib.pyplot.gcf()
            matplotlib.pyplot.show()
            figure.savefig(path + "/ScatterPlot/" + "WholeSites.Cutoff." + str(cutoff[k]) + "." + disease + "." + Type_dic[type_i] + ".ScatterPlot.pdf")
    
            output_correlation_table[Type_array[type_i]].write("%s" % (str(cutoff[k])) + "\t%f\t%f\n" % (correlation_table[k][Type_array[type_i]][0], correlation_table[k][Type_array[type_i]][1]))

    if(Type == "All") :

        output_compare_table = open(path + "/Correlation/" + "WholeSites." + disease + "." + "CompareAll" + ".Correlation.Summation.And." + "TargetGeneActivity.txt", 'w')
        
        header_compare = "Cutoff"
        for j in range(3) : header_compare += "\t%s\t%s" % (Type_dic[j] + "(Cor)", Type_dic[j] + "(Pvalue)")
        header_compare += "\n"
        output_compare_table.write(header_compare)

        for i in range(len(cutoff)) :
            printline = str(cutoff[i])
            for j in range(3) : printline += "\t%s\t%s" % (str(correlation_table[i][j][0]), str(correlation_table[i][j][1]))
            output_compare_table.write(printline + "\n")

    return sample_binary_table

#target_genes = ["GZMA", "PRF1"]
#cutoff_list = [0.05]
#analysis_type = "All"
#whether_FC_anaylsis = True

#View_Correlation_AND_ScatterPlot("PANCANCER", target_gene, cutoff_list, analysis_type, whether_FC_analysis)
