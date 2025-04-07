
### 1. **Клонирование репозитория**

```bash
git clone https://github.com/ваш-репозиторий.git
cd ваш-репозиторий
```

---

### 2. **Сборка Docker-образа**

```bash
docker build -t ваше-приложение .
```

Для docker-compose (другого нет)
```bash
docker-compose build
```

---

### 3. **Запуск приложения**
Чтобы запустить контейнер
```bash
docker run -p 5000:5000 ваше-приложение
```
Для `docker-compose`:
```bash
docker-compose up
```

---

### 4. **Переменные окружения (если нужны)**
Есть раздел с примером `.env` в докер конфиге (compose, file), можете вставить свои
Например:
```env
DATABASE_URL=mysql://user:password@db:3306/mydatabase
DEBUG_MODE=True
```

---


### 7. **Проверка работоспособности**
Укажите, как убедиться, что приложение запустилось:
```bash
curl http://localhost:5000
# Или откройте в браузере http://localhost:5000
```

---
шаблоны html,css делал гпт (кто их вообще пишет вручную)
