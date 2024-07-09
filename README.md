### NFT Gating Repository

#### Overview
This repository contains a project for implementing NFT gating functionality. The project includes various components such as API services, a database, Docker configurations, and a Telegram integration.

#### Features
- **API**: Provides endpoints for managing NFT gating operations.
- **Database**: Scripts for setting up and managing the database.
- **Docker**: Configuration files for containerizing the application.
- **Telegram**: Integration with Telegram for notifications or commands.

#### Setup Instructions

1. **Clone the Repository**
   ```sh
   git clone https://github.com/Alexandr0856/nft_gating.git
   cd nft_gating
   ```

2. **Environment Variables Configuration**
   - Navigate to the `environments` directory and create a `telegram.env` file.
     
     ```env
     BOT_TOKEN=your_telegram_bot_token
     ```
  - Create a `postgres.env` file.
     ```env
     POSTGRES_DB=db_name
     POSTGRES_USER=db_user
     POSTGRES_PASSWORD=secure_password
     POSTGRES_HOST=db_address
     POSTGRES_PORT=5432
     ```
  - Create `ton.env` file.
    ```env
    API_URL=base_link_for_ton_api
    API_KEY=api_key_for_ton_api
    ```

4. **Docker Setup**
   - Ensure Docker is installed and running.
   - Build and start the Docker containers:
     ```sh
     docker-compose up --build
     ```

#### Technologies Used
- **Python**: Main programming language.
- **Docker**: For containerization.
- **PostgreSQL**: Database management system.

#### License
This project is licensed under the GNU General Public License (GPL).
