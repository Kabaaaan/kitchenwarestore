<template>
  <div class="order-card">
    <h3>Заказ #{{ order.id }}</h3>
    <p>Общая цена: {{ order.total_price }} ₽</p>
  </div>
</template>
  
  <script>
export default {
  name: "OrderCard",
  props: {
    order: {
      type: Object,
      required: true,
    },
  },
};
</script>
  
  <style scoped>
.order-card {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 16px;
  margin: 8px;
  width: 90%;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.order-card h3 {
  margin: 0 0 8px;
  font-size: 18px;
}

.order-card p {
  margin: 0;
  font-size: 16px;
  color: #555;
}
</style>