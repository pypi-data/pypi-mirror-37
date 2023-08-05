Generated from [notebooks/variant_effect_prediction_simple.ipynb](https://github.com/kipoi/kipoi-veff/blob/master/notebooks/variant_effect_prediction_simple.ipynb)

# Variant effect prediction - simple

NOTE: This notebook is a companion notebook to `variant_effect_prediction.ipynb` and shows a simpler way to run variant effect predictions in python. If you want to know more details about variant effect prediction, the details of how to customise things and how to run it on the command line and in batch please refer to the `variant_effect_prediction.ipynb`.

Variant effect prediction offers a simple way to predict effects of SNVs using any model that uses DNA sequence as an input. Many different scoring methods can be chosen, but the principle relies on in-silico mutagenesis. The default input is a VCF and the default output again is a VCF annotated with predictions of variant effects. 

First we set up the model and make sure the requirements are installed in the current environment.


```python
import kipoi
model_name = "DeepSEA/variantEffects"
```

Then we need to know where the query VCF is located and where we want to store the results.


```python
# The input vcf path
vcf_path = "example_data/clinvar_donor_acceptor_chr22.vcf"
# The output vcf path, based on the input file name    
out_vcf_fpath = vcf_path[:-4] + "%s.vcf"%model_name.replace("/", "_")
```

Finally the dataloader arguments are set that are required to run the dataloader. Here we omit the `intervals_file` argument of the dataloader, because that has been tagged as bed file input in the `dataloader.yaml` file, which means that `score_variants` will automatically populate that argument with a temporary bed file that is generated from the VCF in order to query every variant contained in the input VCF. ("Variant-centered approach")


```python
# The datalaoder keyword arguments
dataloader_arguments = {"fasta_file": "example_data/hg19_chr22.fa"}
```


```python
!ls example_data/
```

    chr22.101bp.2000_intervals.JUND.HepG2.tsv
    clinvar_donor_acceptor_annotated_chr22.csv
    clinvar_donor_acceptor_annotated_w_rbp_chr22.csv
    clinvar_donor_acceptor_chr22DeepSEA_variantEffects.vcf
    clinvar_donor_acceptor_chr22.vcf
    clinvar_donor_acceptor_chr22.vcf.gz
    clinvar_donor_acceptor_chr22.vcf.gz.tbi
    dbsnp_chr22_29108009.vcf
    hg19_chr22.fa
    hg19_chr22.fa.fai
    Homo_sapiens.GRCh37.75_chr22.gtf
    Homo_sapiens.GRCh37.75.filtered_chr22.gtf



```python
import kipoi_veff.snv_predict as sp
sp.score_variants(model = model_name,
                  dl_args = dataloader_arguments,
                  input_vcf = vcf_path,
                  output_vcf = out_vcf_fpath)
```

     29%|██▊       | 4/14 [00:11<00:28,  2.83s/it]

Now we can have a look at the generated output:


```python
# Let's print out the first 40 lines of the annotated VCF (up to 80 characters per line maximum)
with open("example_data/clinvar_donor_acceptor_chr22DeepSEA_variantEffects.vcf") as ifh:
    for i,l in enumerate(ifh):
        long_line = ""
        if len(l)>80:
            long_line = "..."
        print(l[:80].rstrip() +long_line)
        if i >=40:
            break
```

Here we have shown a simpler function `score_variants` that covers most use-cases for variant effect prediction. For a more fine-grain control please use `predict_snvs` and take a look at the `variant_effect_prediction.ipynb` notebook. 

An important thing to remember when using `score_variants` or the command-line interface is that for all dataloaders that support bed-file inputs, the bed file generation will be used and only model that do not have the `postprocessing > variant_effects > bed_input` field set in `dataloader.yaml` will be executed in overlap-based mode. For details on how variant region overlap works please take a look at the variant effect prediction documentation. 
