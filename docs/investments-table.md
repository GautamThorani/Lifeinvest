# Investments Table Documentation

## Purpose
The `investments` table is the core of the LifeInvest application. It tracks all types of investments: money, time, and energy.

## Table Structure

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique identifier |
| user_id | UUID | FOREIGN KEY → users.id | Owner of this investment |
| category_id | UUID | FOREIGN KEY → investment_categories.id | Classification category |
| type | VARCHAR(20) | CHECK: 'money','time','energy' | Type of investment |
| title | VARCHAR(200) | NOT NULL | Short description |
| description | TEXT | NULLABLE | Detailed notes |
| amount_invested | NUMERIC(10,2) | NOT NULL | Amount (money or hours) |
| currency | VARCHAR(10) | NULLABLE | 'USD', 'EUR', or 'hours' |
| invested_at | TIMESTAMPTZ | NOT NULL | When investment was made |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | Record creation time |

## Example Usage

### Time Investment (Learning)
INSERT INTO investments 
(user_id, category_id, type, title, amount_invested, currency, invested_at)
VALUES 
('user-uuid', 'category-uuid', 'time', 'Learn Docker', 8.0, 'hours', NOW());

### Money Investment (Course)
INSERT INTO investments 
(user_id, category_id, type, title, amount_invested, currency, invested_at)
VALUES 
('user-uuid', 'category-uuid', 'money', 'AWS Certification', 300.00, 'USD', NOW());

### Energy Investment (Networking)
INSERT INTO investments 
(user_id, category_id, type, title, amount_invested, currency, invested_at)
VALUES 
('user-uuid', 'category-uuid', 'energy', 'Tech Conference', 6.0, 'hours', NOW());

## Constraints & Validation
- **Foreign Keys**: Ensures user and category exist
- **Check Constraint**: Only valid types allowed
- **NOT NULL**: Critical fields must be provided
- **Index**: Optimizes queries by user and date
