<template>
  <nav class="admin-nav">
    <ul class="admin-nav__list">
      <li class="admin-nav__item">
        <router-link to="/admin/products" class="admin-nav__link">
          <span class="admin-nav__icon">🛒</span>
          <span class="admin-nav__text">Товары</span>
        </router-link>
      </li>
      <li class="admin-nav__item">
        <router-link to="/admin/categories" class="admin-nav__link">
          <span class="admin-nav__icon">📂</span>
          <span class="admin-nav__text">Категории</span>
        </router-link>
      </li>
      <li class="admin-nav__item">
        <router-link to="/admin/brands" class="admin-nav__link">
          <span class="admin-nav__icon">🏷️</span>
          <span class="admin-nav__text">Бренды</span>
        </router-link>
      </li>
      <li class="admin-nav__item">
        <router-link to="/admin/images" class="admin-nav__link">
          <span class="admin-nav__icon">🖼️</span>
          <span class="admin-nav__text">Изображения</span>
        </router-link>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: "AdminNav",
};
</script>

<style lang="scss" scoped>
.admin-nav {
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1rem;
  border-radius: 8px;

  &__list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  &__item {
    margin: 0;
  }

  &__link {
    display: flex;
    align-items: center;
    padding: 0.75rem 1rem;
    text-decoration: none;
    color: #333;
    border-radius: 4px;
    transition: background-color 0.3s ease, color 0.3s ease;

    &:hover {
      background-color: #f0f0f0;
      color: #4caf50;
    }

    &.router-link-exact-active {
      background-color: #4caf50;
      color: #ffffff;
    }
  }

  &__icon {
    margin-right: 0.75rem;
    font-size: 1.25rem;
  }

  &__text {
    font-size: 1rem;
    font-weight: 500;
  }
}
</style>