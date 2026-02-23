# API Reference

## Base URL

```
http://localhost:8000/api/v1/
```

## Authentication

All protected endpoints require a valid session cookie or JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

## Endpoints

### Products

#### `GET /api/v1/products/`
Returns paginated list of products.

**Query params:**
- `page` — Page number (default: 1)
- `category` — Filter by category slug
- `search` — Search by name/description

**Response:**
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/v1/products/?page=2",
  "results": [
    {
      "id": 1,
      "name": "Product Name",
      "price": "99.99",
      "category": "electronics",
      "in_stock": true
    }
  ]
}
```

### Orders

#### `POST /api/v1/orders/`
Creates a new order.

**Body:**
```json
{
  "items": [
    {"product_id": 1, "quantity": 2}
  ],
  "shipping_address": "string"
}
```

## Error Responses

All errors return:
```json
{
  "error": "Error message",
  "detail": "More details"
}
```
