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

## Database Model

| Table | Description |
|---|---|
| `usuarios` | Telegram users registered as salon customers |
| `empleados` | Salon employees and their specialities |
| `servicios` | Beauty services with price and duration |
| `disponibilidad_empleado` | Employee availability time ranges |
| `citas` | Appointments linked to users, services, and employees |
| `faq` | Frequently asked questions used by the AI assistant |
| `solicitudes_contacto` | Human support requests created from the bot |

---

## Booking Flow

```text
/book
  -> Show available services
  -> User selects a service
  -> System generates available time slots
  -> User selects a slot
  -> System shows booking summary
  -> User confirms
  -> Appointment is saved in the database
```

The system uses employee availability and existing appointments to avoid double bookings.

---

## AI Assistant

The AI assistant is powered by Ollama.

It uses database context from:

- FAQs
- Services
- Employees
- Upcoming availability

The assistant only answers using available business information and does not modify the database.

---

## Human Support

Users can request human support using:

```text
/contacto_humano
```

The request is saved in the database with a pending status.

---

## Project Purpose

This project demonstrates how a small beauty salon can improve its digital maturity by automating repetitive administrative tasks.

Main benefits:

- Fewer phone calls
- Easier appointment booking
- Better customer experience
- Reduced scheduling errors
- Centralised customer and appointment data
- AI-assisted customer support