# Botsu

Welcome to Botsu! 🤖

This repository contains Peanuts.
Peanuts is powerful Discord bot is built using the Hata library.

## Features

- **Moderation Commands:** Keep your server in check with commands for muting,
kicking, and banning members, as well as managing roles and channels.

- **Utility Commands:** Make your server more interactive and informative with
utility commands that provide information about users, roles, channels, and
servers, and perform actions like sending messages, creating polls, and setting reminders.

- **Custom Features:** Tailor the bot to suit your server's unique needs with
custom commands, automated tasks, and event handlers.

## Why Hata Discord Bot?

- **Easy-to-use:** Hata Discord Bot is built using the Hata library, which\
provides a simple and intuitive way to interact with the Discord API.

- **Powerful and Flexible:** With a wide range of built-in functionalities and\
customization options, you can easily configure the bot to fit your server's requirements.

- **Open-source and Community-driven:** Hata Discord Bot is open-source, meaning\
you can freely modify and distribute it. Contributions from the community are\
encouraged and welcome!

## Getting Started

To get started with Botsu using Poetry, follow these simple steps:

1. Clone this repository to your local machine.
2. Install Poetry, the Python package manager, by following the instructions at [https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation).
3. Navigate to the cloned repository directory in your terminal.
4. Run the following command to install the dependencies:

    ```bash
    poetry install
    ```

5. Create a new bot account on the Discord Developer Portal and obtain the bot token.
6. Create a .env file in the repository directory with the following format:

    ```py
    PEANUTS_BOT="some discord key"
    ```

    Replace "some discord key" with your actual bot token.

7. Run the bot using Poetry's virtual environment:

    ```bash
    poetry run python main.py
    ```

## Contributing

We welcome contributions to Botsu! If you find any issues, have suggestions for\
improvements, or want to add new features, you can submit a pull request or\
open an issue on the GitHub repository. Please follow the established coding\
conventions, document your changes, and thoroughly test your code before\
submitting a pull request.

## License

Hata Discord Bot is open-source and available under the [MIT License](LICENSE).\
Feel free to use, modify, and distribute it according to the terms of the license.\
Join us and take your Discord server to the next level with Hata Discord Bot! 🚀
