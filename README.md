# SlackScrapper

The name may be a little confusing since it is not really a slack scrapper nor a web scrapper. However, it's primary use is to scrap a specific web page. But it is not limited to it. Basically, it's a collection of python script that notify their result (success or failure or other) by posting them inside a slack organization. 

## One recurring task

The purpose of those script are to be run every day (or on a specific time) so the use of systemctl might b usefull. You might have to create a `service` and a corresponding `timer`

## docker

every thing should run inside docker. But be carefull since you need some env variable for the different account you may use. Those have to be passe with `--build-arg` (but I will certainly move it to be used with an `env` file or something else since the number of environment variable migh sky rocket in the future.

## Correction

There are some typo in the strings  used. They will be corrected. 
