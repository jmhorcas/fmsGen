function validateMinMax(minInputId, maxInputId) {
    const minInput = document.getElementById(minInputId);
    const maxInput = document.getElementById(maxInputId);
  
    // Add event listeners to both input fields
    minInput.addEventListener('input', () => {
      if (parseFloat(maxInput.value) < parseFloat(minInput.value)) {
        maxInput.value = minInput.value;
      }
    });
  
    maxInput.addEventListener('input', () => {
      if (parseFloat(maxInput.value) < parseFloat(minInput.value)) {
        minInput.value = maxInput.value;
      }
    });
}
  
// Call the function with IDs of input fields
validateMinMax('MIN_NUM_FEATURES', 'MAX_NUM_FEATURES');
validateMinMax('MIN_NUM_CONSTRAINTS', 'MAX_NUM_CONSTRAINTS');
