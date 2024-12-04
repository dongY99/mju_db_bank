<template>
  <div>
    <!-- Modal Trigger -->
    <button type="button" class="btn btn-primary" data-bs-toggle="modal" :data-bs-target="'#depositAccountModal'+index">
      예금 계좌 추가
    </button>

    <!-- Modal -->
    <div class="modal fade" :id="'depositAccountModal'+index" tabindex="-1" :aria-labelledby="'depositAccountModalLabel'+index"
      aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" :id="'depositAccountModalLabel'+index">예금 계좌 등록</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <!-- 계좌 종류 -->
            <div class="input-group mb-3">
              <span class="input-group-text">계좌 종류</span>
              <input v-model="depositAccount.Account_Type" type="text" class="form-control" placeholder="저축, 정기예금 등"
                :class="{ 'is-invalid': errors.Account_Type }" @input="validateForm" />
              <div v-if="errors.Account_Type" class="invalid-feedback">계좌 종류를 입력해주세요.</div>
            </div>

            <!-- 잔액 -->
            <div class="input-group mb-3">
              <span class="input-group-text">잔액</span>
              <input v-model="depositAccount.Balance" type="number" class="form-control" placeholder="잔액 (숫자)"
                :class="{ 'is-invalid': errors.Balance }" @input="validateForm" />
              <div v-if="errors.Balance" class="invalid-feedback">유효한 잔액을 입력해주세요.</div>
            </div>

            <!-- 카드 신청 여부 -->
            <div class="form-check mb-3">
              <input v-model="depositAccount.Card_Application_Status" class="form-check-input" type="checkbox"
                id="cardApplicationStatus" />
              <label class="form-check-label" for="cardApplicationStatus">카드 신청 여부</label>
            </div>

            <!-- 계좌 개설일 -->
            <div class="input-group mb-3">
              <span class="input-group-text">개설일</span>
              <input v-model="depositAccount.Data_Of_Opening" type="date" class="form-control"
                :class="{ 'is-invalid': errors.Data_Of_Opening }" @input="validateForm" />
              <div v-if="errors.Data_Of_Opening" class="invalid-feedback">유효한 개설일을 선택해주세요.</div>
            </div>
          </div>

          <!-- Modal Footer -->
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="resetForm">닫기</button>
            <button type="button" class="btn btn-primary" :disabled="hasErrors" data-bs-dismiss="modal"
              @click="addDepositAccount">
              완료
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: "DepositAccountForm",
  data() {
    return {
      depositAccount: {
        Deposit_Account_ID: Math.floor(Math.random() * 9000) + 1000,
        Account_Type: "",
        Balance: 0,
        Card_Application_Status: false,
        Data_Of_Opening: "",
        Customer_Resident_Registration_Number: this.customer.Resident_Registration_Number,
      },
      errors: {
        Account_Type: false,
        Balance: false,
        Data_Of_Opening: false,
      },
    };
  },

  computed: {
    hasErrors() {
      return Object.values(this.errors).some((error) => error);
    },
  },

  props: {
    customer: Object,
    index: Number,
  },

  methods: {
    ...mapActions(["postDepositAccount"]), // Vuex 액션 맵핑

    validateForm() {
      // 계좌 종류 검증
      this.errors.Account_Type = this.depositAccount.Account_Type.trim() === "";

      // 잔액 검증
      this.errors.Balance = isNaN(this.depositAccount.Balance) || this.depositAccount.Balance < 0;

      // 개설일 검증
      this.errors.Data_Of_Opening = this.depositAccount.Data_Of_Opening === "";
    },

    resetForm() {
      this.depositAccount = {
        Deposit_Account_ID: Math.floor(Math.random() * 9000) + 1000,
        Account_Type: "",
        Balance: 0,
        Card_Application_Status: false,
        Data_Of_Opening: "",
        Customer_Resident_Registration_Number: this.customer.Resident_Registration_Number,
      };
      this.errors = {
        Account_Type: false,
        Balance: false,
        Data_Of_Opening: false,
        Customer_Resident_Registration_Number: false,
      };
      document.activeElement.blur(); // 현재 포커스가 있는 요소에서 포커스 제거
    },

    async addDepositAccount() {
      try {
        if (this.hasErrors) {
          alert("입력된 정보를 확인해주세요.");
          return;
        }

        // POST 요청
        await this.postDepositAccount(this.depositAccount);

        alert("예금 계좌가 성공적으로 추가되었습니다.");
        this.resetForm();
      } catch (error) {
        console.error("Error adding deposit account:", error);
      }
    },
  },
};
</script>

<style>
.is-invalid {
  border-color: red;
}
</style>
