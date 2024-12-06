<template>
  <div class="row">
    <ul class="nav nav-tabs">
      <li class="nav-item col">
        <a class="nav-link" aria-current="page">카드 ID</a>
      </li>
      <li class="nav-item dropdown col">
        <a class="nav-link dropdown-toggle" data-bs-toggle="dropdown" role="button" aria-expanded="false">신청일</a>
        <ul class="dropdown-menu">
          <li><a class="dropdown-item" @click="sortCardFront('Date_Of_Application', 'asc')">오름차순</a></li>
          <li><a class="dropdown-item" @click="sortCardFront('Date_Of_Application', 'desc')">내림차순</a></li>
        </ul>
      </li>
      <li class="nav-item dropdown col">
        <a class="nav-link dropdown-toggle" data-bs-toggle="dropdown" role="button" aria-expanded="false">한도 금액</a>
        <ul class="dropdown-menu">
          <li><a class="dropdown-item" @click="sortCardFront('Limit_Amount', 'asc')">오름차순</a></li>
          <li><a class="dropdown-item" @click="sortCardFront('Limit_Amount', 'desc')">내림차순</a></li>
        </ul>
      </li>
      <li class="nav-item col">
        <a class="nav-link" aria-current="page">결제 날짜</a>
      </li>
      <li class="nav-item dropdown col">
        <a class="nav-link dropdown-toggle" data-bs-toggle="dropdown" role="button" aria-expanded="false">카드 종류</a>
        <ul class="dropdown-menu">
          <li><a class="dropdown-item" @click="sortCardFront('Card_Type', 'asc')">오름차순</a></li>
          <li><a class="dropdown-item" @click="sortCardFront('Card_Type', 'desc')">내림차순</a></li>
        </ul>
      </li>
      <li class="nav-item col">
        <a class="nav-link" aria-current="page">고객 주민 번호</a>
      </li>
      <li class="nav-item col">
        <a class="nav-link" aria-current="page">예금계좌 ID</a>
      </li>
    </ul>
  </div>
  <ul v-for="(c, index) in card" :key="index" class="list-group list-group-horizontal row">
    <li class="list-group-item col"> {{ c.Card_ID }}</li>
    <li class="list-group-item col"> {{ c.Date_Of_Application }}</li>
    <li class="list-group-item col"> {{ c.Limit_Amount }}</li>
    <li class="list-group-item col"> {{ c.Payment_Date }}</li>
    <li class="list-group-item col"> {{ c.Card_Type }}</li>
    <li class="list-group-item col"> {{ c.Customer_Resident_Registration_Number }}</li>
    <li class="list-group-item col"> {{ c.Deposit_Account_ID }}</li>
  </ul>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  name: 'CardPage',
  data() {
    return {

    }
  },

  computed: {
    ...mapState(["card"]),
  },

  methods: {
    ...mapActions(["sortCard"]),

    async sortCardFront(field, order) {
      const data = {field, order}
      await this.sortCard(data)
    }
  }
}
</script>