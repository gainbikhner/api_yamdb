# YaMDB

## Описание

База отзывов пользователей о фильмах, книгах и музыке. Произведения делятся на категории, произведению может быть присвоен жанр из списка предустановленных. Добавлять произведения, категории и жанры может только администратор. Пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти; из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. На одно произведение пользователь может оставить только один отзыв. Пользователи могут оставлять комментарии к отзывам. Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

### Авторы

- https://github.com/gainbikhner
- https://github.com/Jultokm
- https://github.com/PIEJIN

### Стек технологий

- Django
- Django filters
- DRF
- JWT

### Документация API

http://127.0.0.1:8000/redoc/

## Инструкция

### Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/gainbikhner/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

Создать юзера для админки:

```
python3 manage.py createsuperuser
```

## Примеры

### Запросы к API

Регистрация:

```
http://127.0.0.1:8000/api/v1/auth/signup/
```

```
{
  "email": "user@example.com",
  "username": "string"
}
```


```
http://127.0.0.1:8000/api/v1/auth/token/
```

```
{
  "username": "string",
  "confirmation_code": "string"
}
```

Получить список всех произведений:

```
http://127.0.0.1:8000/api/v1/titles/
```

```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "string"
        }
      ],
      "category": {
        "name": "string",
        "slug": "string"
      }
    }
  ]
}
```

Оставить отзыв:

```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```

```
{
  "text": "string",
  "score": 1
}
```
