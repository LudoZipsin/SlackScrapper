# SlackScrapper

The name may be a little confusing since it is not really a slack scrapper nor a web scrapper. However, it's primary use is to scrap a specific web page. But it is not limited to it. Basically, it's a collection of python script that notify their result (success or failure or other) by posting them inside a slack organization. 

## One recurring task

The purpose of those script are to be run every day (or on a specific time) so the use of systemctl might b usefull. You might have to create a `service` and a corresponding `timer`

this is the content of my `/etc/systemd/system/PacktpubFreelearning.service`:
```
[Unit]
Description=Fetch the daily ebook from packtpub free learning program

[Service]
Type=oneshot
ExecStart=/usr/bin/sh -c 'docker run --rm slack-scrapper:latest -m PacktPubActionner -a fetch_free_learning'
```

and the content of `/etc/systemd/system/PacktputFreelearning.timer`:
```
[Unit]
Description=Run the service every 24h00

[Timer]
OnCalendar=*-*-* 05:00:00
```

just activate it with:
```
sudo systemctl start PacktpubFreelearning.timer
```

and every day your free ebook should be downloaded with a notification on your slack channel.

## docker

every thing should run inside docker. But be carefull since you need some env variable for the different account you may use. Those have to be passe with `--build-arg` (but I will certainly move it to be used with an `env` file or something else since the number of environment variable migh sky rocket in the future.

## Correction

There are some typo in the strings  used. They will be corrected. 
