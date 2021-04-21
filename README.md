# Eeyore
> a text extraction / generation library

<hr>
<br />

## <a name="table-of-contents"></a>Table of Contents
* [Text Generation](#text-generation)
  * [Markov Chain](#markov-chain)
* [Text Extraction](#text-extraction)
  * [Phrase Chunker](#phrase-chunker)
  * [Pos Chunker](#pos-chunker)
  * [Define Scope](#scoper)
  * [Pipeline](#pipeline)
* [References](#references)

<br />
<br />

## <a name="text-generation"></a>Text Generation

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
<p align="right">
  <a href='#table-of-contents'>&#8593;</a>
</p>


<br />

## <a name="text-extraction"></a>Text Extraction

<br />

### <a name="phrase-chunker"></a>Phrase Chunker:

```python
from eeyore.models import Tag, RegexPhrase
from eeyore.taggers import PhraseChunker

chunker = PhraseChunker(tags=[
    Tag('R', phrase=RegexPhrase(r'\b(New York)\b')),
])

tokens, phrases = chunker.tag('We went to New York.')

## tokens == ['We', 'went', 'to', 'New', 'York', '.']
## phrases == ['', '', '', 'R', 'R', '']
```

<p align="right">
  <a href='#table-of-contents'>&#8593;</a>
</p>

### <a name="pos-chunker"></a>Pos Chunker:

```python
from eeyore.models import Context
from eeyore.taggers import PosChunker

context = Context('Learn php from sam')
context.add('pos', ['JJ', 'NN', 'IN', 'NN'])

chunker = PosChunker("NP: {<DT>?<JJ>*<NN>}")
chunks = chunker.tag(context)

## chunks == ['NP', 'NP', 'S', 'NP']
```

<p align="right">
  <a href='#table-of-contents'>&#8593;</a>
</p>

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

<p align="right">
  <a href='#table-of-contents'>&#8593;</a>
</p>

### <a name="pipeline"></a>Pipeline:

```python
from eeyore.models import Tag, RegexPhrase
from eeyore.taggers import PhraseChunker
from eeyore.pipelines import ChunkerPipe, TokenAttributesPipe, Pipeline


pipeline = Pipeline(
    pipes=[
        ChunkerPipe(
            'regex_ner',
            PhraseChunker(tags=[
                Tag(
                    'LOC',
                    phrase=RegexPhrase(r'\b(New York)\b')
                ),
            ]),
            order=1
        ),
        TokenAttributesPipe(order=2),
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

<p align="right">
  <a href='#table-of-contents'>&#8593;</a>
</p>
<br />

## <a name="references"></a>References:

<br />

1. Chapman, Wendy & Bridewell, Will & Hanbury, Paul & Cooper, Gregory & Buchanan, Bruce. (2001). A Simple Algorithm for Identifying Negated Findings and Diseases in Discharge Summaries. Journal of Biomedical Informatics. 34. 301-310. 10.1006/jbin.2001.1029.

</br>

2. Chapman, Wendy & Chu, David & Dowling, John. (2007). ConText: An Algorithm for Identifying Contextual Features from Clinical Text. BioNLP 2007: Biological, translational, and clinical language processing. Prague, CZ. 81-88.

<p align="right">
  <a href='#table-of-contents'>&#8593;</a>
</p>
<br />