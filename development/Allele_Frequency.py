# The function takes two prompts as input. filename which will be the population vcf file and output which is the text file that the allele frequencies are written to.
def Allele_Frequency(filename, output):
    with open(filename, "r") as f:
        # Open the output file
        with open(output, "w") as out_f:
            # Write the header line to the output file
            out_f.write("CHROM\tPOS\tREF\tALT\tREF_FREQ\tALT_FREQ\n")
        
            # Iterate over each line in the vcf file
            for line in f:
                # Skip header lines
                if line.startswith("#"):
                    continue
            
                # Split the line into fields
                fields = line.strip().split("\t")
            
                # Get the reference allele and alternate alleles
                ref = fields[3]
                alt = fields[4]
            
                # Get the genotype information for all samples
                genotypes = fields[9:]
            
                # Calculate the frequency of each allele
                ref_count = 0
                alt_count = 0
                for genotype in genotypes:
                    if genotype == "0|0":
                        ref_count += 2
                    elif genotype == "0|1" or genotype == "1|0":
                        ref_count += 1
                        alt_count += 1
                    elif genotype == "1|1":
                        alt_count += 2
            
                # Calculate the allele frequencies
                total_count = ref_count + alt_count
                ref_frequency = ref_count / total_count
                alt_frequency = alt_count / total_count
            
                # Write the result to the output file
                out_f.write("{}\t{}\t{}\t{}\t{:.4f}\t{:.4f}\n".format(
                    fields[0], fields[1], ref, alt, ref_frequency, alt_frequency
                ))
