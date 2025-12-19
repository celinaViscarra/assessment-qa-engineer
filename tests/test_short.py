# tests/test_api.py

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# ---------- AUTH ----------

def test_login_with_valid_admin_credentials(client):
    response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_with_invalid_credentials(client):
    response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "wrongpass"}
    )
    assert response.status_code == 401


# ---------- PRODUCTS ----------

def test_get_products_requires_auth(client):
    response = client.get("/products")
    assert response.status_code == 401


def test_get_products_as_admin(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/products", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_product_success(client, admin_token):
    payload = {
        "name": "Producto QA",
	"description":"Producto de prueba QA",
        "price": 25,
        "stock": 10
    }
    headers = {"Authorization": f"Bearer {admin_token}"}

    response = client.post("/products", json=payload, headers=headers)

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == payload["name"]
    assert body["price"] == payload["price"]
    assert body["stock"] == payload["stock"]
    assert "id" in product


def test_create_product_with_negative_values_returns_422(client, admin_token):
    payload = {
        "name": "Producto inválido",
        "price": -10,
        "stock": -5
    }
    headers = {"Authorization": f"Bearer {admin_token}"}

    response = client.post("/products", json=payload, headers=headers)

    assert response.status_code == 422


def test_get_product_by_id_not_found(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/products/99999", headers=headers)
    assert response.status_code == 404


def test_update_non_existing_product_returns_404(client, admin_token):
    payload = {
        "name": "Fantasma",
        "price": 50,
        "stock": 5
    }
    headers = {"Authorization": f"Bearer {admin_token}"}

    response = client.put("/products/99999", json=payload, headers=headers)

    assert response.status_code == 404


def test_delete_non_existing_product_returns_404(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.delete("/products/99999", headers=headers)
    assert response.status_code == 204


# ---------- INVENTORY ----------

def test_adjust_inventory_success(client, admin_token):
    # Crear producto primero
    product_payload = {
        "name": "Producto inventario",
        "description": "Producto para inventario",
        "price": 10,
        "stock": 5
    }

    headers = {"Authorization": f"Bearer {admin_token}"}

    create_response = client.post(
        "/products",
        json=product_payload,
        headers=headers
    )

    assert create_response.status_code == 422
    product = create_response.json()
    assert "id" in product

    adjust_payload = {
        "product_id": product["id"],
        "quantity": 5
    }

    response = client.post(
        "/inventory/adjust",
        json=adjust_payload,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["stock"] == 10


def test_adjust_inventory_invalid_product_returns_404(client, admin_token):
    payload = {
        "product_id": 99999,
        "quantity": 5
    }
    headers = {"Authorization": f"Bearer {admin_token}"}

    response = client.post("/inventory/adjust", json=payload, headers=headers)

    assert response.status_code == 422


def test_low_stock_products(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get("/inventory/low-stock", headers=headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)

