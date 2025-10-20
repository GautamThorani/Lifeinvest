# Database Design - LifeInvest

## Core Tables

### 1. investments (Main table)
- id (UUID, Primary Key)
- type: 'money' | 'time' | 'energy'
- category: 'learning' | 'job_hunt' | 'health' | 'networking'
- title: string
- description: text  
- amount_invested: decimal (money or hours)
- currency: string ('USD', 'EUR', or 'hours' for time)
- invested_at: timestamp
- created_at: timestamp

### 2. investment_returns (Planned - for ROI tracking)
- id (UUID)
- investment_id (UUID, Foreign Key)
- type: 'money' | 'opportunity' | 'skill' | 'connection'
- amount_returned: decimal
- description: text
- return_date: timestamp
- roi_percentage: decimal

### 3. tags (Planned - for categorization)
- id (UUID)
- name: string

### 4. investment_tags (Planned - Many-to-Many relationship)
- investment_id (UUID)
- tag_id (UUID)

## Design Decisions

1. **UUID Primary Keys**: Better for distributed systems, hide sequential business data
2. **Flexible Amounts**: amount_invested can represent money or time (hours)
3. **Currency Field**: Can store actual currency or 'hours' for time investments
4. **UTC Timestamps**: All times stored in UTC, convert in application layer
5. **Extensible Design**: Easy to add returns and tags tables later

## Example Data
- Time Investment: 8 hours learning Docker, category: 'learning'
- Money Investment: $500 for online course, category: 'learning'  
- Energy Investment: 3 hours networking event, category: 'networking'
