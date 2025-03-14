<template>
  <div class="product-card" @click="goToProduct">
    <img :src="imageUrl" :alt="product.name" class="product-image" />

    <h2 class="product-name">{{ product.name }}</h2>

    <p class="product-description">{{ product.description }}</p>

    <p class="product-price">Цена: {{ product.price }} ₽</p>
  </div>
</template>
  
  <script>
import apiClient from "@/utils/api";
export default {
  props: {
    product: {
      type: Object,
      required: true,
    },
  },
  computed: {
    imageUrl() {
      const imageUrl = `${apiClient.defaults.baseURL}/products/image/${
        this.product.id
      }?timestamp=${Date.now()}`;
      return imageUrl;
    },
  },
  methods: {
    goToProduct() {
      this.$router.push({
        name: "product",
        params: { id: this.product.id },
      });
    },
  },
};
</script>
  
  <style scoped>
.product-card {
  width: 100%;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  text-align: center;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease,
    background-color 0.3s ease;
}

.product-card:hover {
  transform: translate(-5px, -5px) scale(1.05);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
  background-color: #f9f9f9;
}

.product-image {
  width: 60%;
  height: auto;
  border-radius: 10px;
  margin-bottom: 15px;
  transition: transform 1s ease;
}

.product-card:hover .product-image {
  transform: scale(1.02);
}

.product-name {
  font-size: 1.5em;
  margin-bottom: 10px;
  color: #333;
  transition: color 0.3s ease;
}

.product-card:hover .product-name {
  color: #3d8f4d;
}

.product-description {
  font-size: 1em;
  color: #666;
  margin-bottom: 15px;
  transition: color 0.3s ease;
}

.product-card:hover .product-description {
  color: #555;
}

.product-price {
  font-size: 1.2em;
  font-weight: bold;
  color: #000;
  transition: color 0.3s ease;
}
</style>