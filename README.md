# auth_form

### Описание
Приложение работает на виртуальной машине (yandex cloud), по адресу https://authdomen.website/ (https://authdomen.website/admin/ - админка).   
Операционная система - Ubuntu 18.04 LTS Bionic.  
Получен SSL сертификат и настроено под https (утилита certbot). 
Веб серверы: настроена связка Nginx + Uwsgi.   
СУБД: PostgreSQL 12.   
Деплой: пока что вручную, перезагрузкой воркеров uwsgi, обновлением репозитория на сервере.

### Возможности   
Регистрация/логин пользователя, валидация полей формы, регистрация/логин при нажитии на FACEBOOK или    
GOOGLE (возможно открытие отдельного окна авторизации, либо без, при повторном нажатии). После авторизации пользователя   
в системе - форма будет скрыта, у неавторизванного - будет отображаться.   
После регистрации пользователя - он автоматически авторизуется.
При регистрации через соцсети - пользователю на емэйл (который из соцсетей) высылаются данные для входа    
(имя, фамилия, пароль).

В последнем релизе была расширена модель пользователя галочкой о получении новостей, идет ее запись в соответствующее    
поле, в админке пользователя - добавлено инлайном соответствующее поле.

#### P.S
Возможны 502-е ответы, т.к. была выбрана прерываемая   
конфигурация машины с целью экономии :)

##### P.P.S.
Возможны проблемы с запуском репозитория из за отсутствия файла local_settings.py и неопходимых настроек а так-же работы кнопок соц-сетей, т.к. там требуется SSL сертификат и внешний домен.
