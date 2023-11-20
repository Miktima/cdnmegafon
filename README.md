# CDN Megafon
## Django site for Megafon CDN API
### Утилиты для работы с CDN Megafon
Авторизация происходит с помощью APIKey

**Список проектов CDN** Выводится номер проекта (ID), описание (название) проекта, источник (Origin) и список CDN адресов через ";"

**Получение статистики трафика через API.** Для получения статистики трафика (переданный объем трафика CDN) необходимо выбрать портал и период. 
Гранулярность разбиения выбранного периода выбирается автоматически. Выводятся данные по трафику от CDN серверов до конечных пользователей 

**Получение метрик трафика через API.** Для получения метрик трафика портала необходимо указать портал, период и метрики (можно несколько). 
Разбиение периода происходит автоматически в зависимости от его длительности с учетом максимально возможного разбиения в 1440 точек (ограничение API CDN). Список метрик:
- upstream_bytes — to get traffic in bytes from the source to the CDN servers or from the source to the shielding
- sent_bytes — to get traffic in bytes from CDN servers to the end users
- shield_bytes — to get traffic in bytes from shielding to CDN servers
- total_bytes — to get the sum of shield_bytes, upstream_bytes and sent_bytes traffic
- cdn_bytes — to get the sum of sent_bytes and shield_bytes traffic
- requests — to get the number of requests to the CDN servers
- requests_waf_passed — to get the number of requests that were processed by the Basic WAF option
- responses_2xx — to get the number of 2xx HTTP response status codes
- responses_3xx — to get the number of 3xx HTTP response status codes
- responses_4xx — to get the number of 4xx HTTP response status codes
- responses_5xx — to get the number of 5xx HTTP response status codes
- responses_hit — to get the number of responses with the HTTP header Cache: HIT
- responses_miss — to get the number of responses with the HTTP header Cache: MISS
- response_types — to get the statistics by content type. Returns a number of responses for content with different MIME types
- cache_hit_traffic_ratio — to get the amount of cached traffic. It is calculated by the formula: one minus upstream_bytes divided by sent_bytes. We subtract the non-cached traffic from the total traffic
- cache_hit_requests_ratio — to get the amount of cached content that is sent. It is calculated by the formula: responses_hit divided by requests
- shield_traffic_ratio — to get the efficiency of shielding: how much more traffic is sent from shielding rather than from the source. It is calculated by the formula: (shield_bytes minus upstream_bytes) divided by shield_bytes
- image_processed — to get the number of images processed by the Image optimization option

**Проверка загрузки изображений через CDN.** В поле Page URL требуется ввести URL тестируемой страницы портала Sputnik, в поле CDN on the page - домен CDN, используемый на тестируемой странице. 
Домен CDN можно получить, открыв исходный текст тестируемой страницы. Например, 
в ссылке на изображение https://`cdn1.img.sputniknews.com.tr`/img/07e7/01/0d/1065715712_0:0:1536:864_1920x0_80_0_0_a64c0583379bdf20f66e30fbbc5be8c1.jpg.webp выделен домен CDN.
Если поле New CDN оставить пустым, то проверка загрузки избражений происходит по домену CDN из тестируемой страницы. 
Если указать новый CDN домен в поле New CDN, то все ссылки из тестрируемой страницы, использующие старый CDN, будут проверены на новом домене
В результате выводятся ссылки на страницы с ошибкой 404 и процент ошибок

**Анализ логов CDN.** Вывод агрегированных значений логов CDN-ресурсов. Можно просмотреть основные данные за последние 3 дня. Интервал данных в одном запросе 6 часов. Время - UTC. 
У фильтров status и size расширенное число операторов и можно устанавливать значения, ограниченные диапазоном. Размерность поля size - байты. 
Чекбокс у фильтра позволяет вывести соответствующий аггрегированный график. 
Если ни один график по фильтру не выбран, выводятся агрегированные графики по запрошиваемому ресурсу и user-agent

**Сведения о DNS домена и HTTP заголовках.** В поле Domain требуется ввести адрес домена, например, sputniknews.com.tr в поле CDN - домен CDN, (если несколько - через запятую), 
например, cdn1.img.sputniknews.com.tr.
В результате выводятся сведения о домене и HTTP заголовки

**Очистка кеша CDN.** Маски очистки кеша:
- Если параметр пустой, то очищается весь кеш
- Можно указать одну маску /img/* Из кеша будут удалены все файлы, начинающиеся на /img/ (/img/one.jpg, /img/two.jpg).
- Можно указать несколько масок через запятую /img/*, /video/* Из кеша будут удалены все файлы, начинающиеся на /img/ и /video/
  (/img/one.jpg, /img/two.jpg, /video/one.mp4, /video/video.avi и т.п.).
- Если указать маску без *, то из кеша будет удалён только файл с url, строго совпадающий с маской. К примеру, masks=/img/my_super_image.jpg?id=8193737182253
  Из кеша будет удалён файл, url которого строго совпадает с /img/my_super_image.jpg?id=8193737182253.
