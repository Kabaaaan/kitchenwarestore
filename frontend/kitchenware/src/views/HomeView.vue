<template>
  <div class="container">
    <div class="content">
      <h1 class="title">Kitchenware Store</h1>
      <p class="description">
        Ваш идеальный магазин для покупки посуды и кухонных принадлежностей.
      </p>

      <div class="section" style="width: 70%; margin: auto">
        <div class="cards">
          <div v-for="brand in brands.brands" :key="brand.id" class="card">
            <div class="card-content">
              <h3 class="card-title">{{ brand.name }}</h3>
            </div>
          </div>
        </div>
      </div>

      <div class="section">
        <div class="cards">
          <div
            v-for="category in categories.categories"
            :key="category.id"
            class="card"
          >
            <div class="card-content">
              <h3 class="card-title">{{ category.name }}</h3>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
  
  <script>
import apiClient from "../utils/api";

export default {
  data() {
    return {
      brands: { brands: [] },
      categories: { categories: [] },
    };
  },
  methods: {
    async getBrands() {
      try {
        const response = await apiClient.get("/brands");
        this.brands = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    async getCategories() {
      try {
        const response = await apiClient.get("/categories");
        this.categories = response.data;
      } catch (error) {
        console.error(error);
      }
    },
  },
  mounted() {
    this.getBrands();
    this.getCategories();
  },
};
</script>
  
  <style scoped>
.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 20px;
}

.content {
  text-align: center;
  max-width: 1200px;
  width: 100%;
}

.title {
  font-size: 4rem;
  color: #343a40;
  margin-bottom: 20px;
  margin-top: 100px;
  font-family: "Arial", sans-serif;
  transition: transform 1s;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}
.title:hover {
  transform: scale(1.1);
}

.description {
  font-size: 1.5rem;
  color: #6c757d;
  margin-bottom: 100px;
}

.section {
  margin-bottom: 40px;
  padding-bottom: 20px;
}

.section-title {
  font-size: 2rem;
  color: #343a40;
  margin-bottom: 20px;
}

.cards {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  border-bottom: 1px solid black;
  margin-bottom: 100px;
}

.card {
  background-color: white;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 150px;
  padding: 20px;
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  margin-bottom: 10px;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 4px rgba(0, 0, 0, 0.5);
}

.card-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.card-title {
  font-size: 1.25rem;
  color: #343a40;
  margin: 0;
  width: 100%;
  height: 100%;
}
</style>