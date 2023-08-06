# CorpusSearch

A tool to load and search in text corpora.

The tool provides routines to search in large corpora in pandas dataframe format, where rows contain textual information on the level of sentences or paragraphs.
Dataframes can be single or multilevel indexed and loaded from URL, DOI, [citable](http://www.edition-topoi.org/publishing_with_us/citable) or local files. Accepted file formats are pickle, excel, json and csv.

This package is designed to work with Jupyter Notebooks as well as in the IPython command line. If used in a Notebook, the user has access to a search GUI. See the [example folder](examples) for some simple examples in Jupyter Notebooks.  

# Content

1. [Installation](#installation)
2. [Usage](#basic-usage)
3. [GUI usage](#gui-usage)
4. [Search in context](#search-words-of-similar-context)
5. [Visualization](#visualization)


# Installation

The package can be installed via `pip`:
```
  pip install corpussearch
```

Since the package is under active development, the most recent version is always on Github, and can be installed by
```
  pip install git+https://github.com/computational-antiquity/corpussearch.git
```

# Basic usage

Import the package
```python
from corpussearch import search as corSearch
```

The class is instantiated by providing the path to the source file. Excepted
formats are pickled dataframes, CSV, JSON or Excel files.

Standard parameters assume pickled, multi-indexed dataframes, where the main text
is contained in a column 'text'. For other sources change parameters accordingly.

## Loading data

Using a pre-pickled dataframe:
```python
  search = corSearch('./path/to/dataframe/file.pickle')
```

Using data in excel format:
```python
  search = corSearch(
      pathDF='./path/to/excel/file.xlsx'
      dataType='excel',
      dataIndex='single'
  )
```

Loading data in excel format from a DOI:
```python
  search = corSearch(
      pathDF='10.17171/1-6-90'
      pathType='DOI',
      dataType='excel',
      dataIndex='single'
  )
```

## Search for text and/or parts

A reduction to a specific part and page number is obtained by chaining the desired
reductions `.reduce(key,value)`, where `key` can be either a level of the multi index, or a column name. To obtain the resulting dataframe, `.results()` is added.

```python
  result = search.reduce('part','part_name').reduce('page','page_number').results()
```

To restart a search, e.g. within another part, use
```python
  search.resetSearch()
```

Additional search logic can be used with `.logicReduce()`. The method accepts a
list of reductions chained with logical AND,OR, or NOT. For example,
```python
  search.logicReduce([('part','Part1'),&,('page','10'),|,('text','TEST')]).result()
```
will return the entries of a dataframe where part is Part1 and page number is 10, or the text string contains TEST.

# GUI usage

Import the GUI part of the package into a Jupyter Notebook
```python
from corpussearch import gui as CorpusGUI
```

Instantiate with path to source file, as above.
```python
  gui = CorpusGUI('./path/to/dataframe/file.pickle')
```
and display the interface
```python
  gui.displayGUI()
```

A basic word search returns all results where the search word is contained in the main column, e.g. 'text'. Search values can contain regular expressions, e.g. `\d{2,4}\s[A-Z]`.
For search in parts other then the main column, fuzzy searches are possible if the number of unique values on that level is less than `maxValues`. This routine uses `difflib` to compare the search string to possible values on that level. This can help if the actual string formating is not well known, but could possibly lead to undesired results.

Results are displayed in the sentence output boxes, where the right box contains meta-information derived from the non-main columns or multi-index levels.

To navigate between results use the slider.

## Additional search logic

To chain search terms, use the 'more'-button. This opens additional search fields.
Possible logic operations are 'AND', 'OR', and 'NOT'. Each logic operation is between
two consecutive search pairs (part,value). The logic operates in a linear fashion, from the first triple downwards, e.g. for the search ``(('text','NAME') & ('part','PART1') | ('page','PAGE4'))`` each tuple (key,value) yields a boolean vector v, such that the search becomes `(v1 & v2 | v3)`. Evaluation continues for the pair `v<sub>temp</sub> = (v1 & v2)`, and finally `v<sub>res</sub>= (v<sub>temp</sub> | v3)`. The resulting boolean vector is used to reduce the full data to the dataframe containing the search result.

# Search words of similar context

To find words which occur in a similar context in the corpus, a simple machine-learning module is provided. The module is based on [Gensims word2vec](https://github.com/RaRe-Technologies/gensim) and uses `difflib` for words
which are not part of the training dictionary.

Import the machine-learning module using
```python
from corpussearch import ml as corML
```

Instantiate with path to source file, as above. Additionally, you need to provide the language of the corpus, to remove stop-words and normalize the text (currently Greek, Latin, English and German are supported).

The model parameters for Gensims word2vec are a tuple (a,b,c) with the following functionality:

| par | used for |
|:---|:---:|
| a | number of workers |
| b | minimal occurrence of a word |
| c | feature size |


Optionally, you can enable the display of logging messages by `showLogging = True`.
```python
ml = corML(
        './path/to/dataframe/file.pickle',
        language='german',
        showLogging=True,
        model_params=(4,1,5)
        )
```

To train the model use
```python
ml.trainModel()
```

This automatically performs all necessary steps: It cleans the text column, creates a training_data column, and builds the vocabulary for the model.

To find words of similiar context just enter any word
```python
ml.getSimilarContext('searchterm')
```
If the search term is not contained in the dictionary, `difflib` tries to find a similar word, and performs the search for this word. The result is a list of words with their respective similarity weight.

# Visualization

**Attention:** *work in progress*

To visualize results of a search in Jupyter Notebooks you can use the `visualize` module.
```python
from corpussearch import vis as corVis
```
It is initialized with any result dataframe of a search and a label, which describes the search in the corpus.
```python
vis = corVis(
        result_dataframe
        'description of search'
        )
```

A GUI allows to select which column of the dataframe to use for plotting. If, for example, dates are provided with the corpus, one could plot a distribution of publications per year.

If the number of unique values for a column is of the order of the size of the dataframe, a warning is printed and no plotting occurs.

Additionally, the user can select the option `lambda function` to enter a custom function to operate on a column, which is then used for plotting. The format to enter is a tuple `(a,b)` with `a:` the column name to operate on, and `b:` the function (as a function of row) to apply to the column. Formating of the function depends on the column values, e.g. `row[:4]` for the first four characters of a string, or `row < 10` for integer comparison. The resulting new column can be checked by
```python
vis.resultDF.lambda_func
```
If the lambda function fails to create a new column, a warning is printed and a new column with `None` values is returned.
