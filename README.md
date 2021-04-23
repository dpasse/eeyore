# Eeyore
> a text extraction / generation library

<hr>
<br />

## <a name="table-of-contents"></a>Table of Contents
* [Text Generation](#text-generation)
  * [Markov Chain](#markov-chain)
* [Token Tagging](#text-tagging)
  * [Phrase Chunker](#phrase-chunker)
  * [POS Chunker](#pos-chunker)
  * [Define Scope](#scoper)
  * [Tag Mapper](#tag-mapper)
  * [Context Pipeline](#context-pipeline)
* [Text Extraction](#text-extraction)
  * [Tag Extract](#tag-extract)
  * [Scope Overlap Extract](#tag-scope-overlap-extract)
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

## <a name="text-tagging"></a>Text Tagging
<br />

### <a name="phrase-chunker"></a>Phrase Chunker:

```python
from eeyore.models import Tag, RegexPhrase
from eeyore.taggers import PhraseChunker

chunker = PhraseChunker(tags=[
    Tag('LOC', phrase=RegexPhrase(r'\b(New York)\b')),
])

tokens, phrases = chunker.tag('We went to New York.')

## tokens == ['We', 'went', 'to', 'New', 'York', '.']
## phrases == ['', '', '', 'B-LOC', 'I-LOC', '']
```

<p align="right">
  <a href='#table-of-contents'>&#8593;</a>
</p>

### <a name="pos-chunker"></a>POS Chunker:

```python
from eeyore.models import Context
from eeyore.taggers import PosChunker

context = Context('Learn php from sam')
context.add('pos', ['JJ', 'NN', 'IN', 'NN'])

chunker = PosChunker("NP: {<DT>?<JJ>*<NN>}")
chunks = chunker.tag(context)

## chunks == ['B-NP', 'I-NP', '', 'B-NP']
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
        scope_direction=ScopeDirection.RIGHT,
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

### <a name="tag-mapper"></a>Tag Mapper:

```python
from eeyore.taggers import TagMapper

tag_mapper = TagMapper({
  'negtaive': 'negative',
  'fales': 'false'
})

mapped_tags = tag_mapper.tag(['negtaive', 'fales', 'nxet'])
## mapped_tags == ['negative', 'false', 'nxet']

tag_mapper = TagMapper({
    'VBD': 'past',
    'VBG': 'present',
    'VBN': 'past',
    'VBP': 'present',
    'VBZ': 'present'
}, clear_if_missing=True)

pos = ['DT', 'JJ', 'NN', 'VBD', 'RB', 'RB', 'VBN']
mapped_tags = tag_mapper.tag(pos)
## mapped_tags == ['', '', '', 'past', '', '', 'past']
```

<p align="right">
  <a href='#table-of-contents'>&#8593;</a>
</p>

### <a name="context-pipeline"></a>Context Pipeline:

```python
from eeyore.models import Tag, RegexPhrase
from eeyore.taggers import PhraseChunker
from eeyore.pipelines import ChunkerPipe, TokenAttributesPipe, ContextPipeline


pipeline = ContextPipeline(
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
## regex_ner = ['', '', '', '', '', 'B-LOC', 'I-LOC', '']

pos = context.get('pos')
## pos = ['PRP', 'VBP', 'RB', 'VBG', 'TO', 'NNP', 'NNP', '.']
```

<p align="right">
  <a href='#table-of-contents'>&#8593;</a>
</p>
<br />

## <a name="text-extraction"></a>Text Extraction
<br />

### <a name="tag-extract"></a>Tag Extract:

```python
from eeyore.extractions import TagExtract
from eeyore.models import Context

context = Context('We are not going to New York.')
context.add('entities', ['', '', '', '', '', 'B-LOC', 'I-LOC', ''])

location_extracts = TagExtract(
    'entities',
    ['LOC']
).evaluate(context)
## location_extracts == {
##     'LOC': [
##         [
##             (5, 'New'),
##             (6, 'York')
##         ]
##     ]
## }
```

<p align="right">
  <a href='#table-of-contents'>&#8593;</a>
</p>

### <a name="tag-scope-overlap-extract"></a>Scope Overlap Extract:

```python
from eeyore.extractions import ScopeOverlapExtract
from eeyore.models import Context

context = Context('Tom declined cancer treatment.')
context.add('scope1', ['', 'S1', 'S1', 'S1', 'S1'])
context.add('scope2', ['', '', 'S2', 'S2', ''])

relationships = ScopeOverlapExtract('scope1', 'scope2').evaluate(context)
## relationships == ['', 'REL', 'REL', 'REL', 'REL']

context = Context('Tom declined cancer treatment.')
context.add('scope1', ['S1', 'S1', '', '', ''])
context.add('scope2', ['', '', '', 'S2', ''])

relationships = ScopeOverlapExtract('scope1', 'scope2').evaluate(context)
## relationships == ['', '', '', '', '']
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