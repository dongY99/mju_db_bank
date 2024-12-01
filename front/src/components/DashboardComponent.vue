<template>
  <div class="dash-board">
    <h1>Dashboard</h1>
    <div style="display: flex;">
      <div class="card-blue">
        <p>회원 수</p>
        <h1>400,000</h1>
        <div class="card-icon"><i class="fa-solid fa-user"></i></div>
      </div>
      <div class="card-green">
        <p>자금</p>
        <h1>800,000</h1>
        <div class="card-icon"><i class="fa-solid fa-won-sign"></i></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardComponent'
};
</script>