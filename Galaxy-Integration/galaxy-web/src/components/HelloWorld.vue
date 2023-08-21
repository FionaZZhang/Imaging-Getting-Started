<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <p>
      This page contains user-friendly workflows on some common image analyses using Galaxy.
      <br> Simply click the workflow that you would like to perform and upload images with the required format. <br>
    </p>

    <!-- Workflow Selection -->
    <div class="workflow-selection">
        <select v-model="selectedWorkflow">
            <option disabled value="">Please select a workflow</option>
            <option value="workflow1">Normalize Histogram</option>
            <option value="workflow2">Image Filtering</option>
            <option value="workflow3">Segmentation</option>
        </select>
        <button @click="executeWorkflow">Execute Workflow</button>
    </div>
    <br>
    <!-- Upload button -->
    <div>
      <input type="file" id="fileUpload" @change="handleFiles" accept="image/jpeg, image/png" style="display: none;">
      <label for="fileUpload" class="custom-file-upload">
        Click here to Upload Images
      </label>
    </div>

    <h3>References</h3>
    <ul>
      <li><a href="https://training.galaxyproject.org/training-material/topics/imaging/tutorials/imaging-introduction/tutorial.html" target="_blank" rel="noopener">galaxy-tutorial</a></li>
    </ul>
    <h3>Directories</h3>
    <ul>
      <li><a href="https://github.com/WEHI-ResearchComputing" target="_blank" rel="noopener">WEHI-Research-Computing</a></li>
      <li><a href="https://github.com/WEHI-ResearchComputing/Imaging-Getting-Started" target="_blank" rel="noopener">Imaging-Project</a></li>
      <li><a href="https://github.com/WEHI-ResearchComputing/Imaging-Getting-Started/wiki/Technical-Notes" target="_blank" rel="noopener">Technical-Notes</a></li>
      <li><a href="https://github.com/WEHI-ResearchComputing/Imaging-Getting-Started/wiki/High%E2%80%90level-Architecture" target="_blank" rel="noopener">Architecture</a></li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  data() {
    return {
      selectedWorkflow: '',
      uploadedFiles: null
    }
  },
  methods: {
    handleFiles(event) {
      this.uploadedFiles = event.target.files;
    },
    async executeWorkflow() {
      if (!this.selectedWorkflow || !this.uploadedFiles) {
        alert('Please select a workflow and upload files');
        return;
      }
      const formData = new FormData();
      for (let i = 0; i < this.uploadedFiles.length; i++) {
        formData.append('files', this.uploadedFiles[i]);
      }
      formData.append('workflow', this.selectedWorkflow);

      try {
        const response = await axios.post(`${process.env.VUE_APP_BACKEND_URL}/response`, formData);
        console.log(response.data);
        // handle successful response
      } catch (error) {
        console.error('Error uploading files:', error);
        // handle error response
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}

.custom-file-upload {
  padding: 6px 12px;
  cursor: pointer;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 4px;
  display: inline-block;
  transition: background-color 0.2s;
}

.custom-file-upload:hover {
  background-color: #0056b3;
}

.hello {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;  /* Use 100% viewport height to center vertically in the view */
    flex-direction: column; /* Stack children vertically */
}

.workflow-selection {
    display: flex;
    gap: 10px;
    align-items: center;
    margin-top: 20px; /* Add some spacing at the top to separate it from other content */
}

.workflow-selection select, .workflow-selection button {
    padding: 8px 12px;
    font-size: 16px;
}

.workflow-selection button {
    background-color: #007BFF;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s;
}

.workflow-selection button:hover {
    background-color: #0056b3;
}

</style>
