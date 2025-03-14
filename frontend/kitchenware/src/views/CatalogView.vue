<template>
  <div>
    <div class="container">
      <div class="sidebar">
        <h2>Фильтры и сортировка</h2>

        <div class="filter-section">
          <h3>Сортировать по цене</h3>
          <select v-model="sortByPrice" class="filter-select">
            <option value="asc">По возрастанию</option>
            <option value="desc">По убыванию</option>
          </select>
        </div>

        <div class="filter-section">
          <h3>Бренды</h3>
          <div v-if="brands.length" class="checkbox-group">
            <div v-for="brand in brands" :key="brand.id" class="checkbox-item">
              <label>
                <input
                  type="checkbox"
                  :value="brand.id"
                  v-model="selectedBrands"
                  class="filter-checkbox"
                />
                <span class="checkmark"></span>
                {{ brand.name }}
              </label>
            </div>
          </div>
          <div v-else>
            <p>Нет доступных брендов.</p>
          </div>
        </div>

        <div class="filter-section">
          <h3>Категории</h3>
          <div v-if="categories.length" class="checkbox-group">
            <div
              v-for="category in categories"
              :key="category.id"
              class="checkbox-item"
            >
              <label>
                <input
                  type="checkbox"
                  :value="category.id"
                  v-model="selectedCategories"
                  class="filter-checkbox"
                />
                <span class="checkmark"></span>
                {{ category.name }}
              </label>
            </div>
          </div>
          <div v-else>
            <p>Нет доступных категорий.</p>
          </div>
        </div>

        <button @click="applyFilters" class="apply-button">Применить</button>
      </div>

      <div v-if="filteredProducts.length" class="product-grid">
        <Product
          v-for="product in filteredProducts"
          :key="product.id"
          :product="product"
        />
      </div>
      <div v-else>
        <p>Нет товаров, соответствующих выбранным фильтрам.</p>
      </div>
    </div>
  </div>
</template>

<script>
import Product from "../components/Product.vue";
import apiClient from "../utils/api";

export default {
  components: { Product },
  data() {
    return {
      products: [],
      brands: [],
      categories: [],
      selectedBrands: [],
      selectedCategories: [],
      sortByPrice: "none",
      filteredProducts: [],
    };
  },
  methods: {
    async fetchProducts() {
      try {
        const response = await apiClient.get("/products/");
        this.products = response.data.Products;
        this.filteredProducts = response.data.Products;
      } catch (error) {
        console.error(error);
      }
    },

    async getBrands() {
      try {
        const response = await apiClient.get("/brands");
        this.brands = response.data.brands || response.data;
      } catch (error) {
        console.error(error);
      }
    },

    async getCategories() {
      try {
        const response = await apiClient.get("/categories");
        this.categories = response.data.categories || response.data;
      } catch (error) {
        console.error(error);
      }
    },

    applyFilters() {
      let filtered = this.products;

      if (this.selectedBrands.length > 0) {
        filtered = filtered.filter((product) =>
          this.selectedBrands.includes(product.brand_id)
        );
      }

      if (this.selectedCategories.length > 0) {
        filtered = filtered.filter((product) =>
          this.selectedCategories.includes(product.category_id)
        );
      }

      if (this.sortByPrice === "asc") {
        filtered.sort((a, b) => a.price - b.price);
      } else if (this.sortByPrice === "desc") {
        filtered.sort((a, b) => b.price - a.price);
      }

      this.filteredProducts = filtered;
    },
  },
  mounted() {
    this.fetchProducts();
    this.getBrands();
    this.getCategories();
  },
};
</script>

<style scoped>
h1 {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
  font-size: 2rem;
  font-weight: 600;
}

.container {
  display: flex;
  gap: 30px;
  padding: 0 20px;
  max-width: 1200px;
  margin: 0 auto;
  margin-top: 50px;
}

.sidebar {
  width: 300px;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.sidebar:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.filter-section {
  margin-bottom: 25px;
}

.filter-section h3 {
  margin-bottom: 15px;
  font-size: 1.1rem;
  color: #444;
  font-weight: 500;
}

.filter-select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  color: #555;
  background-color: #f9f9f9;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.filter-select:focus {
  border-color: #53bd45;
  outline: none;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.2);
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.checkbox-item {
  display: flex;
  align-items: center;
  position: relative;
  cursor: pointer;
  padding: 10px;
}

.filter-checkbox {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 100%;
  width: 100%;
}

.checkmark {
  width: 24px;
  height: 24px;
  border: 2px solid #ccc;
  border-radius: 4px;
  margin-right: 10px;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.checkbox-item:hover .checkmark {
  border-color: #53bd45;
}

.checkbox-item:hover {
  background-color: rgba(83, 189, 69, 0.1);
}

.checkbox-item:hover label {
  color: #53bd45;
  font-weight: bold;
}

.checkbox-item label {
  font-size: 1.1rem;
  transition: color 0.3s ease;
}

.filter-checkbox:checked + .checkmark {
  background-color: #53bd45;
  border-color: #53bd45;
}

.filter-checkbox:checked + .checkmark::after {
  opacity: 1;
}

.apply-button {
  width: 100%;
  padding: 12px;
  background-color: #53bd45;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.apply-button:hover {
  background-color: #3fd231;
  transform: translateY(-2px);
}

.apply-button:active {
  transform: translateY(0);
}

.product-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

@media (max-width: 1224px) {
  .product-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 868px) {
  .product-grid {
    grid-template-columns: 1fr;
  }
}
</style>