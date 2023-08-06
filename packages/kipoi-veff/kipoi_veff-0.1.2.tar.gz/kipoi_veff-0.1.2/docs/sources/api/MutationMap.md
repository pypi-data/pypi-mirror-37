<h1 id="kipoi_veff.MutationMap">MutationMap</h1>

```python
MutationMap(self, model, dataloader, dataloader_args=None, use_dataloader_example_data=False)
```

<h2 id="kipoi_veff.MutationMap.query_region">query_region</h2>

```python
MutationMap.query_region(self, chrom, start, end, seq_length=None, scores=['logit_ref', 'logit_alt', 'ref', 'alt', 'logit', 'diff'], score_kwargs=None, **kwargs)
```
Generate mutation map

Prediction of effects of every base at every position of datalaoder input sequences. The regions for which
the effect scores will be calculated are primarily defined by the dataloader input. If the dataloader accepts
`bed` file inputs then this file will be overwritten with regions defined here of length `seq_length` or
the model input sequence length. If that is not available all datalaoder-generated regions that overlap the
region defined here will be investigated. Effect scores are returned as `MutationMapPlotter` object which can
be saved to  an hdf5 file and used for plotting. It is important to mention that the order of the scored
sequences is the order in which the dataloader has produced data input - intersected with the region defined
here.

__Arguments__

- __chrom__: Chrosome of region of interest. Assembly is defined by the dataload arguments.
- __start__: Start of region of interest. Assembly is defined by the dataload arguments.
- __end__: End of region of interest. Assembly is defined by the dataload arguments.
- __seq_length__: Optional argument of model sequence length to use if model accepts variable input
    sequence length.
- __scores__: list of score names to compute. See kipoi_veff.scores
- __score_kwargs__: optional, list of kwargs that corresponds to the entries in score.

__Returns__

    A `MutationMapPlotter` object containing variant scores.

<h2 id="kipoi_veff.MutationMap.query_bed">query_bed</h2>

```python
MutationMap.query_bed(self, bed_fpath, seq_length=None, scores=['logit_ref', 'logit_alt', 'ref', 'alt', 'logit', 'diff'], score_kwargs=None, **kwargs)
```
Generate mutation map

Prediction of effects of every base at every position of datalaoder input sequences. The regions for which
the effect scores will be calculated are primarily defined by the dataloader input. If the dataloader accepts
`bed` file inputs then this file will be overwritten with regions defined in `bed_fpath` of length
`seq_length` or the model input sequence length. If that is not available all datalaoder-generated
regions that overlap the region defined here will be investigated. Effect scores are returned as
`MutationMapPlotter` object which can be saved to  an hdf5 file and used for plotting. It is important to
mention that the order of the scored sequences is the  order in which the dataloader has produced data
input - intersected with `bed_fpath`.

__Arguments__

- __bed_fpath__: Only genomic regions overlapping regions in this bed file will be evaluated. If
        the dataloader accepts bed file input then the dataloader bed input file will be overwritten with
        regions based this (`bed_fpath`) bed file. Assembly is defined by the dataload arguments.
- __seq_length__: Optional argument of model sequence length to use if model accepts variable input
        sequence length.
- __scores__: list of score names to compute. See kipoi_veff.scores
- __score_kwargs__: optional, list of kwargs that corresponds to the entries in score.

__Returns__

    A `MutationMapPlotter` object containing variant scores.

<h2 id="kipoi_veff.MutationMap.query_vcf">query_vcf</h2>

```python
MutationMap.query_vcf(self, vcf_fpath, seq_length=None, scores=['logit_ref', 'logit_alt', 'ref', 'alt', 'logit', 'diff'], score_kwargs=None, var_centered_regions=True, **kwargs)
```
Generate mutation map

Prediction of effects of every base at every position of datalaoder input sequences. The regions for which
the effect scores will be calculated are primarily defined by the dataloader input. If the dataloader accepts
`bed` file inputs then this file will be overwritten with regions generaten from the SNVs in `vcf_fpath`in a
variant-centered fashion. Sequence length is defined by `seq_length` or the model input sequence length.
If the datalaoder does not have a `bed` file input all datalaoder-generated regions that overlap SNVs
here will be investigated. Effect scores are returned as `MutationMapPlotter` object which can be saved to
an hdf5 file and used for plotting. It is important to mention that the order of the scored sequences is the
order in which the dataloader has produced data input - intersected with `vcf_fpath`.

__Arguments__

- __vcf_fpath__: Only genomic regions overlapping the variants in this VCF will be evaluated.
        Variants defined here will be highlighted in mutation map plots. Only SNVs will be used. If
        vcf_to_region is defined and the dataloader accepts bed file input then the dataloader bed input
        file will be overwritten with regions based on variant positions of this VCF.
- __seq_length__: Optional argument of model sequence length to use if model accepts variable input
        sequence length.
- __var_centered_regions__: Generate variant-centered regions if the model accepts that. If a custom
        `vcf_to_region` should be used then this can be set explicitly in the kwargs.
- __scores__: list of score names to compute. See kipoi_veff.scores
- __score_kwargs__: optional, list of kwargs that corresponds to the entries in score.

__Returns__

    A `MutationMapPlotter` object containing variant scores.

