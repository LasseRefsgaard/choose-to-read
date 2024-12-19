<template>
  <div>
    <h1>Story Generator</h1>
    <div class="story-form">
      <input v-model="theme" placeholder="Enter a theme for your story...">
      <button @click="generateStory" :disabled="isLoading">
        {{ isLoading ? 'Generating...' : 'Generate Story' }}
      </button>
    </div>
    <div class="story-display" v-if="story">
      <h2 v-if="title">{{ title }}</h2>
      <p>{{ story }}</p>
      <p v-if="moral" class="moral"><em>Moral: {{ moral }}</em></p>
      <div class="story-actions" v-if="story">
        <input v-model="continuePrompt" placeholder="Continue the story...">
        <button @click="continueStory" :disabled="isLoading">Continue</button>
      </div>
      <div class="options" v-if="options.length">
        <h3>Choose an option:</h3>
        <div v-for="(option, index) in options" :key="index">
          <button @click="selectOption(option)">{{ option }}</button>
        </div>
      </div>
    </div>
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script>
const API_URL = 'http://localhost:8000';  // This should stay the same if your FastAPI is on port 8000

export default {
  name: 'App',
  data() {
    return {
      theme: '',
      story: '',
      title: '',
      moral: '',
      continuePrompt: '',
      isLoading: false,
      error: null,
      userId: 1,  // Hardcoded for now
      storyId: 1,  // Hardcoded for now
      options: []  // New data property for options
    }
  },
  methods: {
    async generateStory() {
      this.isLoading = true;
      this.error = null;
      this.options = [];  // Reset options on new story generation
      try {
        // First, get a new story ID
        const idResponse = await fetch(`${API_URL}/get_new_story_id/${this.userId}`, {
          method: 'GET',
          headers: {
            'Accept': 'application/json',
          }
        });
        if (!idResponse.ok) {
          throw new Error(`HTTP error! status: ${idResponse.status}`);
        }
        const idData = await idResponse.json();
        this.storyId = idData.story_id;

        // Then generate the story with the new ID
        const response = await fetch(`${API_URL}/generate_new_story`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          body: JSON.stringify({
            text: this.theme,
            user_id: this.userId,
            story_id: this.storyId
          })
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        if (typeof data.result === 'object') {
          this.title = data.result.title;
          this.story = data.result.story;
          this.moral = data.result.moral;
        } else {
          this.story = data.result;
        }

        // Call generate_three_options method
        const optionsResponse = await fetch(`${API_URL}/generate_three_options`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          body: JSON.stringify({
            text: this.theme,
            user_id: this.userId,
            story_id: this.storyId
          })
        });

        console.log("Option_responses:", this.optionsResponse);
        if (!optionsResponse.ok) {
          throw new Error(`HTTP error! status: ${optionsResponse.status}`);
        }
        
   
        const optionsData = await optionsResponse.json();

        console.log("optionsData:", optionsData);

        this.options = optionsData.result;  // Ensure this is an array of strings

        console.log("Options:", this.options);  // Debugging line to check the structure

      } catch (error) {
        this.error = 'Failed to generate story. Please try again.';
        console.error('Error:', error);
      } finally {
        this.isLoading = false;
      }
    },

    async continueStory() {
      if (!this.continuePrompt) return;

      this.isLoading = true;
      this.error = null;
      try {
        // Call the chat endpoint to continue the story
        const response = await fetch(`${API_URL}/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            text: this.continuePrompt,
            user_id: this.userId,
            story_id: this.storyId
          })
        });

        const data = await response.json();
        this.story = data.result;  // Update the story with the response
        this.continuePrompt = '';  // Clear the input after sending

        // Now call generate_three_options to get new options
        const optionsResponse = await fetch(`${API_URL}/generate_three_options`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          body: JSON.stringify({
            text: this.theme,  // You can use the same theme or modify as needed
            user_id: this.userId,
            story_id: this.storyId
          })
        });

        if (!optionsResponse.ok) {
          throw new Error(`HTTP error! status: ${optionsResponse.status}`);
        }

        const optionsData = await optionsResponse.json();
        console.log("Options received:", optionsData);

        // Ensure optionsData.result is an array of strings
        if (Array.isArray(optionsData.result)) {
          this.options = optionsData.result;  // Set the options
        } else {
          console.error("Expected an array of options, but got:", optionsData.result);
        }

      } catch (error) {
        this.error = 'Failed to continue story. Please try again.';
        console.error('Error:', error);
      } finally {
        this.isLoading = false;
      }
    },

    selectOption(option) {
      // Handle the selection of an option (you can implement your logic here)
      this.continuePrompt = option;  // For example, set the continuePrompt to the selected option
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin: 20px auto;
  max-width: 800px;
  padding: 0 20px;
}

.story-form {
  margin: 20px 0;
}

input {
  padding: 8px 12px;
  margin-right: 10px;
  width: 300px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  padding: 8px 16px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:disabled {
  background-color: #a8d5c2;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #3aa876;
}

.story-display {
  margin: 20px 0;
  padding: 20px;
  background-color: #f8f8f8;
  border-radius: 8px;
  text-align: left;
}

.story-actions {
  margin-top: 20px;
}

.error-message {
  color: #dc3545;
  margin: 10px 0;
  padding: 10px;
  background-color: #f8d7da;
  border-radius: 4px;
}
</style>
