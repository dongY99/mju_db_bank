<template>
  <div class="chart mt-5">
    <nav class="navbar navbar-expand-lg bg-body-tertiary content-head">
      <div class="container-fluid">
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav">
            <form class="d-flex" role="search">
              <input
                class="form-control me-2"
                type="search"
                placeholder="Search"
                aria-label="Search"
              />
              <button class="btn btn-outline-success" type="submit">
                Search
              </button>
            </form>
            <li class="nav-item dropdown">
              <a
                class="nav-link dropdown-toggle"
                href="#"
                role="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                Dropdown link
              </a>
              <ul class="dropdown-menu">
                <li><a class="dropdown-item" href="#">Action</a></li>
                <li><a class="dropdown-item" href="#">Another action</a></li>
                <li><a class="dropdown-item" href="#">Something else here</a></li>
              </ul>
            </li>
            
            <ModalDialog/>
          </ul>
        </div>
      </div>
    </nav>

    <ul v-for="(size, index) in sizes" :key="index" :class="'list-group list-group-horizontal-' + size">
      <li class="list-group-item" v-for="item in 3" :key="item">Item {{ item }}</li>
    </ul>
  </div>
</template>

<script>
import ModalDialog from './ModalDialog.vue';

export default {
  name: 'ChartComponent',
  data() {
    return {
      sizes: ['sm', 'md', 'lg', 'xl', 'xxl']
    };
  },

  components: {
    ModalDialog
  }
};
</script>