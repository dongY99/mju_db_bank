import { createStore } from 'vuex'
import axios from 'axios'

const store = createStore({
  state() {
    return {
      customers: [],
      depositAccount: [],
      card: [],
      transactions: [],

      searchedCustomer: "",
      searchedDepositAccount: "",
      searchedCard: "",
      searchedTransaction: "",
    }
  },

  mutations: {
    setCustomers(state, customers) {
      state.customers = customers
    },
    addCustomer(state, customer) {
      state.customers.push(customer); // 새 고객 추가
    },

    setDepositAccount(state, depositAccount) {
      state.depositAccount = depositAccount
    },
    addDepositAccount(state, depositAccount) {
      state.depositAccount.push(depositAccount);
    },

    setCard(state, card) {
      state.card = card
    },
    addCard(state, card) {
      state.card.push(card);
    },

    setTransactions(state, transaction) {
      state.transactions = transaction
    },
    addTransactions(state, transaction) {
      state.transactions.push(transaction);
    },

    setsearchedCustomer(state, search) {
      state.searchedCustomer = search;
    },
    setsearchedDepositAccount(state, search) {
      state.searchedDepositAccount = search;
    },
    setsearchedCard(state, search) {
      state.searchedCard = search;
    },
    setsearchedTransaction(state, search) {
      state.searchedTransaction = search;
    },
  },

  actions: {
    async fetchCustomers({ commit }) {
      try {
        const response = await axios.get('/api/customers');

        commit('setCustomers', response.data);
        commit('setsearchedCustomer', "");
      } catch (error) {
        console.error('fetch customers fail: ', error);
      }
    },

    async fetchDepositAccount({ commit }) {
      try {
        const response = await axios.get('/api/deposit_account');

        commit('setDepositAccount', response.data);
        commit('setsearchedDepositAccount', "");
      } catch (error) {
        console.error('fetch depositAccount fail: ', error);
      }
    },

    async fetchCard({ commit }) {
      try {
        const response = await axios.get('/api/card');

        commit('setCard', response.data);
        commit('setsearchedCard', "");
      } catch (error) {
        console.error('fetch card fail: ', error);
      }
    },

    async fetchTransaction({ commit }) {
      try {
        const response = await axios.get('/api/transactions');

        commit('setTransactions', response.data);
        commit('setsearchedTransaction', "");
      } catch (error) {
        console.error('fetch transaction fail: ', error);
      }
    },

    async postCustomer({ commit, dispatch }, customer) {
      try {
        const response = await axios.post('/add_customer', customer);
        commit('addCustomer', response.data.customer); // Store에 새 고객 추가
        dispatch('fetchCustomers')

      } catch (error) {
        console.error('Error posting customer:', error);
        throw error; // Vue 컴포넌트에서 에러를 처리하도록 전달
      }
    },

    async postDepositAccount({ commit, dispatch }, depositAccount) {
      try {
        const response = await axios.post("/add_deposit_account", depositAccount);
        commit("addDepositAccount", response.data.deposit_account); // Vuex 상태 업데이트
        dispatch('fetchDepositAccount')
      } catch (error) {
        console.error("Error posting deposit account:", error);
        throw error;
      }
    },

    async postCard({ commit, dispatch }, card) {
      try {
        const response = await axios.post("/add_card", card);
        commit("addCard", response.data.card); // Vuex 상태 업데이트
        dispatch('fetchCard')
      } catch (error) {
        console.error("Error posting card:", error);
        throw error;
      }
    },

    async postTransactions({ commit, dispatch }, transactions) {
      try {
        const response = await axios.post("/add_transaction", transactions);
        commit("addTransactions", response.data.transaction); // Vuex 상태 업데이트
        dispatch('fetchTransaction');
      } catch (error) {
        console.error("Error posting transaction:", error);
        throw error;
      }
    },

    async searchCustomer({ commit }, resident_registration_number) {
      const response = await axios.get('/query/customer/pk', {
        params: { resident_registration_number: resident_registration_number } // 쿼리 파라미터
      });

      commit("setCustomers", response.data.customer);
      commit('setsearchedCustomer', resident_registration_number);
    },

    async searchDepositAccount({ commit }, deposit_account_id) {
      const response = await axios.get('/query/deposit_account/pk', {
        params: { deposit_account_id: deposit_account_id } // 쿼리 파라미터
      });

      commit("setDepositAccount", response.data.deposit_account)
      commit('setsearchedDepositAccount', deposit_account_id);
    },

    async searchCard({ commit }, card_id) {
      const response = await axios.get('/query/card/pk', {
        params: { card_id: card_id } // 쿼리 파라미터
      });

      commit("setCard", response.data.card)
      commit('setsearchedCard', card_id);
    },

    async searchTransaction({ commit }, deposit_account_id) {
      const response = await axios.get('/query/transaction', {
        params: { deposit_account_id: deposit_account_id } // 쿼리 파라미터
      });

      commit("setTransactions", response.data.transactions)
      commit('setsearchedTransaction', deposit_account_id);
    },

    async sortCustomer({ state, commit }, data) {
      const response = await axios.get('/query/customers/sorted', {
        params: { field: data.field, order: data.order, resident_registration_number: state.searchedCustomer }
      });

      commit("setCustomers", response.data.customers)
    },

    async sortDepositAccount({ state, commit }, data) {
      const response = await axios.get('/query/deposit_accounts/sorted', {
        params: { field: data.field, order: data.order, deposit_account_id: state.searchedDepositAccount }
      });

      commit("setDepositAccount", response.data.deposit_accounts)
    },

    async sortTransaction({ state, commit }, data) {
      const response = await axios.get('/query/transactions/sorted', {
        params: { field: data.field, order: data.order, deposit_account_id: state.searchedTransaction }
      });

      commit("setTransactions", response.data.transactions)
    },

    async sortCard({ state, commit }, data) {
      const response = await axios.get('/query/card/sorted', {
        params: { field: data.field, order: data.order, card_id: state.searchedCard }
      });

      commit("setCard", response.data.cards)
    },
  },

  getters: {
    allCustomers(state) {
      return state.customers;
    },
    allDepositAccount(state) {
      return state.depositAccount;
    },
    allCard(state) {
      return state.card;
    },
    alltransaction(state) {
      return state.transactions;
    },
  }
})

export default store