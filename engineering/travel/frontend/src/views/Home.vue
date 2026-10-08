<template>
  <div class="home-container">
    <section class="hero" id="how-it-works">
      <p class="hero-eyebrow">AI TRAVEL STUDIO</p>
      <h1>出发之前，<span>先想象抵达。</span></h1>
      <p class="hero-subtitle">
        告诉我们时间、目的地和偏好。让行程保持清晰，也为偶遇留一点空白。
      </p>
      <div class="hero-points" aria-label="服务能力">
        <span><i></i>智能生成</span>
        <span><i></i>实时地图</span>
        <span><i></i>随时编辑</span>
      </div>
    </section>

    <a-card class="form-card" :bordered="false">
      <div class="form-intro">
        <span class="form-kicker">PLAN A JOURNEY</span>
        <div>
          <h2>从一段好奇开始。</h2>
          <p>填写必要信息，其余交给智能旅行助手。</p>
        </div>
      </div>

      <a-form :model="formData" layout="vertical" @finish="handleSubmit">
        <div class="form-section">
          <div class="section-header">
            <span class="section-index">01</span>
            <div>
              <span class="section-title">目的地与日期</span>
              <span class="section-description">选择你想出发的地方与时间。</span>
            </div>
          </div>

          <a-row :gutter="20">
            <a-col :span="8">
              <a-form-item name="city" :rules="[{ required: true, message: '请输入目的地城市' }]">
                <template #label><span class="form-label">目的地城市</span></template>
                <a-input v-model:value="formData.city" placeholder="例如：北京" size="large" class="custom-input">
                  <template #prefix><span class="input-symbol">⌖</span></template>
                </a-input>
              </a-form-item>
            </a-col>
            <a-col :span="6">
              <a-form-item name="start_date" :rules="[{ required: true, message: '请选择开始日期' }]">
                <template #label><span class="form-label">开始日期</span></template>
                <a-date-picker v-model:value="formData.start_date" style="width: 100%" size="large" class="custom-input" placeholder="选择日期" />
              </a-form-item>
            </a-col>
            <a-col :span="6">
              <a-form-item name="end_date" :rules="[{ required: true, message: '请选择结束日期' }]">
                <template #label><span class="form-label">结束日期</span></template>
                <a-date-picker v-model:value="formData.end_date" style="width: 100%" size="large" class="custom-input" placeholder="选择日期" />
              </a-form-item>
            </a-col>
            <a-col :span="4">
              <a-form-item>
                <template #label><span class="form-label">旅行天数</span></template>
                <div class="days-display-compact">
                  <span class="days-value">{{ formData.travel_days }}</span>
                  <span class="days-unit">天</span>
                </div>
              </a-form-item>
            </a-col>
          </a-row>
        </div>

        <div class="form-section">
          <div class="section-header">
            <span class="section-index">02</span>
            <div>
              <span class="section-title">旅行方式</span>
              <span class="section-description">用你的节奏，定义这一段旅程。</span>
            </div>
          </div>

          <a-row :gutter="20">
            <a-col :span="8">
              <a-form-item name="transportation">
                <template #label><span class="form-label">交通方式</span></template>
                <a-select v-model:value="formData.transportation" size="large" class="custom-select">
                  <a-select-option value="公共交通">公共交通</a-select-option>
                  <a-select-option value="自驾">自驾</a-select-option>
                  <a-select-option value="步行">步行</a-select-option>
                  <a-select-option value="混合">混合出行</a-select-option>
                </a-select>
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item name="accommodation">
                <template #label><span class="form-label">住宿偏好</span></template>
                <a-select v-model:value="formData.accommodation" size="large" class="custom-select">
                  <a-select-option value="经济型酒店">经济型酒店</a-select-option>
                  <a-select-option value="舒适型酒店">舒适型酒店</a-select-option>
                  <a-select-option value="豪华酒店">豪华酒店</a-select-option>
                  <a-select-option value="民宿">民宿</a-select-option>
                </a-select>
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item name="preferences">
                <template #label><span class="form-label">旅行偏好</span></template>
                <a-checkbox-group v-model:value="formData.preferences" class="custom-checkbox-group">
                  <a-checkbox value="历史文化" class="preference-tag">历史文化</a-checkbox>
                  <a-checkbox value="自然风光" class="preference-tag">自然风光</a-checkbox>
                  <a-checkbox value="美食" class="preference-tag">美食</a-checkbox>
                  <a-checkbox value="购物" class="preference-tag">购物</a-checkbox>
                  <a-checkbox value="艺术" class="preference-tag">艺术</a-checkbox>
                  <a-checkbox value="休闲" class="preference-tag">休闲</a-checkbox>
                </a-checkbox-group>
              </a-form-item>
            </a-col>
          </a-row>
        </div>

        <div class="form-section form-section-last">
          <div class="section-header">
            <span class="section-index">03</span>
            <div>
              <span class="section-title">还有什么想告诉我们？</span>
              <span class="section-description">例如无障碍需求、想看的日出或需要避开的食物。</span>
            </div>
          </div>
          <a-form-item name="free_text_input">
            <a-textarea v-model:value="formData.free_text_input" placeholder="写下你的旅行期待…" :rows="3" size="large" class="custom-textarea" />
          </a-form-item>
        </div>

        <a-form-item class="submit-row">
          <a-button type="primary" html-type="submit" @click="handleSubmit" :loading="loading" size="large" class="submit-button">
            <template v-if="!loading">生成旅行方案</template>
            <template v-else>正在为你安排旅程…</template>
          </a-button>
        </a-form-item>

        <a-form-item v-if="loading" class="progress-row">
          <div class="loading-container">
            <a-progress :percent="loadingProgress" status="active" stroke-color="#5b5b61" :stroke-width="6" :show-info="false" />
            <p class="loading-status">{{ loadingStatus }}</p>
          </div>
        </a-form-item>
      </a-form>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { generateTripPlan } from '@/services/api'
import type { TripFormData } from '@/types'
import type { Dayjs } from 'dayjs'

const router = useRouter()
const loading = ref(false)
const loadingProgress = ref(0)
const loadingStatus = ref('')

type TripFormState = Omit<TripFormData, 'start_date' | 'end_date'> & {
  start_date: Dayjs | null
  end_date: Dayjs | null
}

const formData = reactive<TripFormState>({
  city: '',
  start_date: null,
  end_date: null,
  travel_days: 1,
  transportation: '公共交通',
  accommodation: '经济型酒店',
  preferences: [],
  free_text_input: ''
})

watch([() => formData.start_date, () => formData.end_date], ([start, end]) => {
  if (start && end) {
    const days = end.diff(start, 'day') + 1
    if (days > 0 && days <= 30) {
      formData.travel_days = days
    } else if (days > 30) {
      message.warning('旅行天数不能超过30天')
      formData.end_date = null
    } else {
      message.warning('结束日期不能早于开始日期')
      formData.end_date = null
    }
  }
})

const handleSubmit = async () => {
  if (loading.value) return
  if (!formData.city.trim()) {
    message.error('请输入目的地城市')
    return
  }
  if (!formData.start_date || !formData.end_date) {
    message.error('请选择日期')
    return
  }

  loading.value = true
  loadingProgress.value = 0
  loadingStatus.value = '正在准备行程…'

  const progressInterval = setInterval(() => {
    if (loadingProgress.value < 90) {
      loadingProgress.value += 10
      if (loadingProgress.value <= 30) {
        loadingStatus.value = '正在寻找值得停留的地方…'
      } else if (loadingProgress.value <= 50) {
        loadingStatus.value = '正在查看目的地天气…'
      } else if (loadingProgress.value <= 70) {
        loadingStatus.value = '正在匹配住宿与动线…'
      } else {
        loadingStatus.value = '正在整理你的旅行方案…'
      }
    }
  }, 500)

  try {
    const requestData: TripFormData = {
      city: formData.city,
      start_date: formData.start_date.format('YYYY-MM-DD'),
      end_date: formData.end_date.format('YYYY-MM-DD'),
      travel_days: formData.travel_days,
      transportation: formData.transportation,
      accommodation: formData.accommodation,
      preferences: formData.preferences,
      free_text_input: formData.free_text_input
    }
    const response = await generateTripPlan(requestData)

    clearInterval(progressInterval)
    loadingProgress.value = 100
    loadingStatus.value = '旅行方案已准备好。'

    if (response.success && response.data) {
      sessionStorage.setItem('tripPlan', JSON.stringify(response.data))
      message.success('旅行计划生成成功')
      setTimeout(() => router.push('/result'), 500)
    } else {
      message.error(response.message || '生成失败')
    }
  } catch (error: any) {
    clearInterval(progressInterval)
    message.error(error.message || '生成旅行计划失败，请稍后重试')
  } finally {
    setTimeout(() => {
      loading.value = false
      loadingProgress.value = 0
      loadingStatus.value = ''
    }, 1000)
  }
}
</script>

<style scoped>
.home-container { min-height: calc(100vh - 96px); padding: 88px 24px 96px; background: radial-gradient(circle at 50% -20%, rgba(29, 29, 31, 0.12), transparent 37%), repeating-linear-gradient(0deg, rgba(29, 29, 31, 0.018) 0 1px, transparent 1px 4px), var(--canvas); }
.hero { max-width: 850px; margin: 0 auto 58px; text-align: center; }
.hero-eyebrow, .form-kicker { margin: 0 0 14px; color: var(--accent); font-size: 12px; font-weight: 700; letter-spacing: 0.14em; }
.hero h1 { max-width: 760px; margin: 0 auto; color: var(--ink); font-size: clamp(46px, 7vw, 78px); font-weight: 700; letter-spacing: -0.065em; line-height: 1.04; }
.hero h1 span { display: block; background: linear-gradient(110deg, #1d1d1f 0%, #626268 54%, #c7c7cc 100%); background-clip: text; -webkit-background-clip: text; color: transparent; }
.hero-subtitle { max-width: 590px; margin: 22px auto 0; color: var(--muted); font-size: 19px; line-height: 1.55; }
.hero-points { display: flex; justify-content: center; flex-wrap: wrap; gap: 18px; margin-top: 28px; color: #424245; font-size: 14px; }
.hero-points span { display: inline-flex; align-items: center; gap: 8px; }
.hero-points i { width: 7px; height: 7px; border-radius: 50%; background: #30d158; }
.form-card { max-width: 1120px; margin: 0 auto; overflow: hidden; border: 1px solid rgba(210, 210, 215, 0.84) !important; border-radius: 28px; background: rgba(255, 255, 255, 0.9) !important; box-shadow: 0 24px 65px rgba(0, 0, 0, 0.08); backdrop-filter: blur(22px); }
.form-card :deep(.ant-card-body) { padding: 0; }
.form-intro { display: flex; align-items: flex-start; gap: 24px; padding: 34px 40px 30px; border-bottom: 1px solid #e8e8ed; }
.form-kicker { min-width: 132px; padding-top: 7px; }
.form-intro h2 { margin: 0; color: var(--ink); font-size: 28px; letter-spacing: -0.04em; }
.form-intro p { margin: 7px 0 0; color: var(--muted); font-size: 15px; }
.form-card :deep(.ant-form) { padding: 0 40px 38px; }
.form-section { padding: 30px 0; border-bottom: 1px solid #e8e8ed; }
.form-section-last { border-bottom: 0; }
.section-header { display: flex; align-items: flex-start; gap: 16px; margin-bottom: 24px; }
.section-index { display: inline-flex; align-items: center; justify-content: center; width: 30px; height: 30px; border-radius: 50%; color: var(--accent); background: var(--accent-soft); font-size: 12px; font-weight: 700; }
.section-title, .section-description { display: block; }
.section-title { color: var(--ink); font-size: 20px; font-weight: 650; letter-spacing: -0.025em; }
.section-description { margin-top: 4px; color: var(--muted); font-size: 14px; }
.form-label { color: #424245; font-size: 14px; font-weight: 600; }
.input-symbol { padding-right: 3px; color: var(--accent); font-size: 20px; }
.custom-input :deep(.ant-input), .custom-input :deep(.ant-picker), .custom-select :deep(.ant-select-selector), .custom-textarea :deep(.ant-input) { min-height: 48px; border-radius: 14px !important; background: #fff !important; }
.custom-select :deep(.ant-select-selector) { display: flex; align-items: center; }
.custom-textarea :deep(.ant-input) { padding-top: 13px; resize: vertical; }
.days-display-compact { display: flex; align-items: baseline; justify-content: center; min-height: 48px; border: 1px solid #d2d2d7; border-radius: 14px; background: #f5f5f7; }
.days-value { color: var(--ink); font-size: 24px; font-weight: 700; letter-spacing: -0.04em; }
.days-unit { margin-left: 4px; color: var(--muted); font-size: 13px; }
.custom-checkbox-group { display: flex; flex-wrap: wrap; gap: 8px; }
.preference-tag { display: inline-flex; align-items: center; min-height: 38px; margin: 0 !important; padding: 0 13px; border: 1px solid #d2d2d7; border-radius: 999px; color: #424245; background: #fff; transition: all 180ms ease; }
.preference-tag:hover { border-color: var(--accent); color: var(--accent); }
.preference-tag:has(.ant-checkbox-checked) { border-color: var(--accent-line); color: var(--accent); background: var(--accent-soft); }
.preference-tag :deep(.ant-checkbox) { display: none; }
.submit-row { margin: 6px 0 0; }
.submit-button { width: 100%; height: 52px; font-size: 17px; font-weight: 600; }
.progress-row { margin: 20px 0 0; }
.loading-container { padding: 16px 18px; border: 1px solid #d6d6db; border-radius: 16px; background: #fafafd; }
.loading-status { margin: 10px 0 0; color: var(--accent); font-size: 14px; text-align: center; }

@media (max-width: 800px) {
  .home-container { padding: 60px 16px 72px; }
  .hero { margin-bottom: 38px; }
  .hero-subtitle { font-size: 17px; }
  .form-intro, .form-card :deep(.ant-form) { padding-left: 22px; padding-right: 22px; }
  .form-intro { flex-direction: column; gap: 8px; padding-top: 26px; padding-bottom: 24px; }
  .form-kicker { padding-top: 0; }
  .form-section :deep(.ant-col) { width: 100%; max-width: 100%; flex: 0 0 100%; }
}
</style>
