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
import { mapActions, mapMutations } from 'vuex';

export default {
  name: 'App',
  components: {
    NavBar,
    DashboardComponent,
    ChartComponent,
  },
  methods: {
    ...mapActions(['fetchCustomers' , 'fetchDepositAccount', 'fetchCard', 'fetchTransaction']), // 액션 호출
    ...mapMutations(['setTotalBalance', 'setNumcustomer'])
  },
  mounted() {
    this.fetchCustomers().then(() => {
      console.log('customer data load')
      this.setNumcustomer(this.$store.state.customers.length)
    });

    this.fetchDepositAccount().then(() => {
      console.log('DepositAccount data load')
      let totalBalance = 0
      for (let i=0 ; i<this.$store.state.depositAccount.length ; i++){
       totalBalance += this.$store.state.depositAccount[i].Balance
      }
      this.setTotalBalance(totalBalance)
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