<script setup>
import { RouterLink, RouterView } from "vue-router";
</script>

<template>
  <header>
    <nav>
      <RouterLink class="link" to="/">Домашняя</RouterLink>
      <RouterLink class="link" to="/catalog">Каталог</RouterLink>
      <RouterLink class="link" to="/about">О нас</RouterLink>
      <RouterLink class="link" to="/profile">Профиль</RouterLink>
    </nav>
  </header>

  <RouterView v-slot="{ Component }">
    <transition name="fade" mode="out-in">
      <component :is="Component" />
    </transition>
  </RouterView>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.flip-enter-active,
.flip-leave-active {
  transition: transform 0.7s ease;
  transform-style: preserve-3d;
}

.flip-enter-from {
  transform: rotateY(100deg);
  opacity: 0;
}

.flip-leave-to {
  transform: rotateY(-100deg);
  opacity: 0;
}

header {
  padding: 20px 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

nav {
  display: flex;
  align-items: center;
  justify-content: center;
}

.link {
  margin: 0 30px;
  text-decoration: none;
  color: #333;
  font-size: 2em;
  font-weight: bold;
  padding: 15px 25px;
  border-radius: 8px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.link:hover {
  background-color: #42b983;
  color: white;
}

.router-link-active {
  font-weight: bold;
  color: #42b983;
}

.router-link-exact-active {
  color: #42b983;
}
</style>
