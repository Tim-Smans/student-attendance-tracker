<template>
  <div class="bg-white shadow overflow-hidden sm:rounded-lg mb-8">
    <div class="px-4 py-5 sm:px-6">
      <h3 class="text-lg leading-6 font-medium text-gray-900">Upload Excel File</h3>
      <p class="mt-1 max-w-2xl text-sm text-gray-500">
        Upload an Excel file to upload a classgroup and its students.
      </p>
    </div>
    <div class="border-t border-gray-200 px-4 py-5 sm:px-6">
      <div class="text-sm text-gray-600">
        <p class="mb-2">The Excel file needs to contain following columns:</p>
        <ul class="list-disc pl-5 space-y-1">
          <li>Klasgroup name</li>
          <li>Student ID</li>
          <li>First name</li>
          <li>Last name</li>
          <li>Email</li>
          <li>Degree Programme</li>
        </ul>
      </div>
    </div>
  </div>
</template>
