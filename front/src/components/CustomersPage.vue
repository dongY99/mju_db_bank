<template>
  <div class="row">
    <ul class="nav nav-tabs">
      <li class="nav-item col">
        <a class="nav-link" aria-current="page">주민번호</a>
      </li>
      <li class="nav-item dropdown col">
        <a class="nav-link dropdown-toggle" data-bs-toggle="dropdown" role="button" aria-expanded="false">이름</a>
        <ul class="dropdown-menu">
          <li><a class="dropdown-item">오름차순</a></li>
          <li><a class="dropdown-item">내림차순</a></li>
        </ul>
      </li>
      <li class="nav-item dropdown col">
        <a class="nav-link dropdown-toggle" data-bs-toggle="dropdown" role="button" aria-expanded="false">주소</a>
        <ul class="dropdown-menu">
          <li><a class="dropdown-item">오름차순</a></li>
          <li><a class="dropdown-item">내림차순</a></li>
        </ul>
      </li>
      <li class="nav-item col">
        <a class="nav-link" aria-current="page">생년월일</a>
      </li>
      <li class="nav-item col">
        <a class="nav-link" aria-current="page">이메일</a>
      </li>
      <li class="nav-item col">
        <a class="nav-link" aria-current="page">전화번호</a>
      </li>
      <li class="nav-item col">
        <a class="nav-link" aria-current="page">직업</a>
      </li>
      <li class="col"></li>
    </ul>
  </div>
  <ul v-for="(customer, index) in customers" :key="index" class="list-group list-group-horizontal row">
    <li class="list-group-item col"> {{ customer.Resident_Registration_Number }}</li>
    <li class="list-group-item col"> {{ customer.Name }}</li>
    <li class="list-group-item col"> {{ customer.Address }}</li>
    <li class="list-group-item col"> {{ customer.Date_Of_Birth }}</li>
    <li class="list-group-item col"> {{ customer.Email }}</li>
    <li class="list-group-item col"> {{ customer.Phone_Number }}</li>
    <li class="list-group-item col"> {{ customer.Occupation }}</li>
    <DepositAccountForm :customer="customer" :index="index" class="col"/>
  </ul>
</template>

<script>
import { mapState } from "vuex";
import DepositAccountForm from "./DepositAccountForm.vue";

export default {
  name: 'CustomersPage',
  data() {
    return {

    }
  },
  components: {
    DepositAccountForm,
  },

  computed: {
    ...mapState(["customers"]),
  },
}
</script>