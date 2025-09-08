<h1 align="center">Welcome to InvBinderBot 👋</h1>
<p>
  <a href="https://github.com/1minEpowMinX/InvBinderBot#readme" target="_blank">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" />
  </a>
  <a href="https://github.com/1minEpowMinX/InvBinderBot/blob/dev/LICENSE" target="_blank">
    <img alt="GitHub License" src="https://img.shields.io/github/license/1minEpowMinX/InvBinderBot">
  </a>
  <a href="https://dependabot.com/" target="_blank">
    <img alt="Dependabot" src="https://badgen.net/badge/Dependabot/enabled/green?icon=dependabot">
  </a>
</p>

> Telegram bot for automating work with MAC addresses and unique device names. Used in corporate infrastructure to simplify administration, including through integration with Kubernetes.

## ✨ Features

* Binding unique names to MAC addresses.
* Processing DHCP logs with new MAC uploads.
* User authorization.
* FSM scripts for step-by-step data binding.
* Storing data in Redis.
* Logging user actions.
* Support for Kubernetes manifests for deployment.
* Docker containerization and CI/CD via GitHub Actions.

## 🛠️ Built With

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=yellow)
![Redis](https://img.shields.io/badge/Redis-DC382D?logo=redis&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326ce5?logo=kubernetes&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ed?logo=docker&logoColor=white)

## ⚙️ Install

```sh
git clone https://github.com/1minEpowMinX/InvBinderBot.git
cd InvBinderBot
pip install -r requirements.txt
```

## 🔧 Configuration

Before starting, you need to configure the environment:

1. Configure the enviroment variables in .env (based on `.env_example`):
2. Configure the list of users in authorized_users.json (based on `data/authorized_users.example.json`):

📝 Note: To work through Kubernetes, you need to do the same for Secrets and ConfigMaps files.

## 🚀 Usage

### Local

```sh
python main.py
```

### Kubernetes

```sh
kubectl apply -f k8s/bot
kubectl apply -f k8s/redis/
```

📝 Note: In some deployments (e.g., corporate infrastructure), additional services such as Samba shares may be used. These are optional and not required for running the bot itself.

## 📘 Author

👤 **Kirill Bitskyi**

* Github: [@1minEpowMinX](https://github.com/1minEpowMinX)
* LinkedIn: [@Kirill Bitskyi](https://www.linkedin.com/in/kirill-bitskyi-025672284/)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/1minEpowMinX/InvBinderBot/issues).

## 📝 License

Copyright © 2025 [1minEpowMinX](https://github.com/1minEpowMinX).<br />
This project is [MIT](https://github.com/1minEpowMinX/InvBinderBot/blob/dev/LICENSE) licensed.
