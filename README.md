# SalonFlow — Telegram Bot for Beauty Salons

SalonFlow is a Telegram bot designed to automate appointment management for a beauty salon. It reduces phone calls, allows customers to book appointments online, and includes an AI assistant that answers common customer questions.

The project is designed as a digital transformation solution for small and medium-sized businesses in the beauty sector, aligned with the objectives of the Kit Digital programme.

---

## Features

| Command | Description |
|---|---|
| `/start` | Welcome message and user registration |
| `/help` | Shows the full list of commands |
| `/servicios` | Displays the service catalogue with prices and duration |
| `/book` | Starts the appointment booking flow |
| `/mis_citas` | Shows the user’s upcoming appointments |
| `/cancel` | Cancels a future appointment |
| `/contacto_humano` | Requests human support from the salon team |

Free text messages are processed by an AI assistant using Ollama. The assistant uses real business context from the database, including FAQs, services, employees, and availability. The AI assistant only provides answers and never writes data to the database.
