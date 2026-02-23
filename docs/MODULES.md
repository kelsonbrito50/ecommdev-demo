# Platform Modules

ECOMMDEV is a 13-module enterprise e-commerce platform. Here's a breakdown:

## Core Modules

| Module | Description |
|--------|-------------|
| **Products** | Catalog, categories, variants, images |
| **Orders** | Order lifecycle, status tracking |
| **Cart** | Redis-backed session cart |
| **Users** | Custom user model, address book |
| **Payments** | MercadoPago integration |

## Operations Modules

| Module | Description |
|--------|-------------|
| **Shipping** | Correios + custom carrier integration |
| **Inventory** | Stock management, alerts |
| **Promotions** | Coupons, discounts, flash sales |

## Admin Modules

| Module | Description |
|--------|-------------|
| **Dashboard** | Sales metrics, KPI overview |
| **Reports** | Revenue, conversion, inventory reports |
| **CRM** | Customer relationship management |

## Infrastructure Modules

| Module | Description |
|--------|-------------|
| **Notifications** | Email, SMS via Celery async tasks |
| **Audit Log** | Action tracking for compliance |

## Module Dependencies

```
Users → Cart → Orders → Payments
         ↓
      Products → Inventory
         ↓
      Shipping
```

Each module is a Django app following standard conventions.
