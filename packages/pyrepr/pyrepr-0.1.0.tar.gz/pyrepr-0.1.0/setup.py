# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pyrepr']

package_data = \
{'': ['*']}

install_requires = \
['markdownify>=0.4.1,<0.5.0', 'toml>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'pyrepr',
    'version': '0.1.0',
    'description': 'Pretty-printing serializable objects for humans',
    'long_description': "# pyrepr\n\nPretty-printing serializable objects for humans. This is based on [Markdownify](https://github.com/matthewwithanm/python-markdownify) and [TOML](https://github.com/toml-lang/toml).\n\n## Usage\n\n```python\nfrom pyrepr import Repr\nprint(Repr(obj))\n```\n\nExample output:\n\n```\n[[mid]]\n1358629116480\n\n[[mod]]\n1481117769\n\n[[usn]]\n3491\n\n[[tags]]\n CostanzoEndocrine EndocrinePhysiology \n\n[[flds]]\nPeptide and Protein Hormone Synthesis:   \nTranslation of a **preprohormone ***begins* in the **{{c1::cytoplasm}} **with a **signal** **peptide** at the N terminusx1f![](paste-417251777839638.jpg)\n\n[[sfld]]\nPeptide and Protein Hormone Synthesis: Translation of a preprohormone begins in the {{c1::cytoplasm}} with a signal peptide at the N terminus\n\n[[csum]]\n1963658058\n\n[[flags]]\n0\n```\n\nYou can also make output as pure Markdown\n\n```python\nprint(Repr(obj).to_str('markdown'))\n```\n\n```markdown\n## mid\n1358629116480\n\n## mod\n1481117769\n\n## usn\n3491\n\n## tags\n CostanzoEndocrine EndocrinePhysiology \n\n## flds\nPeptide and Protein Hormone Synthesis:   \nTranslation of a **preprohormone ***begins* in the **{{c1::cytoplasm}} **with a **signal** **peptide** at the N terminusx1f![](paste-417251777839638.jpg)\n\n## sfld\nPeptide and Protein Hormone Synthesis: Translation of a preprohormone begins in the {{c1::cytoplasm}} with a signal peptide at the N terminus\n\n## csum\n1963658058\n\n## flags\n0\n```\n\n## Installation\n\n```commandline\npip install pyrepr\n```\n",
    'author': 'Pacharapol Withayasakpunt',
    'author_email': 'patarapolw@gmail.com',
    'url': 'https://github.com/patarapolw/pyrepr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
