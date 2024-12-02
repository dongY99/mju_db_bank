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
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown"
                aria-expanded="false">
                Dropdown link
              </a>
              <ul class="dropdown-menu">
                <li><a class="dropdown-item" href="#">Action</a></li>
                <li><a class="dropdown-item" href="#">Another action</a></li>
                <li><a class="dropdown-item" href="#">Something else here</a></li>
              </ul>
            </li>

            <ModalDialog />
          </ul>
        </div>
      </div>
    </nav>
    <div style="margin-left: 10px;">
      <ul v-for="(customer, index) in customers" :key="index" class="list-group list-group-horizontal row">
        <li class="list-group-item col"> {{ customer.Resident_Registration_Number }}</li>
        <li class="list-group-item col"> {{ customer.Name }}</li>
        <li class="list-group-item col"> {{ customer.Address }}</li>
        <li class="list-group-item col"> {{ customer.Date_Of_Birth }}</li>
        <li class="list-group-item col"> {{ customer.Email }}</li>
        <li class="list-group-item col"> {{ customer.Phone_Number }}</li>
        <li class="list-group-item col"> {{ customer.Occupation }}</li>
      </ul>
    </div>
    <button @click="fetchData">데이터 가져오기</button>
  </div>
</template>

<script>
import ModalDialog from './ModalDialog.vue';
import { mapState } from "vuex";

export default {
  name: 'ChartComponent',
  data() {
    return {
      searchType: 0
    };
  },
  computed: {
    ...mapState(["customers"]),
  },

  components: {
    ModalDialog
  }
};
</script>