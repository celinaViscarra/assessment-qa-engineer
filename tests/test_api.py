def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_create_product_with_negative_values(client, admin_token):
    """
    BUG: La API permite crear productos con price y stock negativos
    """
    payload = {
        "name": "Producto inválido",
        "price": -10,
        "stock": -5
    }

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    response = client.post(
        "/products",
        json=payload,
        headers=headers
    )

    # Comportamiento esperado (correcto)
    assert response.status_code == 422


def test_update_non_existing_product_returns_404(client, admin_token):
    """
    BUG: La API permite actualizar productos inexistentes
    """
    payload = {
        "name": "Producto fantasma",
        "price": 50,
        "stock": 10
    }

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    response = client.put(
        "/products/9999",
        json=payload,
        headers=headers
    )

    assert response.status_code == 404

