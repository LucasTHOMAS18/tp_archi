<template>
  <div id="app">
    <header>
      <h1>Gestionnaire de Questionnaires</h1>
    </header>
    <router-view></router-view>
    <footer>
      <p>© Département Informatique - IUT d'Orléans</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
header {
  text-align: center;
  margin-bottom: 20px;
}
footer {
  text-align: center;
  margin-top: 40px;
  border-top: 1px solid #ccc;
  padding-top: 10px;
  color: #555;
}
</style>
