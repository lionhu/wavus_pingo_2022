NUXT Frontend
1. Sass division problem
warning: Using / for division is deprecated and will be removed in Dart Sass 2.0.0.
Recommendation: math.div(4em, 3)
More info and automated migrator: https://sass-lang.com/d/slash-div

--> solution
 sass-migrator division **/*.scss



Elasticsearch
1. API error due to indices problem

--> solution
 python manage.py search_index --rebuild
