CREATE TYPE blockchain AS ENUM ('SOL', 'ETH', 'BSC', 'BASE', 'TON');
CREATE TYPE wallet_type AS ENUM ('INTERNAL', 'EXTERNAL');
CREATE TYPE general_status AS ENUM ('ACTIVE', 'INACTIVE', 'DELETED');

CREATE TABLE IF NOT EXISTS wallets (
    id SERIAL PRIMARY KEY,
    address VARCHAR(100) NOT NULL,
    secret TEXT NOT NULL,
    network blockchain NOT NULL,
    type wallet_type DEFAULT 'INTERNAL',
    status general_status DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (address, network)
);

CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    username VARCHAR(255),
    wallet_id BIGINT,
    phone_number VARCHAR(15),
    email VARCHAR(255),
    birthday DATE,
    ip_address VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    edited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (wallet_id) REFERENCES wallets(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS protected_gropes (
    id SERIAL PRIMARY KEY,
    grope_id BIGINT NOT NULL,
    network blockchain NOT NULL,
    collection_address VARCHAR(100) NOT NULL,
    status general_status DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    edited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS airdrop_commands (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    grope_id BIGINT NOT NULL,
    command_extension VARCHAR(255) NOT NULL,
    network blockchain NOT NULL,
    collection_address VARCHAR(100) NOT NULL,
    description TEXT,
    message TEXT,
    status general_status DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    edited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (command_extension)
);

CREATE TABLE IF NOT EXISTS airdrop_user_activities (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    airdrop_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (airdrop_id) REFERENCES airdrop_commands(id) ON DELETE CASCADE
);