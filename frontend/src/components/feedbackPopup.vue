<template>
  <div>
    <div>
      <b-button v-b-modal.modal-1>Trigger Feedback</b-button>
      <p>*The response is displayed in console</p>

      <b-modal id="modal-1" title="BootstrapVue" hide-footer>
        <form @submit.prevent="sendFeedback"> 
          <div class="mb-2">
            <b-form-rating v-model="formData.rating" id="rating"></b-form-rating>
            <!-- Rating component for user to select a rating value -->
          </div>
          <div> 
            <b-input-group prepend="Description" class="mb-2">
              <b-form-input aria-label="Description (optional)" v-model="formData.description" id="description"></b-form-input>
              <!-- Input field for user to provide optional feedback description -->
            </b-input-group>
          </div>
          <b-button variant="secondary" @click="$bvModal.hide('modal-1')" class="mr-2">Close</b-button>
          <!-- Button to close the modal -->
          <b-button variant="primary" type="submit" class="ml-2">Send Feedback</b-button>
          <!-- Button to submit the feedback form -->
        </form>
        <template #modal-footer>
        </template>
      </b-modal>
    </div>
  </div>
</template>

<script>
import axios from 'axios' // Import Axios library for making HTTP requests
export default {
  name: 'feedbackPopup',
  data() {
    return {
      formData: {
        rating: "", // Initialize rating value to an empty string
        description: "", // Initialize description value to an empty string
      },
    };
  },
  methods: {
    sendFeedback() {
      // Send feedback data to the API using Axios
      axios.post('http://127.0.0.1:8000/feedback', this.formData)
        .then(response => {
          console.log(response); // Log the API response to the console
        })
        .catch(error => {
          console.log(error); // Log any errors that occur during the API request
        });
      this.$bvModal.hide('modal-1'); // Close the modal after sending feedback
    },
  },
};
</script>

<style lang="scss" scoped>

</style>
