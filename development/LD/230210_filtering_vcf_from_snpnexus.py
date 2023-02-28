import pysam

# Open the VCF file for reading
vcf_file = pysam.VariantFile("gen_coords.vcf")

# Open a new file for writing the filtered records
out_file = pysam.VariantFile("gen_coords_only_chr6.vcf", "w", header=vcf_file.header)

# Iterate through each record in the VCF file
for record in vcf_file:
	# Check if the record's CHROM is equal to "6"
    	if record.chrom == "6":
        	# Write the record to the output file
        	out_file.write(record)

# Close both files
vcf_file.close()
out_file.close()
