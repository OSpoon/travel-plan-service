<template>
  <div class="container">
    <el-card class="travel-planner">
      <template #header>
        <div class="card-header">
          <h2>旅行规划助手</h2>
        </div>
      </template>

      <el-form @submit.prevent="submitQuery">
        <el-form-item>
          <el-input v-model="query" type="textarea" :rows="3" placeholder="请描述您的旅行需求（例如：帮我规划一个为期3天的北京旅行计划）" />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitQuery" :loading="loading">
            {{ loading ? '规划中...' : '开始规划' }}
          </el-button>
        </el-form-item>
      </el-form>

      <div v-if="loading" class="loading-indicator">
        <el-skeleton :rows="10" animated />
      </div>

      <div v-else-if="travelContent" class="response-container">
        <div class="ai-message">
          <div class="markdown-content" v-html="renderedContent"></div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'
import { marked } from 'marked'
import { ElMessage } from 'element-plus'

const query = ref('')
const travelContent = ref('')
const loading = ref(false)
let abortController = null

// 组件卸载时清理
onUnmounted(() => {
  if (abortController) {
    abortController.abort()
  }
})

// 使用计算属性渲染Markdown
const renderedContent = computed(() => {
  return renderMarkdown(travelContent.value)
})

// Markdown渲染函数
const renderMarkdown = (content) => {
  if (!content) return '';

  marked.setOptions({
    gfm: true,
    breaks: true,
    tables: true
  })

  return marked(content);
}

// 提交查询
const submitQuery = async () => {
  if (!query.value.trim()) {
    ElMessage.warning('请输入您的旅行需求')
    return
  }

  // 取消之前的请求
  if (abortController) {
    abortController.abort()
  }

  // 创建新的 AbortController
  abortController = new AbortController()
  loading.value = true
  travelContent.value = ''

  try {
    const response = await fetch('/travel-plan/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query: query.value }),
      signal: abortController.signal
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()

    while (true) {
      const { value, done } = await reader.read()
      
      if (done) {
        loading.value = false
        break
      }

      const chunk = decoder.decode(value)
      const lines = chunk.split('\n').filter(line => line.trim())
      
      for (const line of lines) {
        try {
          const data = JSON.parse(line)
          if (data.content) {
            loading.value = false
            travelContent.value += data.content
          } else if (data.status === 'complete') {
            loading.value = false
            break
          } else if (data.error) {
            throw new Error(data.error)
          }
        } catch (e) {
          console.error('解析数据失败:', e)
        }
      }
    }
  } catch (error) {
    loading.value = false
    if (error.name === 'AbortError') {
      console.log('请求被取消')
    } else {
      console.error('请求出错:', error)
      ElMessage.error(`请求出错: ${error.message}`)
    }
  } finally {
    abortController = null
  }
}
</script>

<style scoped>
.container {
  max-width: 900px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.travel-planner {
  margin-bottom: 2rem;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.response-container {
  margin-top: 1.5rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  max-height: 70vh;
  overflow-y: auto;
}

.ai-message {
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.markdown-content {
  line-height: 1.6;
}

.markdown-content :deep(h1) {
  font-size: 1.8rem;
  margin: 1rem 0;
  color: #303133;
  border-bottom: 1px solid #ebeef5;
  padding-bottom: 0.5rem;
}

.markdown-content :deep(h2) {
  font-size: 1.5rem;
  margin: 1.2rem 0 0.8rem;
  color: #303133;
}

.markdown-content :deep(h3) {
  font-size: 1.3rem;
  margin: 1rem 0 0.6rem;
  color: #606266;
}

.markdown-content :deep(ul),
.markdown-content :deep(ol) {
  padding-left: 1.5rem;
  margin: 0.8rem 0;
}

.markdown-content :deep(li) {
  margin: 0.4rem 0;
}

.markdown-content :deep(p) {
  margin: 0.8rem 0;
}

.markdown-content :deep(table) {
  border-collapse: collapse;
  width: 100%;
  margin: 1rem 0;
}

.markdown-content :deep(th),
.markdown-content :deep(td) {
  border: 1px solid #dcdfe6;
  padding: 0.5rem;
  text-align: left;
}

.markdown-content :deep(th) {
  background-color: #f5f7fa;
}

.markdown-content :deep(hr) {
  margin: 1.5rem 0;
  border: none;
  border-top: 1px solid #ebeef5;
}

.loading-indicator {
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .container {
    padding: 0.5rem;
    margin: 1rem auto;
  }

  .ai-message {
    padding: 1rem;
  }

  .markdown-content :deep(table) {
    font-size: 0.9rem;
  }
}

.markdown-content :deep(strong) {
  font-weight: 600;
  color: #303133;
}

.markdown-content :deep(blockquote) {
  padding: 0.5rem 1rem;
  color: #6c757d;
  border-left: 4px solid #ebeef5;
  background-color: #f8f9fa;
  margin: 1rem 0;
}

.markdown-content :deep(code) {
  background-color: #f8f9fa;
  padding: 2px 6px;
  border-radius: 4px;
  color: #e83e8c;
  font-family: monospace;
}

.markdown-content :deep(table) {
  width: 100%;
  max-width: 100%;
  margin-bottom: 1rem;
  border-collapse: collapse;
  background-color: transparent;
}

.markdown-content :deep(table th),
.markdown-content :deep(table td) {
  padding: 0.5rem;
  border: 1px solid #dee2e6;
}

.markdown-content :deep(table thead th) {
  vertical-align: bottom;
  border-bottom: 2px solid #dee2e6;
  background-color: #f2f6fc;
}

.ai-message {
  animation: fadeIn 0.5s ease-in-out;
}
</style>