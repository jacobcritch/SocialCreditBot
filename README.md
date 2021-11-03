# SocialCreditBot

## Installation
1. Clone/Download this repo.

2. `cd` to the directory and run `pip install -r requirements.txt`

3. Create a bot using the 'BotFather' in Telegram, and make note of your access token.

4. Rename `sample_config.json` to `config.json`, and `sample_db.json` to `db.json`

5. In `config.json`, add in the access token you got from the BotFather. I.e `token: "MYTOKENHERE"` (**NOTE: DO NOT COMMIT OR SHARE YOUR PERSONAL TOKEN**)

6. In `db.json`, make any changes you want to the initial database (more names, different values, etc.).

7. Modify the `leaderUsernames` dictionary to assign who gets ultimate power.

8. Change the filepaths to reflect your working directory.

9. Run `python3 echobot.py`.

10. Test out the bot by talking to it in a Telegram chat.
