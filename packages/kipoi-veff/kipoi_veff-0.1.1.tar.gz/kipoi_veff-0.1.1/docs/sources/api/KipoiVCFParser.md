<h1 id="kipoi_veff.parsers.KipoiVCFParser">KipoiVCFParser</h1>

```python
KipoiVCFParser(self, vcf_file)
```
Iteratively parse a vcf file into a dictionary. This class was designed to work well with VCFs annotated by
`kipoi-veff`. It performs automated shortening of column names.

__Arguments__

- __vcf_file__: .vcf file path (can be also .vcf.gz, .bcf, .bcf.gz)

__Notes__

Iterator returns a nested dictionary with the schema:

```yaml
 - variant:
   - id
   - chr
   - pos
   - ref
   - alt
 - other:
   - f1
   - f2
 - kipoi:
   - model:
     - type:
       - feature1...
       - feature2...
```

