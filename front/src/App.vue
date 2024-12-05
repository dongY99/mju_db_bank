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
import { mapActions } from 'vuex';

export default {
  name: 'App',
  components: {
    NavBar,
    DashboardComponent,
    ChartComponent,
  },
  methods: {
    ...mapActions(['fetchCustomers' , 'fetchDepositAccount', 'fetchCard', 'fetchTransaction']), // 액션 호출
  },
  mounted() {
    this.fetchCustomers().then(() => {
      console.log('customer data load')
    });

    this.fetchDepositAccount().then(() => {
      console.log('DepositAccount data load')
    });

    this.fetchCard().then(() => {
      console.log('card data load')
    });

    this.fetchTransaction().then(() => {
      console.log('Transations data load')
    });
  },
};
</script>