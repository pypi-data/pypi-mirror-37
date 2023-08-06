# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 11:56:11 2018
@author: samantha
"""

import os
import csv                                                                                                        
import pysam  
import collections
import matplotlib.pyplot as plt
import random

from termcolor import colored
from colorama import init # use Colorama to make Termcolor work on Windows too

import click

###############################################################################

def load_taxondump(idpath):
    """Importing the Acidobacteria taxon IDs"""
    taxons = {}
    with open(idpath) as csvfile:
        reader = csv.reader(csvfile, delimiter=',') 
        for row in reader:
            taxons[row[1]] = row[0]
        return taxons

def taxon_file(taxdumptype):
    while "ALL" not in taxdumptype and "U" not in taxdumptype:
        print("Error...")
        taxdumptype = input("Input here ('ALL' or 'U')?: ")
    if taxdumptype == "ALL":
        idpath = os.path.dirname(__file__)+"/input/acido_taxid_all.csv"
        taxons = load_taxondump(idpath) 
    if taxdumptype == "U":
        idpath = os.path.dirname(__file__)+"/input/acido_taxid_unclassified.csv"
        taxons = load_taxondump(idpath) 
    return taxons

###############################################################################
# Kaiju input and Acidobacteria read outputs

def insert_csv(kaijufile):
    """Inserting the CSV file of your results and returning a dictionary of them."""
    dict_seqid_taxon = {}
    with open(kaijufile) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if row[1] not in dict_seqid_taxon:
                dict_seqid_taxon[row[1]] = { "reads": [] }     
            dict_seqid_taxon[row[1]]["reads"].append(row[0])
    return dict_seqid_taxon # above swaps over the columns and avoids the duplicates

def percentage(part, whole):
    """Calculating the coverage of Acidobacteria reads from the set of sequences."""
    return 100 * float(part)/float(whole)

###############################################################################
# ACGT comparisons

def list_of_sequences(fasta): # list of sequences, e.g. ['ACACCT', 'TAGC']
    reads = []
    for read in fasta.references:
        reads.append(fasta.fetch(read))
    return reads


def calculate_at(read):
    """Returns AT count."""
    return (read.lower().count("a") + read.lower().count("t")) / len(read) * 100.0
def calculate_gc(read):
    """Returns GC count."""
    return (read.lower().count("g") + read.lower().count("c")) / len(read) * 100.0

def plot_hist(myDict, style, taxdumptype): 
    plt.style.use(style)
    #max_read = int(max(myDict.values()))
    #min_read = int(min(myDict.values())) # random.randint(min_read, max_read)
        
    plt.hist(myDict.values(), bins=1000) 
    plt.xlabel('Ratio')   
    plt.ylabel('Count')
    
    meanDict = (sum(myDict.values())/float(len(myDict.values())))
    plt.axvline(x=meanDict, color='k')
    plt.text(x=(meanDict+1), y=(random.randint(20, 200)), s=str("%.2f" % meanDict))

    if taxdumptype == "U":
        ttype = "unclassified"
        plt.title('Histogram of ACGT for a collection of\n%s Acidobacteria sequences' % (ttype))
    elif taxdumptype == "ALL":
        ttype = "all"
        plt.title('Histogram of ACGT for a collection of\nAcidobacteria sequences')

    plt.grid(True)
    plt.savefig('acgt-comparison_%s_style-%s.png' % (ttype, str(style)))

###############################################################################
# GC ratio

def plot_hist_gc(myDict, style, ph, plottype, taxdumptype): 
    """Returns a plot of the GC ratio for a series of Acidobacteria sequences. 
    Includes the averages of the subdivisions based on the pH number."""
    plt.style.use(style) 
    ph = float(ph)
    
    plt.hist(myDict.values(), bins=1000, color="grey") 
    plt.xlabel('GC Ratio')   
    plt.ylabel('Count')  
    
    if plottype == "line": # mean GC
        lowph = {
            "sub1":58,
            "sub2":57.5,
            "sub3":59,
            "sub13":58.5
        }
        highph = {
            "sub4":60.12,
            "sub6":67.5,
            "sub22":67
        }
        medph = {
            "sub5":65.43, # medium
            "sub8":66.84, # medium
            "sub23":63 # medium
        } 
        colours = ['b', 'r', 'y', 'g']
        if ph < 5:
            for si, sub in enumerate(lowph):
                plt.axvline(lowph[sub], color=colours[si])
                plt.text(x=(lowph[sub]+0.5), y=(random.randint(20, 200)), s=str(sub), color=colours[si])
        elif ph > 5:
            for si, sub in enumerate(highph):
                plt.axvline(highph[sub], color=colours[si])
                plt.text(x=(highph[sub]+0.5), y=(random.randint(20, 200)), s=str(sub), color=colours[si])
        elif ph == 5:
            for si, sub in enumerate(medph):
                plt.axvline(medph[sub], color=colours[si])
                plt.text(x=(medph[sub]+0.5), y=(random.randint(20, 200)), s=str(sub), color=colours[si])    
                
    elif plottype == "span": # span of GC 
        if ph < 5:
            plt.axvspan(35.18, 67.1, alpha=0.25, color='green') # 1 
            plt.text(x=(35.18), y=(random.randint(20, 200)), s="sub1", color='green')
            plt.axvspan(57, 58, alpha=0.25, color='yellow') # 2 
            plt.text(x=(57.5), y=(random.randint(20, 200)), s="sub2", color='yellow')
            plt.axvspan(51, 73.35, alpha=0.25, color='red') # 3
            plt.text(x=(51), y=(random.randint(20, 200)), s="sub3", color='red')
            plt.axvspan(58, 59, alpha=0.25, color='blue') # 13
            plt.text(x=(58), y=(random.randint(20, 200)), s="sub13", color='blue')
        elif ph > 5:
            plt.axvspan(50, 61, alpha=0.25, color='blue') # 4 
            plt.text(x=(50), y=(random.randint(20, 200)), s="sub4", color='blue')
            plt.axvspan(67, 68, alpha=0.25, color='darkgreen') # 6 
            plt.text(x=(67), y=(random.randint(20, 200)), s="sub6", color='green')
            plt.axvspan(66, 67.5, alpha=0.25, color='pink') # 22 
            plt.text(x=(66), y=(random.randint(20, 200)), s="sub22", color='red')
        elif ph == 5:
            plt.axvspan(62.3, 68.3, alpha=0.25, color='red') # 5
            plt.text(x=(62.5), y=(random.randint(20, 200)), s="sub5", color='red')
            plt.axvspan(55.14, 71.83, alpha=0.25, color='pink') # 8
            plt.text(x=(55.5), y=(random.randint(20, 200)), s="sub8", color='pink')
            plt.axvspan(62, 64, alpha=0.25, color='orange') # 23        
            plt.text(x=(62), y=(random.randint(20, 200)), s="sub23", color='orange')
    if taxdumptype == "U":
        ttype = "unclassified"
        plt.title('Histogram of GC ratio of pH%.2f for a\ncollection of %s Acidobacteria sequences' % (ph, ttype))
    elif taxdumptype == "ALL":
        ttype = "all"
        plt.title('Histogram of GC ratio of pH%.2f for a\ncollection of Acidobacteria sequences' % (ph))
    plt.savefig('gc-ratio_%s_ph%.2f_plot-%s_style-%s.png' % (ttype, ph, plottype, style))

###############################################################################
# Subdivisions

def output_sub(taxdumptype, ph, gc_dict, fasta):
    ph = float(ph)
    p = str(ph)
    s = list(p)
    s[1] = '-'
    newph = "".join(s)
    
    sub1 = [35.18, 52, 53, 57, 59, 63] # low 
    sub2 = [57, 58]
    sub3 = [52, 53, 63, 73.35]
    sub13 = [58, 63]
    #sub12 = 63 # < 
    sub4 = [50.5, 64] # high
    sub6 = [67, 68]
    sub22 = [64, 67]
    #subHo = [50, 60, 64, 68] # 7, 10, 11, 14, 16, 17, 18, 25
    sub5 = [64, 70] # med
    sub8 = [55.14, 62, 70, 71.83]
    sub23 = [62, 64]
            
    sub1seq = {} 
    sub2seq = {}   
    sub3seq = {} 
    sub13seq = {} 
    #sub12seq = {}      
    sub4seq = {} 
    sub6seq = {} 
    sub22seq = {} 
    #subHseq = {} # other high   
    sub5seq = {} 
    sub8seq = {} 
    sub23seq = {}     
            
    if taxdumptype == "ALL":
        pass
    elif taxdumptype == "U":       
        for key,val in gc_dict.items():
            if ph < 5:    
                if val > sub1[0] and val < sub1[1] or val > sub1[2] and val < sub1[3] or val > sub1[4] and val < sub1[5]:
                    sub1seq[key] = val
                elif val > sub2[0] and val < sub2[1]:         
                    sub2seq[key] = val
                elif val > sub3[0] and val < sub3[1] or val > sub3[2] and val < sub3[3]: 
                    sub3seq[key] = val
                elif val > sub13[0] and val < sub13[1]: 
                    sub13seq[key] = val
                #elif val > sub12[0]: 
                #    sub12seq[key] = val
            elif ph > 5:     
                if val > sub4[0] and val < sub4[1]: 
                    sub4seq[key] = val
                elif val > sub6[0] and val < sub6[1]: 
                    sub6seq[key] = val
                elif val > sub22[0] and val < sub22[1]: 
                    sub22seq[key] = val
                #elif val < subHo[0] or (val > subHo[1] and val < subHo[2]) or val > subHo[3]: # others
                #    subHseq[key] = val
            elif ph == 5:
                if val > sub5[0] and val < sub5[1]: 
                    sub5seq[key] = val
                elif val > sub8[0] and val < sub8[1] or val > sub8[2] and val < sub8[3]: 
                    sub8seq[key] = val
                elif val > sub23[0] and val < sub23[1]: 
                    sub23seq[key] = val

        if ph < 5:
            seq = []
            print("Creating file for subdivision 1")
            opath = ("sub1_%s_ph%s.fasta" % (taxdumptype, newph))     
            with open(opath, "w") as output:
                for r in sub1seq:      
                    seq = fasta.fetch(reference=r)              
                    output.write(">%s\n%s\n" % (r, seq))
            seq = []
            print("Creating file for subdivision 2")
            opath = ("sub2_%s_ph%s.fasta" % (taxdumptype, newph))     
            with open(opath, "w") as output:
                for r in sub2seq:                    
                    seq = fasta.fetch(reference=r)
                    output.write(">%s\n%s\n" % (r, seq))
            seq = []
            print("Creating file for subdivision 3")
            opath = ("sub3_%s_ph%s.fasta" % (taxdumptype, newph))     
            with open(opath, "w") as output:
                for r in sub3seq:                    
                    seq = fasta.fetch(reference=r)
                    output.write(">%s\n%s\n" % (r, seq))
            seq = []
            print("Creating file for subdivision 13")
            opath = ("sub13_%s_ph%s.fasta" % (taxdumptype, newph))     
            with open(opath, "w") as output:
                for r in sub13seq:                    
                    seq = fasta.fetch(reference=r)
                    output.write(">%s\n%s\n" % (r, seq))
            #opath = ("sub12_%s_ph%s.fasta" % (taxdumptype, newph))     
            #with open(opath, "w") as output:
            #    for r in sub12seq:                    
            #        output.write("%s\n" % (r))
        elif ph > 5:
            seq = []
            print("Creating file for subdivision 4")
            opath = ("sub4_%s_ph%s.fasta" % (taxdumptype, newph))     
            with open(opath, "w") as output:
                for r in sub4seq:   
                    seq = fasta.fetch(reference=r)                 
                    output.write(">%s\n%s\n" % (r, seq))
            seq = []
            print("Creating file for subdivision 6")
            opath = ("sub6_%s_ph%s.fasta" % (taxdumptype, newph))     
            with open(opath, "w") as output:
                for r in sub6seq:
                    seq = fasta.fetch(reference=r)                    
                    output.write(">%s\n%s\n" % (r, seq))
            seq = []
            print("Creating file for subdivision 22")
            opath = ("sub22_%s_ph%s.fasta" % (taxdumptype, newph))     
            with open(opath, "w") as output:
                for r in sub22seq:      
                    seq = fasta.fetch(reference=r)              
                    output.write(">%s\n%s\n" % (r, seq))           
            #opath = ("sub7-10-11-14-16-17-18-25_%s_ph%s.fasta" % (taxdumptype, newph))     
            #with open(opath, "w") as output:
            #    for r in subHseq:                    
            #        output.write("%s\n" % (r))
        elif ph == 5:
            seq = []
            print("Creating file for subdivision 5")
            opath = ("sub5_%s_ph%s.fasta" % (taxdumptype, newph))     
            with open(opath, "a") as output:
                for r in sub5seq:                    
                    seq = fasta.fetch(reference=r) 
                    output.write(">%s\n%s\n" % (r, seq))
            seq = []
            print("Creating file for subdivision 8")
            opath = ("sub8_%s_ph%s.fasta" % (taxdumptype, newph))     
            with open(opath, "a") as output:
                for r in sub8seq:                    
                    seq = fasta.fetch(reference=r) 
                    output.write(">%s\n%s\n" % (r, seq))
            seq = []
            print("Creating file for subdivision 23")
            opath = ("sub23_%s_ph%s.fasta" % (taxdumptype, newph))     
            with open(opath, "a") as output:
                for r in sub23seq:                    
                    seq = fasta.fetch(reference=r) 
                    output.write(">%s\n%s\n" % (r, seq))

###############################################################################

@click.command()
@click.option('--taxdumptype', default='ALL', help='Study "ALL" or only unclassified "U"?')
@click.option('--kaijufile', help='Place edited Kaiju (csv) in directory for ease.')
@click.option('--fastapath', help='Place FASTA in directory for ease.')
@click.option('--style', default='NONE', help="['seaborn-bright', 'seaborn-poster', 'seaborn-white', 'bmh', 'seaborn-darkgrid', 'seaborn-pastel', 'grayscale', '_classic_test', 'ggplot', 'seaborn-whitegrid', 'seaborn-dark', 'seaborn-muted', 'seaborn-colorblind', 'seaborn-ticks', 'Solarize_Light2', 'seaborn-notebook', 'dark_background', 'fast', 'seaborn', 'fivethirtyeight', 'seaborn-paper', 'seaborn-dark-palette', 'seaborn-talk', 'classic', 'seaborn-deep']")
@click.option('--plottype', default='line', help='"span" range of GC means OR "line" average mean GC')
@click.option('--ph', default='5', help='pH of soil, use map script for assistance.')
def main(taxdumptype, kaijufile, fastapath, style, plottype, ph):
    colors = ["cyan", "yellow", "magenta", "blue", "green"]
    ph = float(ph)
    
    taxons = taxon_file(taxdumptype) # ALL/U
    taxon_read_map = insert_csv(kaijufile) # KAIJU
    
    has_taxon = 0
    total_reads = 0
    numrec = 0
    acido_reads = []
    
    for taxon_id in taxon_read_map:
        numrec += 1
        total_reads += len(taxon_read_map[taxon_id]["reads"])
        print("Record\t%s" % (str(numrec)))
        try:
            taxon_read_map[taxon_id]["scientific_name"] = taxons[taxon_id]
            has_taxon += len(taxon_read_map[taxon_id]["reads"])
            acido_reads.extend(taxon_read_map[taxon_id]["reads"])
        except KeyError:
            continue
    
    if taxdumptype == "ALL":
        print(colored('\nAcidobacteria coverage of file:', colors[0])) 
        acido_coverage = percentage(has_taxon, total_reads)
        print("%.2f%%" % (acido_coverage))
    elif taxdumptype == "U":
        print(colored('\nUnclassified Acidobacteria coverage of file:', colors[0])) 
        acido_coverage = percentage(has_taxon, total_reads)
        print("%.2f%%" % (acido_coverage))

############################################
    #FASTA
    fasta = pysam.FastaFile(fastapath) # FASTA
    output_acido_file = ("acido_%s_reads.fa" % (taxdumptype))
    with open(output_acido_file, "w") as output:
        for r in acido_reads:                                                                                                
            seq = fasta.fetch(reference=r) 
            output.write(">%s\n%s\n" % (r, seq))
    print(colored("\nSuccessful! The file name:", colors[1])) 
    print("%s" % (output_acido_file))
    
############################################
    # ACGT comparisons 
    
    out_path = output_acido_file
    fasta = pysam.FastaFile(out_path) 

    reads = list_of_sequences(fasta)   
    #max_read = len(max(reads, key=len))
    #min_read = len(min(reads, key=len))
    lens = [len(x) for x in reads]
    max_read = max(lens)
    min_read = min(lens)
    
    print(colored("\nStatistics:", colors[2]))
    print("Read Lengths\tMin: %d\tMax: %d" % (min_read, max_read))
    
    at = {}
    gc = {}
    for read in fasta.references:
        at[read] = calculate_at(fasta.fetch(read))  
        gc[read] = calculate_gc(fasta.fetch(read))
    max_at = max(at.values())
    min_at = min(at.values())  
    mean_at = (sum(at.values())/float(len(at.values())))
    print("AT\tMin: %f\tMax: %f\tMean: %f" % (min_at, max_at, mean_at))
    max_gc = max(gc.values())
    min_gc = min(gc.values())  
    mean_gc = (sum(gc.values())/float(len(gc.values())))
    print("GC\tMin: %f\tMax: %f\tMean: %f" % (min_gc, max_gc, mean_gc))

############################################

    styles = plt.style.available
    try:
        plt.style.use(style)
    except OSError:
        print("\nStyle unrecognised, automatically choosing one for you...")
        style_int = random.randint(0,24)
        style = styles[style_int]
    
    x = 1
    plt.figure(x)    
    plot_hist(at, style, taxdumptype)
    plot_hist(gc, style, taxdumptype)
    
############################################
    # GC ratio
    
    x = 2
    plt.figure(x)    
    plot_hist_gc(gc, style, ph, plottype, taxdumptype)
    
############################################
    # Subdivisions  

    if taxdumptype == "ALL":
        pass
    elif taxdumptype == "U":
        print(colored("\nExporting sequences into files of subdivisions based on pH...", colors[3]))

    output_sub(taxdumptype, ph, gc, fasta)
    
############################################

    print(colored("\nAll Done!\n", colors[4]))
    
###############################################################################
###############################################################################
###############################################################################

if __name__ == "__main__":
    main()    
