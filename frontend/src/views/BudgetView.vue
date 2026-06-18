<template>
  <section>
    <PageHeader eyebrow="Budget" title="采购预算看板" />

    <transition name="fade">
      <div v-if="toast.show" class="toast" :class="toast.type">
        <span class="toast-icon">{{ toast.type === 'success' ? '✓' : '!' }}</span>
        <span class="toast-message">{{ toast.message }}</span>
      </div>
    </transition>

    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>数据加载中...</p>
    </div>

    <div v-else-if="loadError" class="error-state">
      <p class="error-icon">!</p>
      <p class="error-title">数据加载失败</p>
      <p class="error-desc">{{ loadError }}</p>
      <button class="primary-btn" @click="loadData">重新加载</button>
    </div>

    <template v-else>
      <div class="metrics-grid">
        <article class="metric">
          <span>年度预算总额</span>
          <strong>¥{{ totalPlanned.toLocaleString() }}</strong>
        </article>
        <article class="metric">
          <span>已下单金额</span>
          <strong>¥{{ totalOrdered.toLocaleString() }}</strong>
        </article>
        <article class="metric">
          <span>超预算月份</span>
          <strong class="error-text">{{ overBudgetCount }}</strong>
        </article>
        <article class="metric">
          <span>整体执行率</span>
          <strong>{{ overallUsageRate }}%</strong>
        </article>
      </div>

      <div class="budget-chart">
        <div class="chart-header">
          <h2>月度预算执行概览</h2>
          <div class="chart-legend">
            <span class="legend-item"><i class="legend-dot planned"></i>预计支出</span>
            <span class="legend-item"><i class="legend-dot ordered"></i>已下单金额</span>
            <span class="legend-item"><i class="legend-dot over"></i>超预算</span>
          </div>
        </div>
        <div v-if="dashboard.length === 0" class="empty-state">
          <p>暂无预算数据</p>
        </div>
        <div v-else class="chart-body">
          <div
            v-for="item in dashboard"
            :key="item.month"
            class="chart-row"
            :class="{ 'over-budget': item.overBudget }"
          >
            <div class="row-label">{{ formatMonth(item.month) }}</div>
            <div class="row-bars">
              <div class="bar-line">
                <span class="bar-label">预计</span>
                <div class="bar-track">
                  <div
                    class="bar planned-bar"
                    :style="{ width: barWidth(item.plannedAmount) }"
                  ></div>
                </div>
                <span class="bar-value val-planned">¥{{ item.plannedAmount.toLocaleString() }}</span>
              </div>
              <div class="bar-line">
                <span class="bar-label">已下单</span>
                <div class="bar-track">
                  <div
                    class="bar ordered-bar"
                    :class="{ 'bar-over': item.overBudget }"
                    :style="{ width: barWidth(item.orderedAmount) }"
                  ></div>
                </div>
                <span class="bar-value" :class="{ 'error-text': item.overBudget }">
                  ¥{{ item.orderedAmount.toLocaleString() }}
                </span>
              </div>
            </div>
            <div class="row-status">
              <span v-if="item.overBudget" class="badge danger">
                超预算 +¥{{ item.overAmount.toLocaleString() }}
              </span>
              <span v-else class="badge success">
                {{ item.usageRate }}%
              </span>
            </div>
          </div>
        </div>
      </div>
    </template>

    <div class="content-grid">
      <section class="panel">
        <h2>超预算预警</h2>
        <DataTable :columns="warningColumns" :rows="overBudgetItems">
          <template #plannedAmount="{ row }">¥{{ row.plannedAmount.toLocaleString() }}</template>
          <template #orderedAmount="{ row }">
            <span class="error-text">¥{{ row.orderedAmount.toLocaleString() }}</span>
          </template>
          <template #overAmount="{ row }">
            <span class="error-text">+¥{{ row.overAmount.toLocaleString() }}</span>
          </template>
        </DataTable>
      </section>
      <section class="panel">
        <h2>预算明细</h2>
        <div class="budget-form-row">
          <select v-model="newBudget.month">
            <option disabled value="">选择月份</option>
            <option v-for="m in availableMonths" :key="m" :value="m">{{ formatMonth(m) }}</option>
          </select>
          <input v-model.number="newBudget.amount" type="number" min="0" placeholder="预算金额" />
          <button class="secondary-btn" @click="addBudget">添加预算</button>
        </div>
        <DataTable :columns="budgetColumns" :rows="budgets">
          <template #amount="{ row }">
            <input
              class="inline-edit"
              type="number"
              min="0"
              :value="row.amount"
              @change="updateBudget(row, $event.target.value)"
            />
          </template>
        </DataTable>
      </section>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'

import { budgetsApi } from '../api/budgets'
import DataTable from '../components/DataTable.vue'
import PageHeader from '../components/PageHeader.vue'

const dashboard = ref([])
const budgets = ref([])
const newBudget = reactive({ month: '', amount: 0 })
const loading = ref(false)
const loadError = ref('')
const toast = reactive({
  show: false,
  type: 'success',
  message: ''
})
let toastTimer = null

function showToast(type, message) {
  if (toastTimer) clearTimeout(toastTimer)
  toast.show = true
  toast.type = type
  toast.message = message
  toastTimer = setTimeout(() => {
    toast.show = false
  }, 3000)
}

const totalPlanned = computed(() =>
  dashboard.value.reduce((sum, item) => sum + item.plannedAmount, 0)
)
const totalOrdered = computed(() =>
  dashboard.value.reduce((sum, item) => sum + item.orderedAmount, 0)
)
const overBudgetCount = computed(() =>
  dashboard.value.filter((item) => item.overBudget).length
)
const overallUsageRate = computed(() => {
  if (totalPlanned.value === 0) return 0
  return Math.round((totalOrdered.value / totalPlanned.value) * 1000) / 10
})

const overBudgetItems = computed(() =>
  dashboard.value.filter((item) => item.overBudget)
)

const maxAmount = computed(() =>
  Math.max(...dashboard.value.map((item) => Math.max(item.plannedAmount, item.orderedAmount)), 1)
)

const warningColumns = [
  { key: 'month', label: '月份' },
  { key: 'plannedAmount', label: '预计支出' },
  { key: 'orderedAmount', label: '已下单金额' },
  { key: 'overAmount', label: '超出金额' }
]

const budgetColumns = [
  { key: 'month', label: '月份' },
  { key: 'amount', label: '预算金额(¥)' }
]

const existingMonths = computed(() => new Set(budgets.value.map((b) => b.month)))

const availableMonths = computed(() => {
  const months = []
  for (let y = 2026; y <= 2026; y++) {
    for (let m = 1; m <= 12; m++) {
      const key = `${y}-${String(m).padStart(2, '0')}`
      if (!existingMonths.value.has(key)) months.push(key)
    }
  }
  return months
})

function formatMonth(month) {
  if (!month) return ''
  const [y, m] = month.split('-')
  return `${y}年${parseInt(m)}月`
}

function barWidth(amount) {
  return Math.min((amount / maxAmount.value) * 100, 100) + '%'
}

async function addBudget() {
  if (!newBudget.month || !newBudget.amount) {
    showToast('error', '请选择月份并填写预算金额')
    return
  }
  try {
    await budgetsApi.create({ month: newBudget.month, amount: newBudget.amount })
    Object.assign(newBudget, { month: '', amount: 0 })
    await loadData()
    showToast('success', '预算添加成功')
  } catch (err) {
    showToast('error', '预算添加失败：' + (err.message || '请稍后重试'))
  }
}

async function updateBudget(row, value) {
  const amount = parseFloat(value)
  if (isNaN(amount) || amount < 0) {
    showToast('error', '请输入有效的预算金额')
    return
  }
  try {
    await budgetsApi.update(row.id, { amount })
    await loadData()
    showToast('success', '预算修改成功')
  } catch (err) {
    showToast('error', '预算修改失败：' + (err.message || '请稍后重试'))
  }
}

async function loadData() {
  loading.value = true
  loadError.value = ''
  try {
    const [dashboardRes, budgetsRes] = await Promise.all([
      budgetsApi.dashboard(),
      budgetsApi.list()
    ])
    dashboard.value = dashboardRes.data
    budgets.value = budgetsRes.data
  } catch (err) {
    loadError.value = err.message || '网络请求失败，请检查后端服务是否正常运行'
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
</script>
