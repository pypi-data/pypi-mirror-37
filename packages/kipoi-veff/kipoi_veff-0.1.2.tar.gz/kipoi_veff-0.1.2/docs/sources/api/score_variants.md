<h1 id="kipoi_veff.score_variants">score_variants</h1>

```python
score_variants(model, dl_args, input_vcf, output_vcf, scores=['logit_ref', 'logit_alt', 'ref', 'alt', 'logit', 'diff'], score_kwargs=None, num_workers=0, batch_size=32, source='kipoi', seq_length=None, std_var_id=False, restriction_bed=None, return_predictions=False, output_filter=None)
```
Score variants: annotate the vcf file using
model predictions for the refernece and alternative alleles
Args:
  model: model string or a model class instance
  dl_args: dataloader arguments as a dictionary
  input_vcf: input vcf file path
  output_vcf: output vcf file path
  scores: list of score names to compute. See kipoi_veff.scores
  score_kwargs: optional, list of kwargs that corresponds to the entries in score. For details see
  num_workers: number of paralell workers to use for dataloading
  batch_size: batch_size for dataloading
  source: model source name
  std_var_id: If true then variant IDs in the annotated VCF will be replaced with a standardised, unique ID.
  seq_length: If model accepts variable input sequence length then this value has to be set!
  restriction_bed: If dataloader can be run with regions generated from the VCF then only variants that overlap
  regions defined in `restriction_bed` will be tested.
  return_predictions: return generated predictions also as pandas dataframe.
  output_filter: If set then either a boolean filter or a named filter for model outputs that are reported.

