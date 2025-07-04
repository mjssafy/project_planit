<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <h3>{{ title }}</h3>
      <div v-if="title === '비밀번호 변경'" class="form-group">
        <input v-model="currentPassword" type="password" placeholder="현재 비밀번호" />
        <input v-model="newPassword" type="password" placeholder="새 비밀번호" />
        <input v-model="confirmPassword" type="password" placeholder="새 비밀번호 확인" />
        <button @click="changePassword">비밀번호 변경</button>
      </div>
      <div v-if="title === '내 소비 데이터 다운로드'" class="form-group">
        <p>소비 데이터를 다운로드하시겠습니까?</p>
        <div class="button-group">
          <button @click="$emit('close')">취소</button>
          <button @click="downloadData">다운로드</button>
        </div>
      </div>
      <div v-if="title === '계정 탈퇴'" class="form-group">
        <p>정말로 탈퇴하시겠습니까?</p>
        <input v-model="deletePassword" type="password" placeholder="비밀번호를 입력하세요" />
        <div class="button-group">
          <button @click="$emit('close')">취소</button>
          <button @click="deleteAccount">탈퇴하기</button>
        </div>
      </div>
      <div v-if="title === '고정지출 항목 입력'" class="form-group">
        <p>고정지출 항목을 입력하세요.</p>
        <input v-model="fixedItem" placeholder="항목명" />
        <input v-model="fixedAmount" type="number" placeholder="금액" />
        <input v-model="fixedDate" type="number" placeholder="결제일 (1~31)" />
        <div class="button-group">
          <button @click="$emit('close')">취소</button>
          <button @click="saveFixedExpense">저장</button>
        </div>
      </div>
      <div v-if="title === '월 목표 지출액 설정'" class="form-group">
        <label for="monthly-budget">월 목표 지출액 설정:</label>
        <input id="monthly-budget" v-model="monthlyBudget" type="number" placeholder="금액 입력" />
        <div class="button-group">
          <button @click="$emit('close')">취소</button>
          <button @click="saveMonthlyBudget">저장</button>
        </div>
      </div>
      <div v-if="title === '소비 절감 목표 설정'" class="form-group">
        <p>소비 절감 목표를 선택하세요.</p>
        <label><input type="radio" v-model="savingGoal" value="예산에 맞게" /> 예산에 맞게</label>
        <label><input type="radio" v-model="savingGoal" value="조금 절약하기" /> 조금 절약하기</label>
        <label><input type="radio" v-model="savingGoal" value="많이 절약하기" /> 많이 절약하기</label>
        <div class="button-group">
          <button @click="$emit('close')">취소</button>
          <button @click="saveSavingGoal">저장</button>
        </div>
      </div>
      <br>
      <button @click="$emit('close')">닫기</button>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'

const emit = defineEmits(['close'])
const props = defineProps({
  title: String
})

const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')

const changePassword = async () => {
  if (!currentPassword.value || !newPassword.value || !confirmPassword.value) {
    alert('모든 항목을 입력해주세요.')
    return
  }
  if (newPassword.value !== confirmPassword.value) {
    alert('새 비밀번호가 일치하지 않습니다.')
    return
  }

  try {
    const response = await axios.post('/api/setting/password/change/', {
      old_password: currentPassword.value,
      new_password: newPassword.value,
    })

    alert(response.data.detail || '비밀번호가 성공적으로 변경되었습니다.')
    currentPassword.value = ''
    newPassword.value = ''
    confirmPassword.value = ''
  } catch (error) {
    console.log(error.response?.data)
    if (error.response?.data?.old_password) {
      alert(error.response.data.old_password[0])
    } else if (error.response?.data?.new_password) {
      alert(error.response.data.new_password[0])
    } else {
      alert('비밀번호 변경 중 오류가 발생했습니다.')
    }
  }
}

const downloadData = async () => {
  try {
    const response = await axios.get('/api/setting/download/expense-data/', {
      responseType: 'blob',  // ✅ 파일 다운로드를 위한 설정
      withCredentials: true
    })

    const blob = new Blob([response.data], { type: 'text/csv;charset=utf-8;' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url

    // 파일 이름 설정 (서버에서 받은 이름 있으면 그걸 쓰고, 없으면 기본)
    const disposition = response.headers['content-disposition']
    const filenameMatch = disposition && disposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/)
    const filename = filenameMatch ? decodeURIComponent(filenameMatch[1].replace(/['"]/g, '')) : '소비데이터.csv'

    link.setAttribute('download', filename)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)

    alert('소비 데이터가 다운로드되었습니다.')
  } catch (error) {
    console.error('❌ 소비 데이터 다운로드 실패:', error)
    alert('소비 데이터를 다운로드하는 데 실패했습니다.')
  }
}

const deletePassword = ref('')

const deleteAccount = () => {
  if (!deletePassword.value) {
    alert('비밀번호를 입력해주세요.')
    return
  }
  alert('계정 탈퇴 요청됨 (백엔드 연동 예정)')
}

const fixedItem = ref('')
const fixedAmount = ref('')
const fixedDate = ref('')

const saveFixedExpense = async () => {
  if (!fixedItem.value || !fixedAmount.value || !fixedDate.value) {
    alert('모든 항목을 입력해주세요.')
    return
  }

  try {
    const response = await axios.post('/api/setting/fixed-expenses/', {
      name: fixedItem.value,
      amount: fixedAmount.value,
      payment_day: fixedDate.value
    }, {
      withCredentials: true
    })

    alert('고정지출 항목이 저장되었습니다.')

    // 입력값 초기화
    fixedItem.value = ''
    fixedAmount.value = ''
    fixedDate.value = ''

    // 닫기
    // $emit 사용 시 외부에서 <SettingsItemModal @close="..." /> 으로 닫기 처리 필요
    // emit('close') 직접 호출하려면 setup 상단에 defineEmits 사용 필요
  } catch (error) {
    console.error('고정지출 저장 실패:', error)
    alert('고정지출 항목 저장에 실패했습니다.')
  }
}


const monthlyBudget = ref('')

const saveMonthlyBudget = async () => {
  if (!monthlyBudget.value) {
    alert('금액을 입력해주세요.')
    return
  }

  const now = new Date()
  const year = now.getFullYear()
  const month = now.getMonth() + 1

  try {
    const response = await axios.post('/api/setting/budget/', {
      year,
      month,
      budget: Number(monthlyBudget.value)
    }, {
      withCredentials: true
    })

    alert('월 목표 지출액이 저장되었습니다.')
    emit('close')
  } catch (error) {
    console.error('월 목표 지출 저장 실패:', error)
    alert('월 목표 지출액 저장에 실패했습니다.')
  }
}

onMounted(async () => {
  if (props.title === '월 목표 지출액 설정') {  // ✅ 텍스트 일치 필요
    const now = new Date()
    const year = now.getFullYear()
    const month = now.getMonth() + 1

    try {
      const response = await axios.get(`/api/setting/budget/?year=${year}&month=${month}`, {
        withCredentials: true
      })
      monthlyBudget.value = response.data.budget
    } catch (error) {
      console.warn('월 목표 지출 예산이 아직 설정되지 않았습니다.')
      monthlyBudget.value = ''
    }
  }
})


const savingGoal = ref('')

const saveSavingGoal = () => {
  if (!savingGoal.value) {
    alert('목표를 선택해주세요.')
    return
  }
  alert(`소비 절감 목표 저장됨: ${savingGoal.value} (백엔드 연동 예정)`)
}
</script>

<style>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.modal-content {
  background: var(--bg-color);
  color: var(--text-color);
  padding: 2rem;
  border-radius: 12px;
  min-width: 400px;
  max-width: 90vw;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  z-index: 10000;
}

.modal-content h3 {
  color: var(--text-color);
}

.button-group {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

body.dark .modal-overlay {
  background: rgba(0, 0, 0, 0.8) !important;
}

body.dark .modal-overlay .modal-content {
  background-color: #2c2c2c !important;
  color: var(--text-color) !important;
}
</style>
