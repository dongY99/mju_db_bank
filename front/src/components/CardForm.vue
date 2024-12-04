<template>
  <div>
    <!-- Modal Trigger -->
    <button type="button" class="btn btn-primary" data-bs-toggle="modal" :data-bs-target="'#cardModal' + index">
      카드 추가
    </button>

    <!-- Modal -->
    <div class="modal fade" :id="'cardModal' + index" tabindex="-1" :aria-labelledby="'cardModalLabel' + index"
      aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" :id="'cardModalLabel' + index">카드 등록</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <!-- 카드 신청일 -->
            <div class="input-group mb-3">
              <span class="input-group-text">신청일</span>
              <input v-model="card.Date_Of_Application" type="date" class="form-control"
                :class="{ 'is-invalid': errors.Date_Of_Application }" @input="validateForm" />
              <div v-if="errors.Date_Of_Application" class="invalid-feedback">신청일을 선택해주세요.</div>
            </div>

            <!-- 한도 금액 -->
            <div class="input-group mb-3">
              <span class="input-group-text">한도 금액</span>
              <input v-model="card.Limit_Amount" type="number" class="form-control" placeholder="한도 금액"
                :class="{ 'is-invalid': errors.Limit_Amount }" @input="validateForm" />
              <div v-if="errors.Limit_Amount" class="invalid-feedback">유효한 한도 금액을 입력해주세요.</div>
            </div>

            <!-- 결제일 -->
            <div class="input-group mb-3">
              <span class="input-group-text" id="basic-addon1">결제일</span>
              <select v-model="card.Payment_Date" class="form-select" :class="{ 'is-invalid': errors.Payment_Date }"
                @input="validateForm">
                <option v-for="day in 28" :key="day" :value="day">{{ day }}일</option>
              </select>
            </div>

            <!-- 카드 종류 -->
            <div class="input-group mb-3">
              <span class="input-group-text">카드 종류</span>
              <input v-model="card.Card_Type" type="text" class="form-control" placeholder="체크카드, 신용카드 등"
                :class="{ 'is-invalid': errors.Card_Type }" @input="validateForm" />
              <div v-if="errors.Card_Type" class="invalid-feedback">카드 종류를 입력해주세요.</div>
            </div>
          </div>

          <!-- Modal Footer -->
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="resetForm">닫기</button>
            <button type="button" class="btn btn-primary" :disabled="hasErrors" data-bs-dismiss="modal"
              @click="addCard">
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
  name: "CardForm",
  props: {
    deposit: Object,
    index: Number,
  },
  data() {
    return {
      card: {
        Card_ID: Math.floor(Math.random() * 9000) + 1000, // 임의 ID
        Date_Of_Application: "",
        Limit_Amount: 0,
        Payment_Date: "",
        Card_Type: "",
        Customer_Resident_Registration_Number: this.deposit.Customer_Resident_Registration_Number, // 고객 주민등록번호
        Deposit_Account_ID: this.deposit.Deposit_Account_ID,
      },
      errors: {
        Date_Of_Application: false,
        Limit_Amount: false,
        Payment_Date: false,
        Card_Type: false,
      },
    };
  },
  computed: {
    hasErrors() {
      return Object.values(this.errors).some((error) => error);
    },
  },
  methods: {
    ...mapActions(["postCard"]), // Vuex 액션 맵핑

    validateForm() {
      // 신청일 검증
      this.errors.Date_Of_Application = this.card.Date_Of_Application === "";

      // 한도 금액 검증
      this.errors.Limit_Amount = isNaN(this.card.Limit_Amount) || this.card.Limit_Amount <= 0;

      // 결제일 검증
      this.errors.Payment_Date = this.card.Payment_Date === "";

      // 카드 종류 검증
      this.errors.Card_Type = this.card.Card_Type.trim() === "";
    },

    resetForm() {
      this.card = {
        Card_ID: Math.floor(Math.random() * 9000) + 1000,
        Date_Of_Application: "",
        Limit_Amount: 0,
        Payment_Date: "",
        Card_Type: "",
        Customer_Resident_Registration_Number: this.deposit.Customer_Resident_Registration_Number, // 고객 주민등록번호
        Deposit_Account_ID: this.deposit.Deposit_Account_ID,
      };
      this.errors = {
        Date_Of_Application: false,
        Limit_Amount: false,
        Payment_Date: false,
        Card_Type: false,
      };
      document.activeElement.blur(); // 현재 포커스 제거
    },

    async addCard() {
      try {
        if (this.hasErrors) {
          alert("입력된 정보를 확인해주세요.");
          return;
        }

        // POST 요청
        await this.postCard(this.card);

        alert("카드가 성공적으로 추가되었습니다.");
        this.resetForm();
      } catch (error) {
        console.error("Error adding card:", error);
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
