# filmy_bot
Данный бот принимает ссылку на фильм от пользователя, парсит контент и постит в канал.

python <= 3.7.0

# Install
```
git clone https://github.com/Doka-hub/vkusvill.git
pip install -r requitements.txt
```
- ## Linux ( create .env )
  ```
  touch .env
  ```
- ## Windows ( create .env )
  ```
  copy con .env
  CTRL-Z
  ```
  ### .env
  ```
  API_ID=TELEGRAM_API_ID
  API_HASH=TELEGRAM_API_HASH
  BOT_TOKEN=BOT_TOKEN
  ADMIN=ADMIN_USERNAME
  CHANNEL=CHANNEL_ID
  ```
# RUN
```python bot.py```
