<template>
  <div class="hello">
  <img alt="Vue logo" src="../assets/WEHI_logo.png">
  <h1>WEHI RCP Customised Platform</h1>
    <h1>{{ msg }}</h1>
    <p>
      This page contains user-friendly workflows on some common image analyses.
      <br> Simply click the workflow that you would like to perform and upload images with the required format. <br>
      <br> If you want to upload a job, please follow this format for the script. <br>
    </p>

    <!-- Workflow Selection -->
    <div class="workflow-selection">
        <select v-model="selectedWorkflow">
            <option disabled value="">Please select a workflow</option>
            <option value="workflow1">Normalize Histogram</option>
            <option value="workflow2">HDAB Counts</option>
            <option value="workflow3">[+ Customised job]</option>
        </select>
    </div>
    <br>

    <!-- Description for selected workflow -->
    <div>
        <p v-if="selectedWorkflow === 'workflow1'">Input must be images (jpeg, png, tiff). </p>
        <p v-if="selectedWorkflow === 'workflow2'">Input must be images (jpeg, png, tiff). </p>
        <p v-if="selectedWorkflow === 'workflow3'">
            <strong>Custom Python Script Instructions:</strong>
        </p>
<ol v-if="selectedWorkflow === 'workflow3'" class="custom-instructions">

<strong>File Format:</strong> Save your custom script as a <code>.py</code> file.
<br>
<strong>Main Function:</strong> Your script should include a main function with the following signature:

<pre class="code">
def main(input_data):
  # Your custom logic here
  return result
</pre>

<code>input_data:</code> This parameter should accept the input data required for your script's execution.
<br>
<code>result:</code> The main function should return the result of the computation in this format:

<pre class="code">
response_data = {
    "Image": encoded_image,  # Base64-encoded grayscale image
    "Data": computed_data if computed_data is not None else False  # Computed data, or False if no data is available
}
</pre>

<strong>Example Script:</strong> Here's a simple example script that you can use as a template:

<pre class="code">
def main(input_image):
    # Convert the input image to grayscale
    grayscale_image = convert_to_grayscale(input_image)

    # Encode the grayscale image as base64
    encoded_image = base64_encode_image(grayscale_image)

    # Prepare the response data
    response_data = {
        "image": encoded_image,
        "data": False
    }

    return response_data
</pre>
</ol>
</div>

    <!-- Upload button -->
    <div>
      <input type="file" id="fileUpload" @change="handleFiles" :accept="getAcceptAttribute" style="display: none;">
      <label for="fileUpload" class="custom-file-upload">
        Click here to upload file
      </label>
    </div>
    <br>

    <div v-if="selectedWorkflow === 'workflow3'" >
      <div>
        <input type="file" @change="handleCustomInput" style="display: none;">
        <label class="custom-file-upload">
          Click here to upload your data
        </label>
      </div>
    </div>
    <br>


    <!-- Job Scheduling -->
    <div class="section-box submit-job-box">
      <h3 class="section-title">Job Scheduling</h3>
      <label for="jobName">Job Name: </label>
      <input v-model="jobName" type="text" id="jobName" />
      <br>

      <label for="jobTime">Job Time: </label>
      <input v-model="jobTime" type="range" min="1" max="7" step="1" id="jobTime" list="timeList" />
      <span>{{ jobTime }} hours</span>
      <datalist id="timeList">
        <option>1</option>
        <option>2</option>
        <option>3</option>
        <option>4</option>
        <option>5</option>
        <option>6</option>
        <option>7</option>
      </datalist>

      <br>
      <label for="jobCPU">CPU Per Task: </label>
      <input v-model="jobCPU" type="range" min="1" max="3" step="1" id="jobCPU" list="cpuList" />
      <span>{{ jobCPU }}</span>
      <datalist id="cpuList">
        <option>1</option>
        <option>2</option>
        <option>3</option>
      </datalist>

      <br>
      <label for="jobNodes">Nodes: </label>
      <input v-model="jobNodes" type="range" min="1" max="3" step="1" id="jobNodes" list="nodeList" />
      <span>{{ jobNodes }}</span>
      <datalist id="nodeList">
        <option>1</option>
        <option>2</option>
        <option>3</option>
      </datalist>

      <br>
      <label for="jobP">Partition: </label>
      <div>
        <input type="radio" id="regular" v-model="jobP" value="regular">
        <label for="regular">Regular</label>

        <input type="radio" id="other" v-model="jobP" value="other">
        <label for="other">Other</label>
      </div>

      <label for="jobMem">Memory: </label>
      <input v-model="jobMem" type="range" min="1" max="7" step="1" id="jobMem" list="memList" />
      <span>{{ jobMem }} GB</span>
      <datalist id="memList">
        <option>1</option>
        <option>2</option>
        <option>3</option>
        <option>4</option>
        <option>5</option>
        <option>6</option>
        <option>7</option>
      </datalist>

      <br>
      <label for="jobGRE">GREs: </label>
      <input v-model="jobGre" type="range" min="0" max="3" step="1" id="jobGre" list="greList" />
      <span>{{ jobGre }}</span>
      <datalist id="greList">
        <option>0</option>
        <option>1</option>
        <option>2</option>
        <option>3</option>
      </datalist>
      <br>
    </div>
    <button @click="executeWorkflow" class="execute-button">Execute Workflow</button>
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
        <div v-else-if="resultImage" class="image-wrapper">
          <img :src="resultImage" alt="Output Image" class="output-image">
        </div>

        <div v-if="wf1stateTimes && Object.keys(wf1stateTimes).length > 0">
          <h3>State Status</h3>
          <ul>
            <li v-for="(time, state) in wf1stateTimes" :key="state">
              {{ state }}: {{ time }} seconds<br>
            </li>
          </ul>
        </div>
        <div v-if="resultData">
          <h3>Result Data</h3>
          {{resultData}}
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
      customInputs: null,
      wf1stateTimes: null,
      wf1imageUrl: null,
      wf1convertedImageUrl: null,
      wf2Hcount: null,
      wf2DABcount: null,
      jobStatus: [],
      displayJobs: false,
      resultImage: false,
      resultData: false,
      jobTime: 5,
      jobCPU: 1,
      jobNodes: 1,
      jobP: "regular",
      jobMem: 1,
      jobGre: 0,
      jobName: "my-job"
    }
  },
  computed: {
      getAcceptAttribute() {
          if (this.selectedWorkflow === 'workflow1') {
              return 'image/jpeg, image/png, image/tiff';
          } else if (this.selectedWorkflow === 'workflow2') {
              return 'image/jpeg, image/png, image/tiff';
          } else if (this.selectedWorkflow === 'workflow3') {
              return '.py'; // Adjust as needed
          }
          return '';
      },
  },
  methods: {
    handleFiles(event) {
      this.uploadedFiles = event.target.files;
    },
    handleCustomInput(event) {
      this.customInputs = event.target.files;
    },
    async executeWorkflow() {


      if (!this.selectedWorkflow || !this.uploadedFiles) {
        alert('Please select a workflow and upload files');
        return;
      }
      const formData = new FormData();
      const jobScript = `#!/bin/bash\n#SBATCH --job-name=${this.jobName}\n#SBATCH --time=0${this.jobTime}:00:00\n#SBATCH --ntasks=${this.jobNodes}\n#SBATCH --mem=${this.jobMem}G\n#SBATCH cpus-per-task=${this.jobCPU}\n`;
      formData.append('script', jobScript);

      for (let i = 0; i < this.uploadedFiles.length; i++) {
        formData.append('files', this.uploadedFiles[i]);
      }
      formData.append('workflow', this.selectedWorkflow);
      if (this.selectedWorkflow == 'workflow3' && this.customInputs) {
        for (let i = 0; i < this.customInputs.length; i++) {
          formData.append('inputs', this.customInputs);
        }
      } else {
        formData.append('inputs', 1);
      }
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
        if (this.selectedWorkflow == 'workflow3') {
          this.resultImage = response.data.image;
          this.resultData = response.data.data;
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
    flex-direction: column;
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

.view-jobs-button, .submit-job-button {
    background-color: #007BFF;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s;
    font-size: 16px
}

.view-jobs-button:hover, .submit-job-button:hover{
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

/* Example CSS for code formatting */
.code {
    background-color: #f4f4f4;
    padding: 10px;
    border: 1px solid #ddd;
    border-left: 3px solid #f36d33;
    color: #333;
    font-size: 12px;
    line-height: 1.4;
    overflow: scroll;
    text-align: left;
    width: 50vw;
}

.execute-button {
    background-color: #007BFF;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s;
    padding: 8px 12px;
    font-size: 16px;
}

.execute-button:hover {
    background-color: #0056b3;
}

</style>
