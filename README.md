# Eeyore
> a text extraction / generation library

<hr>
<br />

## <a name="table-of-contents"></a>Table of Contents
* [Text Generation](#text-generation)
  * [Markov Chain](#markov-chain)
* [Text Extraction](#text-extraction)
  * [Regex Chunker](#regex-chunker)
  * [Define Scope](#scoper)
  * [Pipeline](#pipeline)
* [References](#references)

<br />
<br />

## <a name="text-generation"></a>Text Generation

<hr />
<br />

### <a name="markov-chain"></a>Markov Chain:

```python
from eeyore.models import Relationship, RelationshipContainer
from eeyore.generators import MarkovChain

relationship_container = RelationshipContainer([
    Relationship('<start>', ['I']),
    Relationship('I', ['am']),
    Relationship('am', ['not', 'very', 'tired']),
    Relationship('not', ['very', 'tired']),
    Relationship('very', ['tired']),
    Relationship('tired', ['<end>']),
    Relationship('<end>', []),
])

markov_chain = MarkovChain(seed=42)
generated_relationship_chain = \
    markov_chain.generate(relationship_container)

sentence = [
    relationship.primary
    for relationship
    in generated_relationship_chain
]

## sentence == ['<start>', 'I', 'am', 'tired', '<end>']
```

<a style='float: right;' href='#table-of-contents'>&#8593;</a>
<br />
<br />

## <a name="text-extraction"></a>Text Extraction

<hr />
<br />

### <a name="regex-chunker"></a>Regex Chunker:

```python
from eeyore.models import Tag, RegexPhrase
from eeyore.taggers import Chunker

chunker = Chunker(tags=[
    Tag('R', phrase=RegexPhrase(r'\b(New York)\b')),
])

tokens, phrases = chunker.tag('We went to New York.')

## tokens == ['We', 'went', 'to', 'New', 'York', '.']
## phrases == ['', '', '', 'R', 'R', '']
```

<a style='float: right;' href='#table-of-contents'>&#8593;</a>
<br />

### <a name="scoper"></a>Define Scope:

```python
from eeyore.models import Scope, ScopeDirection
from eeyore.taggers import Scoper

scopes = [
    Scope(
        'NEG',
        scope_direction=ScopeDirection.FORWARD,
        order=1,
        stop_when=['TRANS']
    )
]

tokens = ['', '', 'NEG', '', '', 'TRANS', '', '']
scope_tags = Scoper(scopes).tag(tokens)

## scope_tags == ['', '', 'NEG', 'NEG', 'NEG', '', '', '']
```

<a style='float: right;' href='#table-of-contents'>&#8593;</a>
<br />

### <a name="pipeline"></a>Pipeline:

```python
from eeyore.models import Tag, RegexPhrase
from eeyore.taggers import Chunker
from eeyore.pipelines import ChunkerPipe, AttributePipe, Pipeline


pipeline = Pipeline(
    pipes=[
        ChunkerPipe(
            'regex_ner',
            Chunker(tags=[
                Tag(
                    'LOC',
                    phrase=RegexPhrase(r'\b(New York)\b')
                ),
            ]),
            order=1
        ),
        AttributePipe(order=2),
    ]
)

context = pipeline.execute('We are not going to New York.')

tokens = context.get('tokens')
## tokens = ['We', 'are', 'not', 'going', 'to', 'New', 'York', '.']

regex_ner = context.get('regex_ner')
## regex_ner = ['', '', '', '', '', 'LOC', 'LOC', '']

pos = context.get('pos')
## pos = ['PRP', 'VBP', 'RB', 'VBG', 'TO', 'NNP', 'NNP', '.']
```

<a style='float: right;' href='#table-of-contents'>&#8593;</a>
<br />
<br />

## <a name="references"></a>References:

<hr />

1. Chapman, Wendy & Bridewell, Will & Hanbury, Paul & Cooper, Gregory & Buchanan, Bruce. (2001). A Simple Algorithm for Identifying Negated Findings and Diseases in Discharge Summaries. Journal of Biomedical Informatics. 34. 301-310. 10.1006/jbin.2001.1029.

</br>

2. Chapman, Wendy & Chu, David & Dowling, John. (2007). ConText: An Algorithm for Identifying Contextual Features from Clinical Text. BioNLP 2007: Biological, translational, and clinical language processing. Prague, CZ. 81-88.

<a style='float: right;' href='#table-of-contents'>&#8593;</a>
<br />