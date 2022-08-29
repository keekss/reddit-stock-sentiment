# Reddit Sentiment and Stock Price

## Overview

The first part of this project is a python notebook consisting of a pipeline to get content from Reddit and the stock market, perform sentiment analysis on the content, then graph the two datasets. This notebook is fairly robust - each process takes in an iput file and writes to an output file, allowing you to enter the pipeline at any point and checkpoint as you go. 

All of the necessary code for this can be found in [this notebook](https://github.com/keekss/ics-484-final/blob/main/Reddit_Sentiment_vs_Stock_API.ipynb), which can be run as a Jupyter notebook on a local machine or through Google Colab. It was originally developed in Google Colab, so if the size of the dataset you wish to work with is small enough to run in Google Colab, that platform might be best. NOTE: every time this notebook is restarted in Google Colab, all of the pip installations need to be rerun. 

The final section of the notebook contains driver code to reconstruct our sample graphs using prepared data files, which can be found in the [sampleData](https://github.com/keekss/ics-484-final/tree/main/sampleData) directory. These graphs get posts and comments from [r/disney](https://www.reddit.com/r/disney/) and plots their sentiment alongside Disney stock. 

To smooth the sentiment analysis results, an API called [ASAP](https://dawn.cs.stanford.edu/2017/08/07/asap/) was used. This was written python2, so the modified version of this that we used can be found [here](https://github.com/keekss/ics-484-final/blob/main/ASAP.ipynb). 

## Plotly Website

The results from the Reddit Sentiment and Stock Price notebook above has been included in a plotly website (coded in Python using Dash). We also included a bar graph depicting which Disney characters were discussed the most on the r/Disney subreddit, as well as an interactive map of Disneyland with each ride's sentiment (taken from r/Disneyland) being displayed. 

In order to access the website, the python application must be running. This can be done by cloning this repository locally: 

```
git clone git@github.com:keekss/ics-484-final.git
```

After cloning, navigate into the repository's directory:

```
cd ics-484-final
```

Finally, run the python program (note: make sure python3 is installed on your computer):

```
python3 app.py
```

Alternatively, you can email <clark37@hawaii.edu> to schedule a viewing.
