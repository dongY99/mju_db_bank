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
            <button type="button" class="btn btn-success mx-3" @click="addTransaction">거래 내역 추가</button>
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
import { mapActions } from 'vuex';
import axios from 'axios';

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
    ...mapActions(["postTransactions", "fetchDepositAccount", "fetchTransaction"]), // Vuex 액션 맵핑

    async addTransaction() {
      try {
        const depositAccounts = (await axios.get('/api/deposit_account')).data;
        if (depositAccounts.length === 0) {
          alert("예금 계좌가 존재하지 않습니다.");
          return;
        }
        const randomAccount = depositAccounts[Math.floor(Math.random() * depositAccounts.length)];
        
        const randomAccountID = randomAccount.Deposit_Account_ID;

        // 무작위 거래 내역 생성
        const transactionAmount = Math.floor(Math.random() * 1000) - 499; // -499~500 사이의 무작위 거래 금액
        const newBalance = randomAccount.Balance + transactionAmount;

        if (newBalance < 0) {
          alert("거래 금액이 잔액을 초과합니다. 거래 실패.");
          return;
        }

        let transaction = {
          Transaction_Number: Math.floor(Math.random() * 9000) + 1000, // 임의의 거래 번호
          Deposit_Account_ID: randomAccountID, // 선택된 계좌의 ID
          Data_Of_Deposit_Withdrawal: "", // 현재 날짜와 시간
          Transaction_Amount: transactionAmount, // 무작위 거래 금액
          Balance: newBalance, // 계산된 새로운 잔액
          Details_Of_Transaction: "자동 생성 거래", // 예제 거래 내용
        };

        await this.postTransactions(transaction);
        await this.fetchDepositAccount();

        alert("거래 내역이 성공적으로 추가되었습니다.");
      } catch (error) {
        console.error("Error adding transaction:", error);
      }
    }
  }
};
</script>