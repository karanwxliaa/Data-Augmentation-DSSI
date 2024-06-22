KinNews: Kinyarwanda News Classification Dataset

Version 1, Updated 02/10/2020


LICENSE

The copyrigth of the news articles belongs to the orginal news sources.

DESCRIPTION

The KinNews dataset is collected from 20 news source in total,  15 news websites and 5 newspapers from Rwanda. It contains a total of 21268 news articles which are distributed across 14 classes.
These classes are listed in classes.txt. It has a raw version and a preprocessed (cleaned) version which are both divided in 17,014 articles for the train set and 4254 for the test set. 

The files train.csv and test.csv for the raw version contain samples as comma-sparated values. 
There are 6 columns in them, corresponding to class index (1 to 14), English labels (en_label), Kinyarwanda labels (kin_label), url, title and content. 

The files train.csv and test.csv for the cleaned version also contain samples as comma-sparated values. 
However,there are 3 columns in them, corresponding to class index (1 to 14), title and content.