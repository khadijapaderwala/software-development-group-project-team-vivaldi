import pysam

vcf1 = pysam.VariantFile("gen_coords_chr6_only.vcf")
vcf2 = pysam.VariantFile("Nigerian_filtered_variants.vcf")

# Create a dictionary to store the positions and IDs from the first VCF file
pos_to_id = {}
for record in vcf1.fetch():
    pos_to_id[record.start] = record.id

# Open a new VCF file to store the filled-in ID column
with pysam.VariantFile("Nigerian_filled_in_IDs.vcf", "w", header=vcf2.header) as vcf_writer:

    # Iterate through each variant in the second VCF file
    for record in vcf2.fetch():

        # Check if the position of the variant is in the dictionary of positions and IDs
        if record.start in pos_to_id:

            # If the condition is true, fill in the ID column with the corresponding ID
            record.id = pos_to_id[record.start]

        # Write the variant to the output file, with or without a filled-in ID
        vcf_writer.write(record)

