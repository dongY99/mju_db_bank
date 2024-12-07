<template>
  <div>

    <button type="button" class="btn btn-primary" data-bs-toggle="modal" :data-bs-target="'#exampleModal' + isUpdate" v-if="!isUpdate">
      회원 추가
    </button>
    <button type="button" class="btn btn-primary" data-bs-toggle="modal" :data-bs-target="'#exampleModal' + isUpdate" v-if="isUpdate">
      회원 수정
    </button>

    <div class="modal fade" :id="'exampleModal' + isUpdate" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" :id="'exampleModalLabel' + isUpdate">회원가입</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <!-- 이름 -->
            <div class="input-group mb-3">
              <span class="input-group-text" id="basic-addon1">이름</span>
              <input v-model="customer.Name" type="text" class="form-control" :class="{ 'is-invalid': errors.Name }"
                placeholder="김명지" @input="validateForm" />
              <div v-if="errors.Name" class="invalid-feedback">이름을 입력해주세요.</div>
            </div>

            <!-- 주민등록번호 -->
            <div class="input-group mb-3">
              <span class="input-group-text" id="basic-addon1">주민번호</span>
              <input v-model="Resident_Registration_Number_First" type="text" class="form-control"
                :class="{ 'is-invalid': errors.Resident_Registration_Number }" maxlength="6" placeholder="앞 6자리"
                @input="validateForm" />
              <span class="input-group-text">-</span>
              <input v-model="Resident_Registration_Number_Second" type="text" class="form-control"
                :class="{ 'is-invalid': errors.Resident_Registration_Number }" maxlength="7" placeholder="뒤 7자리"
                @input="validateForm" />
              <div v-if="errors.Resident_Registration_Number" class="invalid-feedback">
                유효한 주민등록번호를 입력해주세요.
              </div>
            </div>

            <!-- 생년월일 -->
            <div class="input-group mb-3">
              <span class="input-group-text" id="basic-addon1">생년월일</span>
              <select v-model="selectedYear" class="form-select" :class="{ 'is-invalid': errors.Date_Of_Birth }"
                @input="validateForm">
                <option v-for="year in years" :key="year" :value="year">{{ year }}년</option>
              </select>
              <select v-model="selectedMonth" class="form-select" :class="{ 'is-invalid': errors.Date_Of_Birth }"
                @input="validateForm">
                <option v-for="month in months" :key="month" :value="month">{{ month }}월</option>
              </select>
              <select v-model="selectedDay" class="form-select" :class="{ 'is-invalid': errors.Date_Of_Birth }"
                @input="validateForm">
                <option v-for="day in days" :key="day" :value="day">{{ day }}일</option>
              </select>
              <div v-if="errors.Date_Of_Birth" class="invalid-feedback">
                생년월일을 입력해주세요.
              </div>
            </div>

            <!-- 주소 -->
            <div class="input-group mb-3">
              <span class="input-group-text" id="basic-addon1">주소</span>
              <input v-model="customer.Address" type="text" class="form-control" placeholder="경기도 용인시 처인구 명지로 116" />
            </div>

            <!-- 이메일 -->
            <div class="input-group mb-3">
              <span class="input-group-text" id="basic-addon1">이메일</span>
              <input v-model="Email_First" type="text" class="form-control" placeholder="60182915" />
              <span class="input-group-text">@</span>
              <input v-model="Email_Second" type="text" class="form-control" placeholder="mju.ac.kr" />
            </div>

            <!-- 전화번호 -->
            <div class="input-group mb-3">
              <span class="input-group-text" id="basic-addon1">전화번호</span>
              <input v-model="Phone_First" type="text" class="form-control"
                :class="{ 'is-invalid': errors.Phone_Number }" maxlength="3" placeholder="010" @input="validateForm" />
              <span class="input-group-text">-</span>
              <input v-model="Phone_Middle" type="text" class="form-control" maxlength="4" placeholder="1234"
                @input="validateForm" />
              <span class="input-group-text">-</span>
              <input v-model="Phone_Last" type="text" class="form-control" maxlength="4" placeholder="5678"
                @input="validateForm" />
              <div v-if="errors.Phone_Number" class="invalid-feedback">유효한 전화번호를 입력해주세요.</div>
            </div>

            <!-- 직업 -->
            <div class="input-group mb-3">
              <span class="input-group-text" id="basic-addon1">직업</span>
              <input v-model="customer.Occupation" type="text" class="form-control" placeholder="학생"
                @input="validateForm" />
            </div>
          </div>

          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="resetData">
              닫기
            </button>
            <button type="button" class="btn btn-primary" data-bs-dismiss="modal" :disabled="hasErrors" @click="addCustomer">
              완료
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  name: 'CustomerForm',
  data() {
    return {
      selectedYear: null,
      selectedMonth: null,
      selectedDay: null,
      years: [],
      months: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
      days: [],

      Resident_Registration_Number_First: "",
      Resident_Registration_Number_Second: "",
      Phone_First: "",
      Phone_Middle: "",
      Phone_Last: "",
      Email_First: "",
      Email_Second: "",

      customer: {
        Resident_Registration_Number: '',
        Name: '',
        Address: '',
        Date_Of_Birth: '',
        Email: '',
        Phone_Number: '',
        Occupation: '',
      },

      errors: {
        Name: false,
        Resident_Registration_Number: false,
        Date_Of_Birth: false,
        Phone_Number: false,
      },
    }
  },
  created() {
    // 현재 연도부터 과거 100년까지의 연도 생성
    const currentYear = new Date().getFullYear();
    for (let i = currentYear; i >= currentYear - 100; i--) {
      this.years.push(i);
    }

    // 선택된 월에 따른 일수 동적으로 변경
    this.updateDays();
  },
  watch: {
    selectedMonth(newMonth) {
      this.updateDays(newMonth);
    }
  },
  props: {
    isUpdate: Boolean
  },


  computed: {
    hasErrors() {
      return Object.values(this.errors).some((error) => error);
    },
  },


  methods: {
    ...mapActions(['postCustomer', 'updateCustomer']),

    updateDays(month = this.selectedMonth) {
      const daysInMonth = new Date(this.selectedYear, month, 0).getDate();
      this.days = [];
      for (let i = 1; i <= daysInMonth; i++) {
        this.days.push(i);
      }
    },
    resetData() {
      this.selectedYear = null;
      this.selectedMonth = null;
      this.selectedDay = null;
      this.Resident_Registration_Number_First = "";
      this.Resident_Registration_Number_Second = "";
      this.Phone_First = "";
      this.Phone_Middle = "";
      this.Phone_Last = "";
      this.Email_First = "";
      this.Email_Second = "";

      this.customer = {
        Resident_Registration_Number: '',
        Name: '',
        Address: '',
        Date_Of_Birth: '',
        Email: '',
        Phone_Number: '',
        Occupation: '',
      };

      document.activeElement.blur(); // 현재 포커스 제거
    },
    validateForm() {
      // 이름 검증
      this.errors.Name = this.customer.Name.trim() === "";

      // 주민등록번호 검증
      const rrnRegex = /^[0-9]{6}$/;
      const rrnSecondRegex = /^[0-9]{7}$/;
      this.errors.Resident_Registration_Number =
        !rrnRegex.test(this.Resident_Registration_Number_First) ||
        !rrnSecondRegex.test(this.Resident_Registration_Number_Second);

      // 생년월일 검증
      if (this.selectedYear == null && this.selectedMonth == null && this.selectedDay == null) {
        this.errors.Date_Of_Birth = true;
      } else {
        this.errors.Date_Of_Birth = false;
      }

      // 전화번호 검증
      const phoneRegex = /^[0-9]+$/;
      this.errors.Phone_Number =
        !phoneRegex.test(this.Phone_First) ||
        !phoneRegex.test(this.Phone_Middle) ||
        !phoneRegex.test(this.Phone_Last);
    },

    async addCustomer() {
      try {
        if (this.hasErrors) {
          alert("입력된 정보를 확인해주세요.");
          return;
        }
        const selectedDate = new Date(this.selectedYear, this.selectedMonth - 1, this.selectedDay);

        this.customer.Resident_Registration_Number = this.Resident_Registration_Number_First + "-" + this.Resident_Registration_Number_Second;
        this.customer.Phone_Number = this.Phone_First + "-" + this.Phone_Middle + "-" + this.Phone_Last;
        this.customer.Email = this.Email_First + "@" + this.Email_Second;
        this.customer.Date_Of_Birth = selectedDate.toISOString().slice(0, 10);

        // Flask API로 POST 요청 보내기
        console.log(this.isUpdate)
        if (this.isUpdate) {
          await this.updateCustomer(this.customer);
        } else {
          await this.postCustomer(this.customer); // 백엔드에 POST 요청 및 Store 업데이트
        }
        
        // 입력 필드 초기화
        this.resetData();

        console.log("Customer Added:", this.customer);
        alert("회원 정보가 성공적으로 저장되었습니다!");
      } catch (error) {
        console.error('Error adding customer:', error);
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