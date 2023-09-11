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
            <option value="workflow2">HDAB Counts</option>
            <option value="workflow3">Segmentation</option>
        </select>
        <button @click="executeWorkflow">Execute Workflow</button>
    </div>
    <br>
    <!-- Upload button -->
    <div>
      <input type="file" id="fileUpload" @change="handleFiles" accept="image/jpeg, image/png, image/tiff" style="display: none;">
      <label for="fileUpload" class="custom-file-upload">
        Click here to Upload Images
      </label>
    </div>
    <br>
    <!-- Display the image -->
    <div class="section-box">
      <h3 class="section-title">Output</h3>
      <div class="output-image-container">
        <h4 v-if="isLoading" class="loading-indicator">
          Loading...
        </h4>
        <div v-else-if="wf1convertedImageUrl" class="image-wrapper">
          <img :src="wf1convertedImageUrl" alt="Output Image" class="output-image">
        </div>
  <!--      <div v-else>-->
  <!--        No image available.-->
  <!--      </div>-->
        <!-- Display State Times -->
        <div v-if="wf1stateTimes && Object.keys(wf1stateTimes).length > 0">
          <h3>State Status</h3>
          <ul>
            <li v-for="(time, state) in wf1stateTimes" :key="state">
              {{ state }}: {{ time }} seconds<br>
            </li>
          </ul>
        </div>
        <div v-if="wf2Hcount !== null && wf2DABcount !== null">
          <p>Hcount: {{ wf2Hcount }}</p>
          <p>DABcount: {{ wf2DABcount }}</p>
        </div>
      </div>
    </div>

    <!-- view jobs -->
    <br>
    <button @click="viewJobs" class="view-jobs-button">View Jobs</button>
    <br>
    <div class="section-box jobs-box">
      <h3 class="section-title">Jobs</h3>
      <table v-if="displayJobs">
        <thead>
          <tr>
            <th>Job ID</th>
            <th>Partition</th>
            <th>Name</th>
            <th>User</th>
            <th>Status</th>
            <th>Memory</th>
            <th>Time</th>
            <th>Nodes</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="job in jobStatus" :key="job.job_id">
            <td>{{ job.job_id }}</td>
            <td>{{ job.partition }}</td>
            <td>{{ job.name }}</td>
            <td>{{ job.user }}</td>
            <td>{{ job.status }}</td>
            <td>{{ job.memory }}</td>
            <td>{{ job.time }}</td>
            <td>{{ job.nodes }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <h3>References</h3>
    <ul>
      <li><a href="https://training.galaxyproject.org/training-material/topics/imaging/tutorials/imaging-introduction/tutorial.html" target="_blank" rel="noopener">galaxy-tutorial</a></li>
      <li><a href="https://bioblend.readthedocs.io/en/latest/" target="_blank" rel="noopener">bioblend</a></li>

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
import Image from 'image-js';

export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  data() {
    return {
      selectedWorkflow: '',
      isLoading: false,
      uploadedFiles: null,
      wf1stateTimes: null,
      wf1imageUrl: null,
      wf1convertedImageUrl: null,
      wf2Hcount: null,
      wf2DABcount: null,
      jobStatus: [],
      displayJobs: false,
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
      this.isLoading = true;
      try {
        const response = await axios.post(`http://127.0.0.1:5000/response`, formData);
        this.isLoading = false;
        console.log(response.data);
        if (this.selectedWorkflow == 'workflow1') {
          this.wf1stateTimes = response.data.state_times;
          console.log(this.wf1stateTimes);
          this.wf1imageUrl = response.data.output_path;
          console.log(this.wf1imageUrl)
          const tiffImageData = await Image.load(this.wf1imageUrl);
          const pngImageData = await tiffImageData.toDataURL('image/png');
          this.wf1convertedImageUrl = pngImageData;
        }
        if (this.selectedWorkflow == 'workflow2') {
          this.wf2Hcount = response.data.Hcount;
          this.wf2DABcount = response.data.DABcount;
          console.log(this.wf2Hcount);
          console.log(this.wf2DABcount);
        }
      } catch (error) {
        console.error('Error uploading files:', error);
      }
    },
    async viewJobs() {
      await this.fetchJobStatus();
      this.displayJobs = true;
    },
    async fetchJobStatus() {
        try {
          const response = await axios.get('http://127.0.0.1:5000/squeue');
          this.jobStatus = response.data;
        } catch (error) {
          console.error('Error fetching job status:', error);
        }
      },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

html, body {
  height: 100%;
  margin: 0;
  padding: 0;
}

.section-box {
  background-color: #f0f0f0; /* Grey background color */
  padding: 20px; /* Adjust padding as needed */
  border-radius: 5px; /* Rounded corners */
  margin-bottom: 20px; /* Add spacing between sections */
  text-align: center; /* Center align text within the box */
  align-items: center;
  width: 50vw;
  height: 100vh;
}

/* Style for the section titles */
.section-title {
  margin-top: 0; /* Remove default top margin for h3 */
}

h3 {
  margin: 40px 0 0;
}

h4 {
  margin: 40px 0 0;
  text-align: center;
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
    height: 100%;
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

.view-jobs-button {
    background-color: #007BFF;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s;
    font-size: 16px
}

.view-jobs-button:hover {
    background-color: #0056b3;
}


.output-image-container {
  max-width: 100%; /* Set the maximum width to 100% of the parent container */
  overflow: auto; /* Add scrollbars if the image exceeds the container dimensions */
  text-align: center;
}

.image-wrapper {
  max-width: 100%; /* Ensure the image fits within its container */
  overflow: auto; /* Add scrollbars if the image exceeds the container dimensions */
}

.output-image {
  width: 100%; /* Ensure the image occupies the full width of its container */
  height: auto; /* Maintain the image's aspect ratio */
}

</style>
