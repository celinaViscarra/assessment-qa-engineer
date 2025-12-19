def test_update_non_existing_product_returns_404(client, admin_token):
    payload = {
        "name": "Producto actualizado",
        "price": 100,
        "stock": 10
    }

    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    response = client.put(
        "/products/99999",  # ID que no existe
        json=payload,
        headers=headers
    )

    assert response.status_code == 404

