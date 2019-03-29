# Twitter Sentiment Analysis
Exemplary analysis derived from the [nice blog series](https://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/) by [Marco Bonzanini](http://marcobonzanini.com/) (licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/))

In the blog posts the code is embedded in chunks inside the text which is great for educational purposes.
Here are two scripts created by combining and adjusting the code chunks.
It also includes a json file of about 3000 tweets with hashtag Trump captured on 2019-03-28 during roughly one hour.

## Capturing tweets
You may skip this step if you just want to play around with the (very small) example dataset.
In order to capture tweets for your own analysis you need to install the python module [tweepy](https://www.tweepy.org/) adjust [stream.py](stream.py).
Insert your Twitter `consumer_key`, `consumer_secret`, `access_token`, and `access_secret`.
Additionally you might want to adjust the output filename in line 21 and the filter in line 33.
Then you can execute:

```bash
python stream.py
```

This will capture all tweets meeting your filter criterion in the json file.

## Basic sentiment analysis
In order to do the basic sentiment anslysis on the captured tweets you need to install the python module [nltk](https://www.nltk.org/).
If you want to use anything but the example dataset you also have to adjust [sentiment.py](sentiment.py).
Set the correct filename in line 15. You can also change the number of words shown or the list of words you are particularly interested in.
When you are done run the script as:

```bash
python sentiment.py
```

This will print:
 - Most common words
 - Most common co-occurences
 - Most positive words
 - Most negative words
 - Semantic orientation of some specific words (wall, canada, mexican, guns, free)
 
Example output:

```
Most common words:
[('#trump', 1690), ('#maga', 276), ('trump', 238), ('@realdonaldtrump', 214), ('one', 214), ('#gop', 182), ('@olivermcgee', 181), ('campaign', 177), ('look', 177), ('message', 174)]

Most common co-occurences:
[(('❤', '️'), 1089), (('border', '👇'), 234), (('🇸', '🇺'), 180), (('asst', 'former'), 174), (('former', 'u'), 174), (('former', 'prosecuted'), 174), (('former', 'passing'), 174), (('former', 'secret'), 174), (('attorney', 'former'), 174), (('fbi', 'former'), 174)]

Most positive words:
[('1', 7.515699838284043), ('crime', 6.894817763307944), ('arrest', 5.087462841250339), ('created', 5.087462841250339), ('break', 4.087462841250339), ('committing', 4.087462841250339), ('defamation', 4.087462841250339), ('fomenting', 4.087462841250339), ('dramatically', 4.087462841250339), ('disgust', 4.087462841250339)]

Most negative words:
[('another', -15.428491035332247), ('continue', -16.179909090014934), ("i'll", -16.936637939002573), ('c', -17.51975909289956), ('9', -18.349834091457247), ('democrats', -19.037890085142507), ('11', -19.09877232728953), ('donald', -19.609640474436812), ('america', -25.798974363820953), ('back', -27.179909090014934)]

Semantic orientation of some specific words
wall: 0.000000
canada: -8.027906
mexican: 0.000000
guns: -6.906891
free: -6.857981
```

## A final note
The two scripts are the result of quick copy and paste.
Not much effort was used to clean things up or to generalize (e.g. use parameters instead of changing the source code each time).
If you find them useful and want to improve them, your pull requests are very welcome :)
