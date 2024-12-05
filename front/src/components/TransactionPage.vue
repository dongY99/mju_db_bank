<template>
  <div class="row">
    <ul class="nav nav-tabs">
      <li class="nav-item col">
        <a class="nav-link" aria-current="page">거래 번호</a>
      </li>
      <li class="nav-item col">
        <a class="nav-link" aria-current="page">계좌번호 ID</a>
      </li>
      <li class="nav-item dropdown col">
        <a class="nav-link dropdown-toggle" data-bs-toggle="dropdown" role="button" aria-expanded="false">입출금일</a>
        <ul class="dropdown-menu">
          <li><a class="dropdown-item">오름차순</a></li>
          <li><a class="dropdown-item">내림차순</a></li>
        </ul>
      </li>
      <li class="nav-item col">
        <a class="nav-link" aria-current="page">거래 금액</a>
      </li>
      <li class="nav-item col">
        <a class="nav-link" aria-current="page">잔고</a>
      </li>
      <li class="nav-item col">
        <a class="nav-link" aria-current="page">거래 세부사항</a>
      </li>
    </ul>
  </div>
  <ul v-for="(transaction, index) in transactions" :key="index" class="list-group list-group-horizontal row">
    <li class="list-group-item col"> {{ transaction.Transaction_Number }}</li>
    <li class="list-group-item col"> {{ transaction.Deposit_Account_ID }}</li>
    <li class="list-group-item col"> {{ transaction.Data_Of_Deposit_Withdrawal }}</li>
    <li class="list-group-item col"> {{ transaction.Transaction_Amount }}</li>
    <li class="list-group-item col"> {{ transaction.Balance }}</li>
    <li class="list-group-item col"> {{ transaction.Details_Of_Transaction }}</li>
  </ul>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: 'TransactionPage',
  data() {
    return {

    }
  },

  computed: {
    ...mapState(["transactions"]),
  },
}
</script>