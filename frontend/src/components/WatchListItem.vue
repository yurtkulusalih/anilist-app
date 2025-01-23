<script setup lang="ts">
interface IProps {
  item: {
    id: number
    title: string
    averageScore: number
    coverImage: string
  }
}

const props = defineProps<IProps>()
</script>
<template>
  <li :key="props.item.id" class="flex items-center space-x-4 border-b pb-2">
    <!-- Picture -->
    <img
      :src="props.item.coverImage"
      alt="Anime Picture"
      class="w-16 h-16 object-cover rounded-md"
    />

    <!-- Details -->
    <div>
      <h3 class="text-lg font-bold text-gray-800">{{ props.item.title }}</h3>
      <p class="text-sm text-gray-600">
        Score: <span class="text-blue-500">{{ props.item.averageScore }}</span>
      </p>
    </div>
  </li>
</template>
