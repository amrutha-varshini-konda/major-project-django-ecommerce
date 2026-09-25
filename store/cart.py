{% extends 'base.html' %}

{% block content %}
<div class="container my-4">
  <h2 class="mb-4">Shopping Cart</h2>

  {% if cart_items %}
    <div class="table-responsive">
      <table class="table table-striped align-middle">
        <thead>
          <tr>
            <th>Product</th>
            <th>Price</th>
            <th>Quantity</th>
            <th>Total</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {% for item in cart_items %}
            <tr>
              <td>
                <strong>{{ item.product.name }}</strong>
              </td>
              <td>${{ item.product.price }}</td>
              <td>{{ item.quantity }}</td>
              <td>${{ item.total_price }}</td>
              <td>
                <a href="{% url 'store:cart_remove' item.product.id %}" class="btn btn-danger btn-sm">Remove</a>
              </td>
            </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>

    <div class="d-flex justify-content-between align-items-center mt-4">
      <h4>Total: <strong>${{ total_price }}</strong></h4>
      <div>
        <a href="{% url 'store:product_list' %}" class="btn btn-outline-secondary me-2">Continue Shopping</a>
        <a href="#" class="btn btn-success">Proceed to Checkout</a>
      </div>
    </div>
  {% else %}
    <div class="alert alert-info text-center py-4">
      <h4>Your cart is empty!</h4>
      <p class="mb-3">Explore our items and add something to your cart.</p>
      <a href="{% url 'store:product_list' %}" class="btn btn-primary">Start Shopping</a>
    </div>
  {% endif %}
</div>
{% endblock %}