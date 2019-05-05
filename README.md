# Ngxin logs for humans

This Python script applies the format in columns for easier viewing

## Example

ssh user@machine "docker logs nginx -f --tail=40" | python .

ssh user@machine "tail -f /var/log/nginx/visit.log" | python .

```
 200 5.188.210.58     05/May/2019:08:31:29 +0000 [GET]/index.php/sistemas-mac-osx/                            2 [500] 2 [404] http://xxxxxx.com/index.php/sistemas-mac-osx/
 200 5.188.210.58     05/May/2019:08:31:29 +0000 [GET]/index.php/2019/01/                                     2 [500] 2 [404] http://xxxxxx.com/index.php/2019/01/
 301 5.188.210.58     05/May/2019:08:31:30 +0000 [GET]/index.php/2019/01/index.php                            2 [500] 2 [404] http://xxxxxx.com/index.php
 301 5.188.210.58     05/May/2019:08:31:31 +0000 [GET]/index.php/2019/01/index.php                            2 [500] 2 [404] http://xxxxxx.com/index.php
 301 5.188.210.58     05/May/2019:08:31:32 +0000 [GET]/index.php/2019/01/index.php                            2 [500] 2 [404] http://xxxxxx.com/index.php

```