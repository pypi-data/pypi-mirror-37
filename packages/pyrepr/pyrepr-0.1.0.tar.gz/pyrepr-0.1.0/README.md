# pyrepr

Pretty-printing serializable objects for humans. This is based on [Markdownify](https://github.com/matthewwithanm/python-markdownify) and [TOML](https://github.com/toml-lang/toml).

## Usage

```python
from pyrepr import Repr
print(Repr(obj))
```

Example output:

```
[[mid]]
1358629116480

[[mod]]
1481117769

[[usn]]
3491

[[tags]]
 CostanzoEndocrine EndocrinePhysiology 

[[flds]]
Peptide and Protein Hormone Synthesis:   
Translation of a **preprohormone ***begins* in the **{{c1::cytoplasm}} **with a **signal** **peptide** at the N terminusx1f![](paste-417251777839638.jpg)

[[sfld]]
Peptide and Protein Hormone Synthesis: Translation of a preprohormone begins in the {{c1::cytoplasm}} with a signal peptide at the N terminus

[[csum]]
1963658058

[[flags]]
0
```

You can also make output as pure Markdown

```python
print(Repr(obj).to_str('markdown'))
```

```markdown
## mid
1358629116480

## mod
1481117769

## usn
3491

## tags
 CostanzoEndocrine EndocrinePhysiology 

## flds
Peptide and Protein Hormone Synthesis:   
Translation of a **preprohormone ***begins* in the **{{c1::cytoplasm}} **with a **signal** **peptide** at the N terminusx1f![](paste-417251777839638.jpg)

## sfld
Peptide and Protein Hormone Synthesis: Translation of a preprohormone begins in the {{c1::cytoplasm}} with a signal peptide at the N terminus

## csum
1963658058

## flags
0
```

## Installation

```commandline
pip install pyrepr
```
