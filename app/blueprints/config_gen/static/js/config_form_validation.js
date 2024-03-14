/**
 * Validate that min and max are correct.
 * 
 * @param {*} minInputId 
 * @param {*} maxInputId 
 */
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

/**
 * Validate that the percentage and the num are coherent based on a given reference.
 * 
 * @param {*} percentageInputId 
 * @param {*} numInputId 
 * @param {*} referenceInputId 
 */
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
updatePercentage('PERCENTAGE_OR_GROUPS', 'NUM_OR_GROUPS', 'MAX_NUM_FEATURES');
updatePercentage('PERCENTAGE_XOR_GROUPS', 'NUM_XOR_GROUPS', 'MAX_NUM_FEATURES');

/**
 * Enable/Disable the response elements based on the trigger element. 
 * 
 * @param {*} triggerElementId 
 * @param {*} responseElementsIds 
 * @param {*} enable 
 * @param {*} defaultValue 
 */
function enableDisableFields(triggerElementId, responseElementsIds, enable, defaultValue) {
  const triggerElement = document.getElementById(triggerElementId);

  triggerElement.addEventListener('change', () => {
    if (triggerElement.checked) {
      for (var id of responseElementsIds) {
        $("#"+id).prop("disabled", !enable);
        if (!enable) {
          $("#"+id).attr("value", '');
        } else {
          $("#"+id).attr("value", defaultValue);
        }
      }
    } else {
      for (var id of responseElementsIds) {
        $("#"+id).prop("disabled", enable);
        if (enable) {
          $("#"+id).attr("value", '');
        } else {
          $("#"+id).attr("value", defaultValue);
        }
      }
    }
  });
}

var abtract_features_elements = ['PERCENTAGE_ABSTRACT_FEATURES', 'NUM_ABSTRACT_FEATURES', 'ROOT_ABSTRACT_FEATURE', 'INTERNAL_ABSTRACT_FEATURES', 'ABSTRACT_LEAF_FEATURES'];
enableDisableFields('ABSTRACT_FEATURES', ['PERCENTAGE_ABSTRACT_FEATURES', 'NUM_ABSTRACT_FEATURES', 'ROOT_ABSTRACT_FEATURE', 'INTERNAL_ABSTRACT_FEATURES', 'ABSTRACT_LEAF_FEATURES'], true, 0);
enableDisableFields('RANDOM_MANDATORY_FEATURES', ['PERCENTAGE_MANDATORY_FEATURES', 'NUM_MANDATORY_FEATURES'], false, 0);
enableDisableFields('RANDOM_OPTIONAL_FEATURES', ['PERCENTAGE_OPTIONAL_FEATURES', 'NUM_OPTIONAL_FEATURES'], false, 0);
enableDisableFields('RANDOM_OR_GROUPS', ['PERCENTAGE_OR_GROUPS', 'NUM_OR_GROUPS'], false, 0);
enableDisableFields('RANDOM_XOR_GROUPS', ['PERCENTAGE_XOR_GROUPS', 'NUM_XOR_GROUPS'], false, 0);

/**
 * Guarante all percentages do not exceeded max.
 * 
 * @param {*} mainFieldID 
 * @param {*} otherFieldsIds 
 */
function allPercentagesSumUpMax(mainFieldID, otherFieldsIds, referenceField, max) {
  const field = document.getElementById(mainFieldID);
  field.addEventListener('input', () => {
    var percentage = parseInt(field.value);
    var total = 0;
    for (var otherId of otherFieldsIds) {
      var otherField = document.getElementById(otherId);
      if (!otherField.disabled) {
        total += parseInt(otherField.value);
      }
    }
    var limit = max;
    if (limit == null) {
      limit = document.getElementById(referenceField).value;
    }
    if ((total + percentage) > limit) {
      field.value = limit - total;
    }
  });
}

allPercentagesSumUpMax('PERCENTAGE_MANDATORY_FEATURES', ['PERCENTAGE_OPTIONAL_FEATURES', 'PERCENTAGE_OR_GROUPS', 'PERCENTAGE_XOR_GROUPS'], null, 100);
allPercentagesSumUpMax('PERCENTAGE_OPTIONAL_FEATURES', ['PERCENTAGE_MANDATORY_FEATURES', 'PERCENTAGE_OR_GROUPS', 'PERCENTAGE_XOR_GROUPS'], null, 100);
allPercentagesSumUpMax('PERCENTAGE_OR_GROUPS', ['PERCENTAGE_MANDATORY_FEATURES', 'PERCENTAGE_OPTIONAL_FEATURES', 'PERCENTAGE_XOR_GROUPS'], null, 100);
allPercentagesSumUpMax('PERCENTAGE_XOR_GROUPS', ['PERCENTAGE_MANDATORY_FEATURES', 'PERCENTAGE_OPTIONAL_FEATURES', 'PERCENTAGE_OR_GROUPS'], null, 100);

allPercentagesSumUpMax('NUM_MANDATORY_FEATURES', ['NUM_OPTIONAL_FEATURES', 'NUM_OR_GROUPS', 'NUM_XOR_GROUPS'], 'MAX_NUM_FEATURES', null);
allPercentagesSumUpMax('NUM_OPTIONAL_FEATURES', ['NUM_MANDATORY_FEATURES', 'NUM_OR_GROUPS', 'NUM_XOR_GROUPS'], 'MAX_NUM_FEATURES', null);
allPercentagesSumUpMax('NUM_OR_GROUPS', ['NUM_MANDATORY_GROUPS', 'NUM_OPTIONAL_GROUPS', 'NUM_XOR_GROUPS'], 'MAX_NUM_FEATURES', null);
allPercentagesSumUpMax('NUM_XOR_GROUPS', ['NUM_MANDATORY_GROUPS', 'NUM_OPTIONAL_GROUPS', 'NUM_OR_GROUPS'], 'MAX_NUM_FEATURES', null);
