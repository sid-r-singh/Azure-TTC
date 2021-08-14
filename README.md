# 🎚 Azure-TTC (educational project)
This repo contains code for a Azure function written in Python. TTC stands for telemetry, tracking & control. The function is based on HTTP trigger i.e. it is invoked when a HTTP request is made to the function's URL. 

## 📄 Details

### ❏  When is the function invoked ?
  A Telegram 🤖 (bot) written in Python is deployed on Heroku which carries out conversation with user. The bot is programmed to extract the following parameters:
  - which program to run 
  - how many iterations of it
  Upon confirmation from the user, this info. is delivered to this function via HTTP Post request.

### ❏ What is the role of this serverless function ?
It has 2 main roles:
- **Telemetry** : receives information from a Telegram bot (installed on Heroku) & then takes further action based on the inputs.
- **Control** : the function controls the execution of Monte-Carlo program. After vefying that all inputs are valid (checking for spam), it allows the execution of the main (Monte-Carlo) program.

### ❏ Why is this an educational project ?
The final program runs on GitHub action, which is called via GitHub REST API. Since GitHub doesn't recommend calling GitHub action from serverless function, it should not be done in a production environment. Thus this project serves as an exmple where one can possibly learn how to run the program in his/her VM.
