### This file is for the big function that will take 2 rs IDs and output the LD measures 

import sqlite3

def LinkageDisequilibrium(rs_ID1, rsID_2):
    '''
    This is a big function. It calculates the LD measures from two rs IDs.
    The population data for the British, Nigerian, and Japanese populations is obtained from .db files.

    Input: two rs IDs.
    Output: a dictionary of all the outputs. r2, D' for each population.  
    '''
    
    ########## 
    # STEP 0
    ##########
    # connecting to the .db files for each population
    # The data in the .db files is Chr6 only, and T1D related SNPs only. 
    

    ### BRITISH population data collection for the specified rs IDs ###
    british_conn = sqlite3.connect('data/british_chr6.db')
    british_cursor = british_conn.cursor()

    british_keys = rs_ID1, rsID_2 

    #creating dictionary to store what is being obtained from db file
    british_chr6 = {key: [] for key in british_keys}

    # loop over the keys and retrieve the values from the corresponding table
    for key in british_keys:
        british_cursor.execute(f"SELECT value FROM {key}")
        values = [row[0] for row in british_cursor.fetchall()]
        british_chr6[key] = values

    # closing connection
    british_conn.close()    

    
    ### NIGERIAN population data collection for the specified rs IDs ###
    nigerian_conn = sqlite3.connect('data/nigerian_chr6.db')
    nigerian_cursor = nigerian_conn.cursor()

    nigerian_keys = rs_ID1, rsID_2 

    #creating dictionary to store what is being obtained from db file
    nigerian_chr6 = {key: [] for key in nigerian_keys}

    # loop over the keys and retrieve the values from the corresponding table
    for key in nigerian_keys:
        nigerian_cursor.execute(f"SELECT value FROM {key}")
        values = [row[0] for row in nigerian_cursor.fetchall()]
        nigerian_chr6[key] = values

    # closing connection
    nigerian_conn.close() 


    ### JAPANESE population data collection for the specified rs IDs ###
    japanese_conn = sqlite3.connect('data/japanese_chr6.db')
    japanese_cursor = japanese_conn.cursor()

    japanese_keys = rs_ID1, rsID_2 

    #creating dictionary to store what is being obtained from db file
    japanese_chr6 = {key: [] for key in japanese_keys}

    # loop over the keys and retrieve the values from the corresponding table
    for key in japanese_keys:
        japanese_cursor.execute(f"SELECT value FROM {key}")
        values = [row[0] for row in japanese_cursor.fetchall()]
        japanese_chr6[key] = values

    # closing connection
    japanese_conn.close() 

    

    ##########
    # STEP 1
    ##########
    
    # assigning the list of genotypes of the two rsIDs, for the BRITISH population
    british_genotype_list_1 = british_chr6[rs_ID1]
    british_genotype_list_2 = british_chr6[rsID_2]

     # assigning the list of genotypes of the two rsIDs, for the NIGERIAN population
    nigerian_genotype_list_1 = nigerian_chr6[rs_ID1]
    nigerian_genotype_list_2 = nigerian_chr6[rsID_2]

    # assigning the list of genotypes of the two rsIDs, for the JAPANESE population
    japanese_genotype_list_1 = japanese_chr6[rs_ID1]
    japanese_genotype_list_2 = japanese_chr6[rsID_2]

    
    ##########
    # STEP 2
    ##########
    # function that obtains the haplotypes of the two rsIDs
    def determine_haplotype(genotype_list_1, genotype_list_2):
        '''Function compares alleles of each individual and determines their haplotype
        '''
        result = []
        for i in range(len(genotype_list_1)):
            genotype1 = genotype_list_1[i].split("|")
            genotype2 = genotype_list_2[i].split("|")
            gt1 = int(genotype1[0])
            gt2 = int(genotype2[0])
            gt3 = int(genotype1[1])
            gt4 = int(genotype2[1])
            if gt1 == 0 and gt2 == 0:
                result.append("00")
            elif gt1 == 0 and gt2 == 1:
                result.append("01")
            elif gt1 == 1 and gt2 == 0:
                result.append("10")
            elif gt1 == 1 and gt2 == 1:
                result.append("11")
            else:
                result.append("N/A")
            if gt3 == 0 and gt4 == 0:
                result.append("00")
            elif gt3 == 0 and gt4 == 1:
                result.append("01")
            elif gt3 == 1 and gt4 == 0:
                result.append("10")
            elif gt3 == 1 and gt4 == 1:
                result.append("11")
            else:
                result.append("N/A")
        return result

    # printing out the haplotype counts from the queried rsID1 and rsID2
    british_haplotypes = determine_haplotype(british_genotype_list_1, british_genotype_list_2)
    nigerian_haplotypes = determine_haplotype(nigerian_genotype_list_1, nigerian_genotype_list_2)
    japanese_haplotypes = determine_haplotype(japanese_genotype_list_1, japanese_genotype_list_2)


    ##########
    # STEP 3
    ##########
    # counting the haplotypes 
    def count_haplotypes(compare_genotypes):
        '''Function counts how many of each haplotype exist
        The 00 is PA PB alleles (so reference, reference for each rsID)
        01 is PA Pb alleles
        10 is Pa PB alleles
        11 is Pa Pb alleles
        This is only possible because the vcf files I used had phased data.
        '''
        count_dict = {'00': 0, '01': 0, '10': 0, '11': 0}
        for genotype in compare_genotypes:
            count_dict[genotype] += 1
        return count_dict

    british_haplotypes_count = count_haplotypes(british_haplotypes)
    nigerian_haplotypes_count = count_haplotypes(nigerian_haplotypes)
    japanese_haplotypes_count = count_haplotypes(japanese_haplotypes)


    ##########
    # STEP 4
    ##########
    # calculating PA, PB, PAB frequencies needed for the LD calculation 
    def count_PA_PB_PAB_british(haplotype_counts):
        '''
        Function obtains the PA, PB, PAB allele frequencies needed for r^2 and D' calculations
        In this case, I'm dividing the frequencies by the total individuals in the population
        The British population we used had 100 individuals, so 200 alleles
        '''
        count_dict = {'PA': 0, 'PB': 0, 'PAB': 0}
        total = 200 
        count_dict['PA'] = (haplotype_counts['00']+haplotype_counts['01'])/total
        count_dict['PB'] = (haplotype_counts['00']+haplotype_counts['10'])/total
        count_dict['PAB'] = (haplotype_counts['00'])/total

        return count_dict

    def count_PA_PB_PAB_nigerian(haplotype_counts):
        '''
        Function obtains the PA, PB, PAB allele frequencies needed for r^2 and D' calculations
        In this case, I'm dividing the frequencies by the total individuals in the population
        The Nigerian population we used had 100 individuals, so 200 alleles
        '''
        count_dict = {'PA': 0, 'PB': 0, 'PAB': 0}
        total = 200 
        count_dict['PA'] = (haplotype_counts['00']+haplotype_counts['01'])/total
        count_dict['PB'] = (haplotype_counts['00']+haplotype_counts['10'])/total
        count_dict['PAB'] = (haplotype_counts['00'])/total

        return count_dict

    def count_PA_PB_PAB_japanese(haplotype_counts):
        '''
        Function obtains the PA, PB, PAB allele frequencies needed for r^2 and D' calculations
        In this case, I'm dividing the frequencies by the total individuals in the population
        The Japanese population we used had 105 individuals, so 210 alleles
        '''
        count_dict = {'PA': 0, 'PB': 0, 'PAB': 0}
        total = 210 
        count_dict['PA'] = (haplotype_counts['00']+haplotype_counts['01'])/total
        count_dict['PB'] = (haplotype_counts['00']+haplotype_counts['10'])/total
        count_dict['PAB'] = (haplotype_counts['00'])/total

        return count_dict

    # Assigning the frequencies PA, PB, PBA for each population
    british_loci_frequencies = count_PA_PB_PAB_british(british_haplotypes_count)
    nigerian_loci_frequencies = count_PA_PB_PAB_nigerian(nigerian_haplotypes_count)
    japanese_loci_frequencies = count_PA_PB_PAB_japanese(japanese_haplotypes_count)


    ##########
    # STEP 5
    ##########
    # calculating LD from the frequencies calculated above
    def LD_D_function(PA, PB, PAB):
        '''
        Function that calculates D
        This is only dependent on what alleles were chosen for PA, PB, Pa, Pb. 
        '''
        D = PAB - (PA * PB)
        return D

    # Assigning the D for each population
    british_LD = LD_D_function(british_loci_frequencies['PA'], british_loci_frequencies['PB'], british_loci_frequencies['PAB'])
    nigerian_LD = LD_D_function(nigerian_loci_frequencies['PA'], nigerian_loci_frequencies['PB'], nigerian_loci_frequencies['PAB'])
    japanese_LD = LD_D_function(japanese_loci_frequencies['PA'], japanese_loci_frequencies['PB'], japanese_loci_frequencies['PAB'])


    ##########
    # STEP 6
    ##########
    # calculating r^2 from D
    def calculate_r_squared(D, pA, pB):
        '''
        Function calculates the r^2, which is a measure of D. It measures the correlation.
        '''
        try:
            r_squared = (D ** 2) / (pA * (1 - pA) * pB * (1 - pB))
        except ZeroDivisionError:
            r_squared = 0.0
        
        return r_squared


    # calculating the r^2 for each population
    british_r2 = calculate_r_squared(british_LD, british_loci_frequencies['PA'], british_loci_frequencies['PB'])
    nigerian_r2 = calculate_r_squared(nigerian_LD, nigerian_loci_frequencies['PA'], nigerian_loci_frequencies['PB'])
    japanese_r2 = calculate_r_squared(japanese_LD, japanese_loci_frequencies['PA'], japanese_loci_frequencies['PB'])


    ##########
    # STEP 6
    ##########
    # calculating D' from D
    def D_prime(D, PA, PB):
        '''
        Function for calculating D' measurement of Linkage Disequilibrium. 
        Function takes D, PA and PB calculated previously. 
        The equation for D' is D / Dmax. Dmax is calculated differently for D>0 and D<0.
        '''
        try: 
            if D > 0:
                Dmax = min(PA*(1-PB), (1-PA)*PB)
            else:
                Dmax = max(-abs(PA)*PB, -abs((1-PA)*(1-PB)))
            D_prime = D / Dmax
        except ZeroDivisionError:
            D_prime = 0.0 

        return D_prime

    # Calculating D' for each population
    british_dprime = D_prime(british_LD, british_loci_frequencies['PA'], british_loci_frequencies['PB'])
    nigerian_dprime = D_prime(nigerian_LD, nigerian_loci_frequencies['PA'], nigerian_loci_frequencies['PB'])
    japanese_dprime = D_prime(japanese_LD, japanese_loci_frequencies['PA'], japanese_loci_frequencies['PB'])


    # The results of this big function is a dictionary of all the possible needed calculations/results
    results = {'rsID_1': rs_ID1, 'rsID_2': rsID_2,
                'british_haplotypes': british_haplotypes_count, 'nigerian_haplotypes': nigerian_haplotypes_count, 'japanese_haplotypes': japanese_haplotypes_count, 
                'british_pA':  british_loci_frequencies['PA'], 'british_pB': british_loci_frequencies['PB'], 'british_pAB': british_loci_frequencies['PAB'],
                'nigerian_pA':  nigerian_loci_frequencies['PA'], 'nigerian_pB': nigerian_loci_frequencies['PB'], 'nigerian_pAB': nigerian_loci_frequencies['PAB'],
                'japanese_pA':  japanese_loci_frequencies['PA'], 'japanese_pB': japanese_loci_frequencies['PB'], 'japanese_pAB': japanese_loci_frequencies['PAB'],
                'british_D': british_LD, 'nigerian_D': nigerian_LD, 'japanese_D': japanese_LD,
                'british_r2': british_r2, 'nigerian_r2': nigerian_r2, 'japanese_r2': japanese_r2,
                'british_Dprime': british_dprime, 'nigerian_Dprime': nigerian_dprime, 'japanese_Dprime': japanese_dprime}

    return results

