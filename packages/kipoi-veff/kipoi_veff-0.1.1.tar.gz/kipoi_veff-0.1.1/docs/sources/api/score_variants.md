<h1 id="kipoi_veff.score_variants">score_variants</h1>

```python
score_variants(model, dl_args, input_vcf, output_vcf, scores=['logit_ref', 'logit_alt', 'ref', 'alt', 'logit', 'diff'], score_kwargs=None, num_workers=0, batch_size=32, source='kipoi', seq_length=None, std_var_id=False, restriction_bed=None, return_predictions=False, model_outputs=None)
```
Score variants: annotate the vcf file using model predictions for the reference and alternative alleles

The functional elements that generate a score from a set of predictions for reference and
alternative allele are defined in the `scores` argument.

This function is the python version of the command-line call `score_variants` and is a convenience version
of the `predict_snvs` function:

Prediction of effects of SNV based on a VCF. If desired the VCF can be stored with the predicted values as
annotation. For a detailed description of the requirements in the yaml files please take a look at
the core `kipoi` documentation on how to write a `dataloader.yaml` file or at the documentation of
`kipoi-veff` in the section: `overview/#model-and-dataloader-requirements`.


__Arguments__

- __model__: model string or a model class instance
- __dl_args__: dataloader arguments as a dictionary
- __input_vcf__: input vcf file path
- __output_vcf__: output vcf file path
- __scores__: list of score names to compute. See `kipoi_veff.scores`
- __score_kwargs__: optional, list of kwargs that corresponds to the entries in score.
- __num_workers__: number of paralell workers to use for dataloading
- __batch_size__: batch_size for dataloading
- __source__: model source name
- __std_var_id__: If true then variant IDs in the annotated VCF will be replaced with a standardised, unique ID.
- __seq_length__: If model accepts variable input sequence length then this value has to be set!
- __restriction_bed__: If dataloader can be run with regions generated from the VCF then only variants that overlap
    regions defined in `restriction_bed` will be tested.
- __return_predictions__: return generated predictions also as pandas dataframe.
- __model_outputs__: If set then either a boolean filter or a named filter for model outputs that are reported.

__Returns__

`dict`: containing a pandas DataFrame containing the calculated values
        for each model output (target) column VCF SNV line. If `return_predictions == False`, returns None.

