<h1 id="kipoi_veff.scores">kipoi_veff.scores</h1>


<h2 id="kipoi_veff.scores.Ref">Ref</h2>

```python
Ref(self, rc_merging='mean')
```
Returns the predictions for the reference allele.

If the predictions were executed taking
the reverse-complement of the sequence into account then the returned value is averaged by
the function defined in `rc_merging`. Allowed values for `rc_merging` are: "min", "max", "mean", "median",
"absmax" or any callable that accepts/expects two arguments:  `my_func(fwd_pred, rc_pred)`.

Reverse-complement-averaging, where applicable, is performed after score calculation.

<h2 id="kipoi_veff.scores.Alt">Alt</h2>

```python
Alt(self, rc_merging='mean')
```
Returns the predictions for the alternative allele.

If the predictions were executed taking
the reverse-complement of the sequence into account then the returned value is averaged by
the function defined in `rc_merging`. Allowed values for `rc_merging` are: "min", "max", "mean", "median",
"absmax" or any callable that accepts/expects two arguments:  `my_func(fwd_pred, rc_pred)`.

Reverse-complement-averaging, where applicable, is performed after score calculation.

<h2 id="kipoi_veff.scores.Diff">Diff</h2>

```python
Diff(self, rc_merging='mean')
```
Returns the difference between predictions for the reference and alternative
sequences prediction difference: `diff = p_alt - p_ref`

If the predictions were executed taking
the reverse-complement of the sequence into account then the returned value is averaged by
the function defined in `rc_merging`. Allowed values for `rc_merging` are: "min", "max", "mean", "median",
"absmax" or any callable that accepts/expects two arguments:  `my_func(fwd_pred, rc_pred)`.

Reverse-complement-averaging, where applicable, is performed after score calculation.

<h2 id="kipoi_veff.scores.LogitRef">LogitRef</h2>

```python
LogitRef(self, rc_merging='mean')
```
Returns the predictions for the reference allele on the logit scale: `np.log(p_alt / (1 - p_alt ))`.

If the predictions were executed taking
the reverse-complement of the sequence into account then the returned value is averaged by
the function defined in `rc_merging`. Allowed values for `rc_merging` are: "min", "max", "mean", "median",
"absmax" or any callable that accepts/expects two arguments:  `my_func(fwd_pred, rc_pred)`.

Reverse-complement-averaging, where applicable, is performed after score calculation.

<h2 id="kipoi_veff.scores.LogitAlt">LogitAlt</h2>

```python
LogitAlt(self, rc_merging='mean')
```
Returns the predictions for the alternative allele on the logit scale: `np.log(p_alt / (1 - p_alt ))`

If the predictions were executed taking
the reverse-complement of the sequence into account then the returned value is averaged by
the function defined in `rc_merging`. Allowed values for `rc_merging` are: "min", "max", "mean", "median",
"absmax" or any callable that accepts/expects two arguments:  `my_func(fwd_pred, rc_pred)`.

Reverse-complement-averaging, where applicable, is performed after score calculation.


<h2 id="kipoi_veff.scores.Logit">Logit</h2>

```python
Logit(self, rc_merging='mean')
```
Returns the difference between predictions for the reference and alternative sequences on
the logit scale: `logit_diff = log(p_alt / (1 - p_alt )) - log(p_ref / (1 - p_ref ))`

If the predictions were executed taking
the reverse-complement of the sequence into account then the returned value is averaged by
the function defined in `rc_merging`. Allowed values for `rc_merging` are: "min", "max", "mean", "median",
"absmax" or any callable that accepts/expects two arguments:  `my_func(fwd_pred, rc_pred)`.

Reverse-complement-averaging, where applicable, is performed after score calculation.

<h2 id="kipoi_veff.scores.DeepSEA_effect">DeepSEA_effect</h2>

```python
DeepSEA_effect(self, rc_merging='mean')
```
Returns the score used by DeepSEA in order to calculate the e-value: `abs(logit_diff) * abs(diff)`

If the predictions were executed taking
the reverse-complement of the sequence into account then the returned value is averaged by
the function defined in `rc_merging`. Allowed values for `rc_merging` are: "min", "max", "mean", "median",
"absmax" or any callable that accepts/expects two arguments:  `my_func(fwd_pred, rc_pred)`.

Reverse-complement-averaging, where applicable, is performed after score calculation.

