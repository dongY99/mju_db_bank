<template>
  <div class="row">
    <ul class="nav nav-tabs">
      <li class="nav-item col">
        <a class="nav-link" aria-current="page">예금계좌 ID</a>
      </li>
      <li class="nav-item dropdown col">
        <a class="nav-link dropdown-toggle" data-bs-toggle="dropdown" role="button" aria-expanded="false">계좌 종류</a>
        <ul class="dropdown-menu">
          <li><a class="dropdown-item" @click="sortDepositAccountFront('Account_Type', 'asc')">오름차순</a></li>
          <li><a class="dropdown-item" @click="sortDepositAccountFront('Account_Type', 'desc')">내림차순</a></li>
        </ul>
      </li>
      <li class="nav-item dropdown col">
        <a class="nav-link dropdown-toggle" data-bs-toggle="dropdown" role="button" aria-expanded="false">잔고</a>
        <ul class="dropdown-menu">
          <li><a class="dropdown-item" @click="sortDepositAccountFront('Balance', 'asc')">오름차순</a></li>
          <li><a class="dropdown-item" @click="sortDepositAccountFront('Balance', 'desc')">내림차순</a></li>
        </ul>
      </li>
      <li class="nav-item col">
        <a class="nav-link" aria-current="page">카드 신청 상태</a>
      </li>
      <li class="nav-item dropdown col">
        <a class="nav-link dropdown-toggle" data-bs-toggle="dropdown" role="button" aria-expanded="false">계좌 개설일</a>
        <ul class="dropdown-menu">
          <li><a class="dropdown-item" @click="sortDepositAccountFront('Data_Of_Opening', 'asc')">오름차순</a></li>
          <li><a class="dropdown-item" @click="sortDepositAccountFront('Data_Of_Opening', 'desc')">내림차순</a></li>
        </ul>
      </li>
      <li class="nav-item col">
        <a class="nav-link" aria-current="page">고객 주민번호</a>
      </li>
      <li class="col"></li>
      <li class="col"></li>
    </ul>
  </div>
  <ul v-for="(deposit, index) in depositAccount" :key="index" class="list-group list-group-horizontal row">
    <li class="list-group-item col"> {{ deposit.Deposit_Account_ID }}</li>
    <li class="list-group-item col"> {{ deposit.Account_Type }}</li>
    <li class="list-group-item col"> {{ deposit.Balance }}</li>
    <li class="list-group-item col"> {{ deposit.Card_Application_Status }}</li>
    <li class="list-group-item col"> {{ deposit.Data_Of_Opening }}</li>
    <li class="list-group-item col"> {{ deposit.Customer_Resident_Registration_Number }}</li>
    <CardForm :deposit="deposit" :index="index" class="col"/>
    <DepositAccountForm :isUpdate="true" :deposit="deposit" class="col"/>
  </ul>
</template>

<script>
import CardForm from "./CardForm.vue";
import DepositAccountForm from "./DepositAccountForm.vue";
import { mapState, mapActions } from "vuex";

export default {
  name: 'DepositAccountPage',
  data() {
    return {

    }
  },

  components: {
    CardForm,
    DepositAccountForm,
  },

  computed: {
    ...mapState(["depositAccount"]),
  },

  methods: {
    ...mapActions(["sortDepositAccount"]),

    async sortDepositAccountFront(field, order) {
      const data = {field, order}
      await this.sortDepositAccount(data)
    }
  }
}
</script>