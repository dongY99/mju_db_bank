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
            <button type="button" class="btn btn-success mx-3">거래 내역 추가</button>
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
  },

  methods: {
    async addTransaction() {
      try {
        let transaction = {
          'Transaction_Number': Math.floor(Math.random() * 9000) + 1000,
          'Deposit_Account_ID': //예금계좌 테이블 중 아무 튜플의 ID
          'Data_Of_Deposit_Withdrawal': //현재 날짜와 시간
          'Transaction_Amount': Math.floor(Math.random()),
          'Balance': //해당 계좌의 금액 - 지불금액 만약 0 이하가 된다면 실패 alter
          'Details_Of_Transaction': //아무글자나 null
        };

        await this.postTransactions(this.transaction);

        alert("거래 내역이 성공적으로 추가되었습니다.");
      } catch(error) {
        console.error("Error adding transaction:", error);
      }
    } 
  }
};
</script>