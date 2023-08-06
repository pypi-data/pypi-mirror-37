# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ankisync', 'ankisync.builder', 'ankisync.presets']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4,<2.0',
 'importlib_resources>=1.0,<2.0',
 'peewee>=3.7,<4.0',
 'psutil>=5.4,<6.0']

setup_kwargs = {
    'name': 'ankisync',
    'version': '0.1.2',
    'description': 'Doing in Anki what AnkiConnect cannot do',
    'long_description': '# ankisync\n\nDoing what AnkiConnect cannot do, including\n- Creating new `*.apkg`\n- Creating new note type / model\n- Setting next review\n- Setting card statistics\n- Note ids to Card ids\n\nBut of course, this is very unsafe compared to pure AnkiConnect. I will not hold liability to damage it may cost.\n\n## Usage\n\nPlease close your `Anki` application first before doing this!\n\n```python\nfrom ankisync.anki import Anki\nfrom ankisync.builder import FieldBuilder, TemplateBuilder\nwith Anki() as a:\n    a.add_model(\n        name=\'foo\',\n        fields=[FieldBuilder(name, i) for i, name in enumerate([\'field_a\', \'field_b\', \'field_c\'])],\n        templates=[TemplateBuilder(\n            name=k,\n            question=q,\n            answer=a,\n            order=i\n        ) for i, (k, [q,a]) in enumerate({\n            \'Forward\': [QUESTION1, ANSWER1],\n            \'Reverse\': [QUESTION2, ANSWER2]\n        }.items())]\n    )\n```\n\nMost of the other API\'s are similar to AnkiConnect, but `_by_id()`\'s are preferred.\n\nCreating a new `*.apkg` is also possible.\n\n```python\nfrom ankisync.apkg import Apkg\nfrom ankisync.builder import FieldBuilder, TemplateBuilder, ModelBuilder, DeckBuilder\nwith Apkg(\'bar.apkg\') as a:\n    model_id = a.init(\n        first_model=ModelBuilder(\n            name=\'foo\',\n            fields=[FieldBuilder(name, i) for i, name in enumerate([\'field_a\', \'field_b\', \'field_c\'])],\n            templates=[TemplateBuilder(\n                name=k,\n                question=q,\n                answer=a,\n                order=i\n            ) for i, (k, [q,a]) in enumerate({\n                \'Forward\': [QUESTION1, ANSWER1],\n                \'Reverse\': [QUESTION2, ANSWER2]\n            }.items())]\n        ),\n        first_deck=DeckBuilder(name=\'baz\')\n    )\n    a.add_note({\n        \'modelName\': \'foo\',\n        \'deckId\': 1,  # "Default" deck\n        \'fields\': {\n            \'field_a\': \'aaaaa\',\n            \'field_b\': 123  # Numbers will be converted to string.\n        }\n    })\n```\n\nFor the example of how I use it in action, see https://github.com/patarapolw/zhlib/blob/09aa27157e6876398aa14f12b2917bd9dafee959/zhlib/export.py#L56\n\n## Installation\n\n```\npip install ankisync\n```\n\n## Contributions\n\n- What features outside AnkiConnect (or inside) do you want? I will try to implement it.\n- Help me understand the documentations, [AnkiDroid Wiki](https://github.com/ankidroid/Anki-Android/wiki/Database-Structure), and [Anki decks collaboration Wiki](http://decks.wikia.com/wiki/Anki_APKG_format_documentation) \n- Please help me implement the `NotImplemented` methods.\n\n## Note\n\n- This is the successor to [AnkiTools](https://github.com/patarapolw/AnkiTools). I will not update it anymore.\n',
    'author': 'Pacharapol Withayasakpunt',
    'author_email': 'patarapolw@gmail.com',
    'url': 'https://github.com/patarapolw/ankisync',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
