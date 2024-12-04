<template>
  <div class="chart mt-5">
    <nav class="navbar navbar-expand-lg bg-body-tertiary content-head">
      <div class="container-fluid">
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav">
            <form class="d-flex" role="search">
              <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" />
              <button class="btn btn-outline-success" type="submit">
                Search
              </button>
            </form>
            <div class="mx-3">
              <select v-model="searchType" class="form-select">
                <option :value=0>고객</option>
                <option :value=1>예금계좌</option>
                <option :value=2>거래내역</option>
                <option :value=3>카드</option>
              </select>
            </div>
            <CustomerForm />
          </ul>
        </div>
      </div>
    </nav>
    <div style="margin-left: 10px; overflow-y: scroll; min-height: 100%;">
      <div v-if="searchType == 0">
        <CustomersPage />
      </div>
      <div v-if="searchType == 1">
        <DepositAccountPage />
      </div>
      <div v-if="searchType == 2">
        <TransactionPage />
      </div>
      <div v-if="searchType == 3">
        <CardPage />
      </div>
    </div>
  </div>
</template>

<script>
import CustomerForm from './CustomerForm.vue';
import CustomersPage from './CustomersPage.vue';
import DepositAccountPage from './DepositAccountPage.vue';
import TransactionPage from './TransactionPage.vue';
import CardPage from './CardPage.vue';

export default {
  name: 'ChartComponent',
  data() {
    return {
      searchType: 0
    };
  },

  components: {
    CustomerForm,
    CustomersPage,
    DepositAccountPage,
    TransactionPage,
    CardPage,
  }
};
</script>