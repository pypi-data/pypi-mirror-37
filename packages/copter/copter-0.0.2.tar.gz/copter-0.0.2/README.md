# Copter

A library for codon optimization

### Installation

```
pip install copter
```

### Quick Start

```
def eval_codons_gc_ratio(codons):
  gene = ''.join(codons)
  gc_ratio = (gene.count('G') + gene.count('C')) / float(len(gene))
  return[gc_ratio]

protein = 'NAMALGLMET'
optimized_genes = optimize(protein,
                           eval_codons_gc_ratio,
                           [1.0],
                           indpb=0.05,
                           population_size=20,
                           generation_size=100,
                           surviver_amount=10)
```
