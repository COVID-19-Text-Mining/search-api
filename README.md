# Materials Scholar Core Library and RESTful API
This repo includes the core materials scholar functionality that should be kept private.

## Important notes
1. For installation and usage - it doesn't work with python3.7 as there are problems with dependencies, so use python3.6
2. It is recommended to use separate conda environments for each project as they may require different versions of same libraries

## Setting up
1. Create a fork on github
2. Clone your forked repo: `git clone https://github.com/YOUR_GITHUB_USERNAME/matscholar-core.git`
3. Also you need git-library matscholar, so create a fork of it on github
4. Clone your forked library: `git clone https://github.com/YOUR_GITHUB_USERNAME/matscholar.git`
5. Create conda environment for project with python3.6, here for installed anaconda3: `conda create NAME_ENV python=3.6`
6. Activate your environment: `source ~/anaconda3/bin/activate NAME_ENV`
7. Check: `which python` should give you path: `~/anaconda3/envs/NAME_ENV/bin/python`
`python --version` should give you python3.6
`which pip` should give you path: ~/anaconda3/envs/NAME_ENV/bin/pip
`pip --version` should give you ... (python3.6)
If something is wrong, check you ~/.bashrc or ~/.bash_profile for any lines with 'alias python=...', 'alias pip=...', restart terminal or running the following commands instead of pip or python write the full path to bin-file (example given further).
8. `cd matscholar`
9. `~/anaconda3/envs/NAME_ENV/bin/pip install -r requirements.txt`
10. `pip install .` or `python setup.py install` (or the full path to correct pip and python)
11. Check: `conda list` should give you the list of packages installed in you environment
12. `cd matscholar-core`
13. `pip install -r requirements.txt` (or full path to pip in env)
14. `python setup.py install`
15. To be able to pull from the main repo: `git add remote upstream https://github.com/materialsintelligence/matscholar-core.git`
16. Add the following enviornment variables: 
```
export ELASTIC_HOST='<elasticsearch host>'
export ELASTIC_PASS='<elasticsearch password>'
export ELASTIC_USER='elastic_read_only'
export S3_BUCKET_NAME='materialsintelligence'
export MATERIALS_SCHOLAR_API_KEY='<api_key>'
```
17. When finish, return to you base environment: `conda activate`

## Committing changes
1. `git add .`
2. `git commit -m "I made such and such changes."`
3. `git push origin master`
    * `origin` is the default git remote alias for your fork
    * `master` is the default branch
4. Go to the page of your fork on github and create a pull request to the main repo on materialsintelligence

## Running the tests
1. Make sure you have [`pytest`](https://pytest.org) installed
2. Run `python -m pytest` from the root directory

## Changelog

- v0.0.12 (Dec 13, 2018)
    - Materials Summary and Entity Search Functionality
    - Materials Map Functionality (2D and 3D)

- v0.0.11 (Dec 12, 2018)
    - Dockerfile and other code for deployment of API on AWS ECS service
    
- v0.0.10 (Dec 3, 2018)
    - PreProcessResource for preprocessing text + corresponding tests
    - EmbeddingResource for requesting word embeddings, or an embedding matrix for a list of words/phrases

- v0.0.9 (Nov 29, 2018)
    - MatSearchResource and CloseWordsResource accept negative words
    - MentionedWithResource, checking if a material is mentioned with a list of keywords
    - test coverage for word2vec processing
    - test coverage for close_words and mentioned_with

- v0.0.8 (Nov 27, 2018)
    - fixed MatSearchResource
    - test coverage for matsearch RESTful API

- v0.0.7 (Nov 27, 2018)
    - Full test coverage for word embeddings

- v0.0.6 (Nov 26, 2018)
    - Full test coverage for annotation
    - Added a test for AuthConnection

- v0.0.5 (Nov 24, 2018)
    - Added MANIFEST.in to package the model files with the module installation
    - Added tests for annotation
    - Fixed a bug in annotation (POS tags when creating phrases)

- (Nov 2, 2018)
    - Optimizing EmbeddingEngine for API using using pymagnitude library
    - Added tests for EmbeddingEngine
    - Still to do: final two functions in word_embeddings.py need tests + modifications


- v0.0.4 (Oct 11, 2018)
    - Added api code
        - added AuthConnection to database.connections.py
        - need to write api tests
        - added API dependencies to requirements.txt
    - Added search code
        - search still needs to be refactored
    - Added collect code
    - Added __init__.py for search
    - Fixed various bugs that popped up when trying to start up API server

- v0.0.3 (Oct 11, 2018)
    - Solved DataPreparation deaccenting issue (does not happen now if it is a single character)
    - annotation_metrics test now pass

- v0.0.2 (Oct 3, 2018)
    - Added annotation
        - missing tests, and the existing annotation metrics test is failing
    - Added nlp/word_embeddings
        - need tests
    - Added processing/word2vec, parsing, utils
        - need tests
        - need to unify the various parsers

- v0.0.1 (Oct 3, 2018)
    - Added database connection functionality with tests
