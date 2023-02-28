import pysam

# Open the first VCF file
vcf1 = pysam.VariantFile("British.vcf")

# Open the second VCF file
vcf2 = pysam.VariantFile("gen_coords_chr6_only.vcf")

# Create a set to store the positions of the variants in the second VCF file
positions = set()

# Iterate through each variant in the second VCF file and add its position to the set
for record in vcf2.fetch():
    positions.add(record.start)

# Open a new VCF file to store the filtered variants
with pysam.VariantFile("British_filtered_variants.vcf", "w", header=vcf1.header) as vcf_writer:

    # Iterate through each variant in the first VCF file
    for record in vcf1.fetch():

        # Check if the position of the variant is in the set of positions from the second VCF file
        if record.start in positions:

            # If the condition is true, write the variant to the output file
            vcf_writer.write(record)

