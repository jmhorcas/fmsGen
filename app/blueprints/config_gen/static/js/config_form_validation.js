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

function updatePercentage(percentageInputId, numInputId, referenceInputId) {
  const percentageInput = document.getElementById(percentageInputId);
  const numInput = document.getElementById(numInputId);
  const referenceInput = document.getElementById(referenceInputId);

  // Add event listeners to both input fields
  percentageInput.addEventListener('input', () => {
    var numPercentage = Math.round(parseInt(referenceInput.value) * (parseInt(percentageInput.value)/100));
    numInput.value = numPercentage;
  });

  // Add event listeners to both input fields
  numInput.addEventListener('input', () => {
    if (parseInt(numInput.value) > parseInt(referenceInput.value)) {
      numInput.value = referenceInput.value;
    }
    var percentageValue = Math.round(parseInt(numInput.value) / parseInt(referenceInput.value) * 100);
    percentageInput.value = percentageValue;
  });
}
  
// Call the function with IDs of input fields
validateMinMax('MIN_NUM_FEATURES', 'MAX_NUM_FEATURES');
validateMinMax('MIN_NUM_CONSTRAINTS', 'MAX_NUM_CONSTRAINTS');

updatePercentage('PERCENTAGE_ABSTRACT_FEATURES', 'NUM_ABSTRACT_FEATURES', 'MAX_NUM_FEATURES');
updatePercentage('PERCENTAGE_MANDATORY_FEATURES', 'NUM_MANDATORY_FEATURES', 'MAX_NUM_FEATURES');
updatePercentage('PERCENTAGE_OPTIONAL_FEATURES', 'NUM_OPTIONAL_FEATURES', 'MAX_NUM_FEATURES');


function enableDisableFields(triggerElementId, responseElementsIds, enable) {
  const triggerElement = document.getElementById(triggerElementId);

  triggerElement.addEventListener('change', () => {
    if (triggerElement.checked) {
      for (var id of responseElementsIds) {
        $("#"+id).prop("disabled", !enable);
      }
    } else {
      for (var id of responseElementsIds) {
        $("#"+id).prop("disabled", enable);
      }
    }
  });
}

var abtract_features_elements = ['PERCENTAGE_ABSTRACT_FEATURES', 'NUM_ABSTRACT_FEATURES', 'ROOT_ABSTRACT_FEATURE', 'INTERNAL_ABSTRACT_FEATURES', 'ABSTRACT_LEAF_FEATURES'];
enableDisableFields('ABSTRACT_FEATURES', ['PERCENTAGE_ABSTRACT_FEATURES', 'NUM_ABSTRACT_FEATURES', 'ROOT_ABSTRACT_FEATURE', 'INTERNAL_ABSTRACT_FEATURES', 'ABSTRACT_LEAF_FEATURES'], true);
enableDisableFields('RANDOM_MANDATORY_FEATURES', ['PERCENTAGE_MANDATORY_FEATURES', 'NUM_MANDATORY_FEATURES'], false);
enableDisableFields('RANDOM_OPTIONAL_FEATURES', ['PERCENTAGE_OPTIONAL_FEATURES', 'NUM_OPTIONAL_FEATURES'], false);


// function checkUncheckFields(triggerElementId, responseElementsIds) {
//   const triggerElement = document.getElementById(triggerElementId);

//   triggerElement.addEventListener('change', () => {
//     if (triggerElement.checked) {
//       for (var id of responseElementsIds) {
//         $("#"+id).prop("checked", true);
//       }
//     } else {
//       for (var id of responseElementsIds) {
//         $("#"+id).prop("checked", false);
//       }
//     }
//   });
// }


// enableDisableFields('RELAXED_FMS', ['ABSTRACT_FEATURES']);