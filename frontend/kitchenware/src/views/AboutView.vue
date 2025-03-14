<template>
  <div class="about-page">
    <div class="hero-section">
      <h1>О нас</h1>
      <p>
        Добро пожаловать в Kitchenware Store — ваш надежный партнер в мире
        кухонной утвари!
      </p>
    </div>

    <div class="content-section">
      <div class="mission">
        <h2>Наша миссия</h2>
        <p>
          Мы стремимся сделать приготовление пищи более удобным, приятным и
          вдохновляющим. Наша цель — предоставить вам качественные товары,
          которые помогут вам создавать кулинарные шедевры с легкостью и
          удовольствием.
        </p>
      </div>

      <div class="history">
        <h2>Наша история</h2>
        <p>
          Kitchenware Store был основан в 2010 году группой энтузиастов, которые
          хотели изменить подход к выбору кухонной утвари. Начиная с небольшого
          магазина, мы выросли в крупный онлайн-ритейлер, предлагающий тысячи
          товаров для кухни от лучших брендов со всего мира.
        </p>
      </div>

      <div class="values">
        <h2>Наши ценности</h2>
        <ul>
          <li>
            Качество — мы предлагаем только проверенные и долговечные товары.
          </li>
          <li>Доступность — наши цены доступны для каждого.</li>
          <li>
            Клиентоориентированность — мы всегда готовы помочь вам с выбором.
          </li>
          <li>
            Инновации — мы следим за трендами и предлагаем современные решения.
          </li>
        </ul>
      </div>

      <div class="team">
        <h2>Наша команда</h2>
        <p>
          Наша команда — это профессионалы, которые любят свою работу и всегда
          готовы поделиться своими знаниями. Мы гордимся тем, что помогаем нашим
          клиентам находить именно то, что им нужно.
        </p>
      </div>

      <div class="why-choose-us">
        <h2>Почему выбирают нас?</h2>
        <ul>
          <li>Широкий ассортимент товаров.</li>
          <li>Быстрая и надежная доставка.</li>
          <li>Гарантия качества на все товары.</li>
          <li>Профессиональная поддержка 24/7.</li>
        </ul>
      </div>
    </div>
  </div>
</template>
  
  <script>
export default {
  name: "AboutPage",
};
</script>
  
  <style scoped>
.about-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: "Arial", sans-serif;
  color: #333;
}

.hero-section {
  text-align: center;
  padding: 60px 20px;
  background: linear-gradient(135deg, #3bb339, #7fdf5f);
  color: white;
  border-radius: 12px;
  margin-bottom: 40px;
}

.hero-section h1 {
  font-size: 3em;
  margin-bottom: 20px;
}

.hero-section p {
  font-size: 1.2em;
  margin: 0;
}

.content-section {
  display: grid;
  gap: 30px;
}

.mission,
.history,
.values,
.team,
.why-choose-us {
  background: #ffffff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

h2 {
  font-size: 2em;
  margin-bottom: 15px;
  color: #2c3e50;
}

p {
  font-size: 1.1em;
  line-height: 1.6;
  color: #555;
}

ul {
  list-style-type: disc;
  padding-left: 20px;
}

li {
  font-size: 1.1em;
  margin-bottom: 10px;
  color: #555;
}
</style>