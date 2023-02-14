### This file contains the code to extract genotype and haplotype information from the 
### British vcf file obtained from ISGR. The file is called 'British_filled_in_IDs.vcf'
### because I have populated the ID column which was originally empty. The file also 
### only contains the rsIDs that are relevant for T1D (obtained from the GWAS data)

### this code is a first draft, as of 14 Feb 2023. There are still lots of print() 
### to be remove and probably more comments to add.
### also I will slightly change some names of the functions




# function that gets the genotype list 
def get_genotype_list(vcf_file, snp_id):
  '''Function reads the file, and obtains the data from the row of the rsID specified
  '''
  with open(vcf_file, "r") as f:
      for line in f:
          if line.startswith("#"):
              continue
          fields = line.strip().split("\t")
          if fields[2] == snp_id:
              genotype_list = fields[9:]
              return genotype_list
  return []

# printing out the genotypes list for rs ID 1
genotype_list_1 = get_genotype_list("/Users/martadelfino/Documents/group_project/vcfs/British_filled_in_IDs.vcf", "rs1050979")
print(genotype_list_1)

# printing out the genotypes list for rs ID 2
genotype_list_2 = get_genotype_list("/Users/martadelfino/Documents/group_project/vcfs/British_filled_in_IDs.vcf", "rs9405661")
print(genotype_list_2)



def compare_genotypes(genotype_list_1, genotype_list_2):
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

# printing out the haplotype counts from the queried rsID 1 and rsID2
compared_genotypes = compare_genotypes(genotype_list_1, genotype_list_2)
print(compared_genotypes)


def count_haplotypes(compare_genotypes):
  '''Function counts how many of each haplotype exist
  The 00 is PA PB alleles (so reference reference for each rsID)
  01 is PA Pb allelss
  10 is Pa PB alleles
  11 is Pa Pb alleles
  This is only possible because the vcf files I used had phased data.
  '''
  count_dict = {'00': 0, '01': 0, '10': 0, '11': 0}
  for genotype in compare_genotypes:
      count_dict[genotype] += 1
  return count_dict

counting_haplotypes = count_haplotypes(compared_genotypes)
print(counting_haplotypes)




def count_PA_PB_PAB(counting_haplotypes_freq):
  '''Function obtains the PA, PB, PAB allele frequencies needed for r^2 and D' calculations
  In this case, I'm dividing the frequencies by the total individuals in the population
  The British population we used had 100 individuals
  '''
  count_dict = {'PA': 0, 'PB': 0, 'PAB': 0}
  total = 100 # will need to update this, different for each population. 
  count_dict['PA'] = (counting_haplotypes_freq['00']+counting_haplotypes_freq['01'])/total
  count_dict['PB'] = (counting_haplotypes_freq['10']+counting_haplotypes_freq['11'])/total
  count_dict['PAB'] = (counting_haplotypes_freq['00'])/total

  return count_dict

# printing PA, PB, PBA
frequencies = count_PA_PB_PAB(counting_haplotypes)
print(frequencies)


def LD_D_function(PA, PB, PAB):
  '''Function that calculates D
  This is only dependent on what alleles were chosen for PA, PB, Pa, Pb. 
  '''
  D = PAB - (PA * PB)
  return D

# printing the D
LD = LD_D_function(frequencies['PA'], frequencies['PB'], frequencies['PAB'])
print(LD)

def calculate_r_squared(D, pA, pB):
  '''Function calculates the r^2, which is a measure of D. It measures the correlation.'''
  r_squared = (D ** 2) / (pA * (1 - pA) * pB * (1 - pB))
  return r_squared

# printing the R^2
r2 = calculate_r_squared(LD, frequencies['PA'], frequencies['PB'])
print(r2)


# next steps are to calculate D'