# Web Crawler
**Веб-краулер** — программа, перебирающая веб-страницы и сохраняющая с этих страниц данные и медиафайлы. 

Взаимодействие с утилитой происходит с помощью CLI через командную строку. 

### **Как начать перебор страниц:** 
1. Перейдите в директорию, куда установлена программа с помощью команды cd;
2. В командной строке пропишите: \
`python CLI.py --scan <URL> ` или ` python CLI.py -s <URL> `  \
Если необходимо, добавьте дополнительные флаги. 
3. Программа запустится. Начнется вывод сообщений об обрабатываемых веб-страницах: \
`YYYY-mm-dd HH:MM:SS [Bot N] Веб-краулер сохраняет: <URL>` \
`YYYY-mm-dd HH:MM:SS Загрузка содержимого страниц закончена.`
4. После сообщения об окончании обработки проверьте директорию, которая была выбрана для сохранения обработанных веб-страниц. 

Список дополнительных флагов: 
```Options:
  -s, --scan TEXT      URL сканируемого сайта или файл .txt с несколькими URL-
                       амиПример: --scan https://example.com или --scan
                       urls.txt  [required]
  -d, --depth INTEGER  Глубина сканирования ресурса  [default: 3]
  -p, --path TEXT      Директория для скачивания файловПример: --path
                       C:/Users/User/directory
  -b, --bots INTEGER   Количество ботов для обхода  [default: 4]
  --help               Show this message and exit.
```

Автор: Соколова Татьяна