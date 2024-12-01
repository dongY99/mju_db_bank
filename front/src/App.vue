<template>
  <div>
    <NavBar />
    <div class="content">
      <DashboardComponent />
      <ChartComponent />
    </div>
    <ModalDialog />
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue';
import DashboardComponent from './components/DashboardComponent.vue';
import ChartComponent from './components/ChartComponent.vue';

export default {
  name: 'App',
  components: {
    NavBar,
    DashboardComponent,
    ChartComponent,
  }
};
</script>

<style>
.title {}
</style>