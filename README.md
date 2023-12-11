# Webhook Plan | Get Job Execution Reminders via Webhook

Welcome to the Webhook Plan repository! This is the core logic behind Webhook Plan, a powerful tool for effortless job scheduling and webhook management.

## Features

🤩 **Easy Scheduling:** Schedule your jobs with ease using Webhook Plan.

⏱️ **Reliable Execution:** Ensure your jobs are executed reliably and on schedule.

🪝 **Webhook Management:** Manage and customize webhook requests effortlessly.

🚀 **Scheduling Options:** Choose from wide verity of schedules -

- **Interval:** Schedule executing on a regular interval
- **Crontab:** Timezone Aware Crontab-like schedule
- **Solar:** Schedule following astronomical patterns
- **Clocked:** Schedule executing at a clocked time

## Usage

To use production ready **WebhookPlan** on your project, just follow the steps -

1. Use the following `docker-compose.yaml` template to run a dummy WebhookPlan instance.

   ```yaml
   version: "3"

   services:
   redis:
     image: redis/redis-stack:latest
     restart: on-failure

   postgres:
     image: postgres:alpine
     env_file:
       - .db.env
     restart: on-failure

   webhookplan:
     image: webhookplan/webhookplan:latest
     container_name: webhookplan
     env_file:
       - .env
     ports:
       - "8000:8000"
     depends_on:
       - postgres
       - redis
     restart: on-failure

   webhookplan_celery_worker:
     image: webhookplan/webhookplan:latest
     command: sh -c "celery -A core.celery worker"
     env_file:
       - .env
     depends_on:
       - postgres
       - redis
     restart: on-failure

   webhookplan_celery_beat:
     image: webhookplan/webhookplan:latest
     command: sh -c "celery -A core.celery beat -S django"
     env_file:
       - .env
     depends_on:
       - postgres
       - redis
     restart: on-failure
   ```

2. Make sure to use the `example.env` `example.db.env` templates to prepare `.env` and `db.env` respectively.

   .env

   ```.env
   # django
   SECRET_KEY='django-insecure-_m4t+w29x^5$&7n$8+!x_e0&=qr5yej$7mpg^5*ummb=)q(6x!'

   # database
   DB_NAME='postgres'
   DB_USER='postgres'
   DB_PASSWORD='postgres'
   DB_HOST='postgres'
   DB_PORT='5432'

   # redis
   CELERY_BROKER_URL='redis://redis:6379'

   # jitter
   JITTER_MAX_RETRIES='27'
   JITTER_RETRY_BACKOFF='1'
   JITTER_RETRY_BACKOFF_MAX='576'
   JITTER_RETRY_JITTER='0'
   ```

   .db.env

   ```db.env
   # postgres
   POSTGRES_USER='postgres'
   POSTGRES_PASSWORD='postgres'
   POSTGRES_DB='postgres'
   PGDATA='/var/lib/postgresql/data/pgdata'
   ```

   Feel free to update these configurations at your convenience.

3. Once these 3 files are ready, you are good to go. Open the terminal and write the following command to run the docker containers.

   ```sh
   $ docker compose up --build
   ```

4. Open [127.0.0.1:8000/swagger](http://127.0.0.1:8000/swagger/) in your browser. 🚀

   ![WebhookPlan API Documentation](./assets/images/383b36ca-549d-4eb6-b1f2-19d88050a758.png "WebhookPlan API Documentation")

5. Schedule your webhooks using `/schedules/` (POST) end-point.

   ![WebhookPlan createing a schedule](./assets/images/b0c4b9fb-ab86-4e0b-801c-c6d6210bac0f.png "WebhookPlan createing a schedule")

   - Use the following JSON to schedule a Task -

     ```json
     {
       "name": "Get webhook request to webhook.site",
       "description": "Every 10 seconds, get webhook requests to webhook.site",
       "interval": {
         "every": 10,
         "period": "seconds"
       },
       "webhook": {
         "url": "https://webhook.site/31c7aa21-62d0-48eb-b17f-6aa0a00a4649",
         "method": "POST",
         "payload": {
           "action": "webhook.generate_account_summary",
           "data": {
             "user_id": 101,
             "account_number": "8397496349234356"
           }
         },
         "headers": {
           "Content-Type": "application/json",
           "Authorization": "Basic eyJ1c2VyX2lkIjogMTAxLCAibmFtZSI6ICJKb2huIERvZSIsICJlbWFpbCI6ICJqb2huLmRvZUB3ZWJob29rcGxhbi5jb20ifQ=="
         }
       }
     }
     ```

     **NOTE:** Use [webhook.site](https://webhook.site/) for the testing/debuging purpose.

   - Hitting Execute, you'll see a Schedule has been created

   ![WebhookPlan createing a schedule](./assets/images/866ba124-9568-4caf-8783-daeba7a8801f.png "WebhookPlan createing a schedule")

   - Open [webhook.site](https://webhook.site/). You'll see, Requests are now coming in the timely manner.

   ![WebhookPlan example](./assets/images/7abc3b23-6db7-4adb-9711-fc0187b9bb65.png "WebhookPlan createing a schedule")

## Contribution 🤝

To contribute to Webhook Plan, follow these steps:

1. **Fork the Repository:** Click the 'Fork' button in the top right of this repository to create your own copy.

2. **Clone Your Fork:** Clone the repository to your local machine using `git clone`.

   ```bash
   git clone https://github.com/<your-username>/webhookplan.git
   ```

3. **Create a Branch:** Create a new branch for your feature or bug fix.

   ```bash
   git checkout -b feature-name
   ```

4. **Make Changes:** Implement your changes and test thoroughly.

5. **Commit and Push:** Commit your changes and push to your forked repository.

   ```bash
   git commit -m "Your meaningful commit message"
   git push origin feature-name
   ```

6. **Submit a Pull Request:** Open a pull request to the main Webhook Plan repository.

<!-- ## Contribution Guidelines

- Follow the [Code of Conduct](CODE_OF_CONDUCT.md).
- Check the [Contribution Guidelines](CONTRIBUTING.md) for detailed information. -->

## License

Webhook Plan is licensed under the [BSD 3-Clause License](LICENSE).

---

Feel free to contribute, and thank you for being a part of the Webhook Plan community!
