#2023 Feb 10
#Marta Delfino
#data prep for group project

# My goal is to use the genotype data of the vcf files obtained from IGSR (British GBR, Nigerian ESN, Japanese JPT) to calculate LD.
# The population vcf files were created by Thuvarahgan. He obtained the 1000 Genomes on GRCh38 variant dataset for chromosome 6. 
# Then, I need to filter these population files to only include the T1D related SNPs
# Then, I need to fill in the rs ID column of the files. I can do this using the gen_coords.vcf file obtained from SNPnexus. This file was 
# obtained buy querying the database using the list of T1D related rsIDs. 



# Firstly, I'm working with gen_coords.vcf from SNPnexus. 
# I've zipped the vcf file and indexed it
gzip <file> 
tabix -p vcf input.vcf.gz

# from the vcf file, I've filtered it to only contain chr6, with this command
grep "^6" input.vcf > output.vcf

# I've counted the lines with this command, there are 64 entries. so 64 rs IDs
grep "^6" input.vcf | wc -l

# the file with the genetic coordinates of chr6 is called: gen_coords_chr6_only.vcf



# Then, I use the gen_coords_chr6_only.vcf to filter the population vcfs
230210_filter_vcf_on_position.py

# This creates files called eg. British_filtered_variants.vcf

# Then I need to populate the rs ID columns in these files using this script
230210_filling_id_in_british_vcf.py



# 13 Feb 2023. The same was done for the Japanese and Nigerian populations 

# the genotype info from each <population>_filled_in_IDs.vcf was put into a dictionary
<population>_dictionary.py

# and then a databases were created from the dictionaries 
<population>_db_setup.py

