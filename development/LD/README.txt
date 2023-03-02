#2023 Feb 10
#Marta Delfino
#data prep for group project

# first, I need to populate the rs ID columns in the vcf files

# I'm taking the vcf file from SNP nexus, called 1KGen.vcf, that was obtained by inputting the rs IDs obtained from the T1D GWAS data. 
# I've zipped the vcf file and indexed it
gzip <file> 
tabix -p vcf input.vcf.gz

# from the vcf file, I've filtered it to only contain chr6, with this command
grep "^6" input.vcf > output.vcf

# I've counted the lines with this command, there are 64 entries. so 64 rs IDs
grep "^6" input.vcf | wc -l

# the file with the genetic coordinates of chr6 is called: gen_coords_chr6_only.vcf

# I've ran the script 230210_filter_vcf_on_position.py to check for the positions from the T1D dataset, in the british population 

# next I've counted the number of lines in the outputted file, and there are 62. so 62 positions of variants

# then I've populated the ID column on the British_filtered_variants.vcf
python 230210_filling_id_in_british_vcf.py


# 13 Feb 2023. The same was done for the Japanese and Nigerian populations 

# the genotype info from each <population>_filled_in_IDs.vcf was put into a dictionary
<population>_dictionary.py

# and then a databases were created from the dictionaries 
<population>_db_setup.py

