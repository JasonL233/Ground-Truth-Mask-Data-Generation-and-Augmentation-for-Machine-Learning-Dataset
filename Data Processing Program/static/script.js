document.addEventListener("DOMContentLoaded", () => {
    // Get references to the radio buttons and dynamic field
    const drawMaskRadio = document.getElementById('drawMask');
    const augmentationRadio = document.getElementById('augmentation');
    const bothRadio = document.getElementById('both');
    const dynamicField = document.getElementById('dynamic-fieldset');

    // Event listeners to update dynamic field when radio selection changes
    drawMaskRadio.addEventListener('change', updateDynamicField);
    augmentationRadio.addEventListener('change', updateDynamicField);
    bothRadio.addEventListener('change', updateDynamicField);

    // Reset button color and text on any input change
    dynamicField.addEventListener('input', (event) => {
        const target = event.target;
        if (target.tagName === 'INPUT') {
            const buttonId = target.closest('fieldset').querySelector('button')?.id;

            if (buttonId) {
                const button = document.getElementById(buttonId);
                button.classList.remove('success', 'error');
                button.style.backgroundColor = '#007BFF';
                button.textContent = 'Submit';
            }
        }
    })

    updateDynamicField();

    // Function to update the dynamic field based on radio selection
    function updateDynamicField() {
        dynamicField.innerHTML = ''; // Clear previous content

        if (drawMaskRadio.checked) {
            dynamicField.innerHTML = `
                <label for="drawMask-tarJsonFileInput">Upload JSON File for target masks:</label>
                <input type="file" id="drawMask-tarJsonFileInput" accept=".json" /><br><br>

                <label for="drawMask-totJsonFileInput">Upload JSON File for total masks:</label>
                <input type="file" id="drawMask-totJsonFileInput" accept=".json" /><br><br>

                <label for="drawMask-imgFolderInput">Enter path for image folder:</label>
                <input type="text" id="drawMask-imgFolderInput" /><br><br>

                <label for="drawMask-targetMaskFolderOutput">Enter path for saving target mask folder:</label>
                <input type="text" id="drawMask-targetMaskFolderOutput" /><br><br>

                <label for="drawMask-totalMaskFolderOutput">Enter path for saving total mask folder:</label>
                <input type="text" id="drawMask-totalMaskFolderOutput" /><br><br>

                <button id="submitDrawMask">Submit</button>
            `;
            document.getElementById('submitDrawMask').addEventListener('click', handleDrawMaskSubmit);
        } else if (augmentationRadio.checked) {
            dynamicField.innerHTML = `         
                    <label for="aug1-imgInput">Select image file:</label>
                    <input type="file" id="aug1-imgInput" multiple/><br><br>

                    <label for="aug1-targetMaskInput">Select target mask file:</label>
                    <input type="file" id="aug1-targetMaskInput" multiple/><br><br>

                    <label for="aug1-totalMaskInput">Select total mask file:</label>
                    <input type="file" id="aug1-totalMaskInput" multiple/><br><br>

                    <label for="aug1-imgFolderOutput">Enter path for saving image augmentations:</label>
                    <input type="text" id="aug1-imgFolderOutput" /><br><br>

                    <label for="aug1-targetMaskFolderOutput">Enter path for saving target mask augmentations:</label>
                    <input type="text" id="aug1-targetMaskFolderOutput" /><br><br>

                    <label for="aug1-totalMaskFolderOutput">Enter path for saving total mask augmentations:</label>
                    <input type="text" id="aug1-totalMaskFolderOutput" /><br><br>

                    <label for="aug1-numAugmentationsInput">Number of augmentations:</label>
                    <input type="number" id="aug1-numAugmentationsInput" min="0" /><br><br>

                    <button id="submitAugmentation">Submit</button>                
            `;
            document.getElementById('submitAugmentation').addEventListener('click', handleAugmentationSubmit);
        } else if (bothRadio.checked) {
            dynamicField.innerHTML = `
                <label for="both-tarJsonFileInput">Upload JSON file for target masks:</label>
                <input type="file" id="both-tarJsonFileInput" accept=".json" /><br><br>

                <label for="both-totJsonFileInput">Upload JSON file for total masks:</label>
                <input type="file" id="both-totJsonFileInput" accept=".json" /><br><br>

                <label for="both-imgFolderInput">Enter path for image folder:</label>
                <input type="text" id="both-imgFolderInput" /><br><br>

                <label for="both-targetMaskFolderOutput">Enter path for saving target mask folder:</label>
                <input type="text" id="both-targetMaskFolderOutput" /><br><br>

                <label for="both-totalMaskFolderOutput">Enter path for saving total mask folder:</label>
                <input type="text" id="both-totalMaskFolderOutput" /><br><br>

                <label for="both-numAugmentationsInput">Number of augmentations:</label>
                <input type="number" id="both-numAugmentationsInput" min="0" /><br><br>

                <button id="submitBoth">Submit</button>
            `;
            document.getElementById('submitBoth').addEventListener('click', handleBothSubmit);
        }
    }


    function handleDrawMaskSubmit() {
        const tarJsonFile = document.getElementById('drawMask-tarJsonFileInput').files[0];
        const totJsonFile = document.getElementById('drawMask-totJsonFileInput').files[0];
        const imgFolderPath = document.getElementById('drawMask-imgFolderInput').value;
        const targetMaskOutputFolderPath = document.getElementById('drawMask-targetMaskFolderOutput').value;
        const totalMaskOutputFolderPath = document.getElementById('drawMask-totalMaskFolderOutput').value;
        const submitButton = document.getElementById('submitDrawMask');

        if (tarJsonFile && totJsonFile && imgFolderPath && targetMaskOutputFolderPath && targetMaskOutputFolderPath) {
            const formData = new FormData();

            formData.append('tarJsonFile', tarJsonFile);
            formData.append('totJsonFile', totJsonFile);
            formData.append('imgFolderPath', imgFolderPath);
            formData.append('targetMaskOutputFolderPath', targetMaskOutputFolderPath);
            formData.append('totalMaskOutputFolderPath', totalMaskOutputFolderPath);

            fetch('/processDrawMask', {
                method: 'POST',
                body: formData
            })
            .then(response => response.text())
            .then(data => {
                console.log('Success:', data);
                submitButton.classList.add('success');
                submitButton.style.backgroundColor = 'rgb(40, 167, 69)';
                submitButton.textContent = 'Success!';
            })
            .catch(error => {
                console.error('Error:', error);
                submitButton.classList.add('error');
                submitButton.textContent = 'Error';
            });
        } 
        else {
            if (!tarJsonFile){
                alert("Please upload json file for target masks");
            }
            if (!totJsonFile){
                alert("Please upload json file for total masks");
            }
            if (!imgFolderPath){
                alert("Please enter Image folder path");
            }
            if (!targetMaskOutputFolderPath)
            {
                alert("Please enter target mask folder path");
            }
            if (!totalMaskOutputFolderPath)
            {
                alert("Please enter total mask folder path");
            }
        }
    }


    function handleAugmentationSubmit() {
        const imgFiles = document.getElementById('aug1-imgInput').files;
        const targetMaskFiles = document.getElementById('aug1-targetMaskInput').files;
        const totalMaskFiles = document.getElementById('aug1-totalMaskInput').files;
        const imgOutputFolderPath = document.getElementById('aug1-imgFolderOutput').value;
        const targetMaskOutputFolderPath = document.getElementById('aug1-targetMaskFolderOutput').value;
        const totalMaskOutputFolderPath = document.getElementById('aug1-totalMaskFolderOutput').value;
        const numAugmentations = document.getElementById('aug1-numAugmentationsInput').value;
        const submitButton = document.getElementById('submitAugmentation');

        if ((imgFiles.length == targetMaskFiles.length == totalMaskFiles.length) 
            && imgFiles.length > 0 
            && targetMaskFiles.length > 0 
            && totalMaskFiles.length > 0 
            && imgOutputFolderPath 
            && targetMaskOutputFolderPath 
            && totalMaskOutputFolderPath
            && numAugmentations) {
            const formData = new FormData();

            for (let i=0; i<imgFiles.length; i++) {
                formData.append('imgFiles', imgFiles[i])
                formData.append('targetMaskFiles', targetMaskFiles[i])
                formData.append('totalMaskFiles', totalMaskFiles[i])
            }

            formData.append('imgOutputFolderPath', imgOutputFolderPath);
            formData.append('targetMaskOutputFolderPath', targetMaskOutputFolderPath);
            formData.append('totalMaskOutputFolderPath', totalMaskOutputFolderPath);
            formData.append('numAugmentations', numAugmentations);

            fetch('/processAugmentation', {
                method: 'POST',
                body: formData
            })
            .then(response => response.text())
            .then(data => {
                console.log('Success:', data);
                submitButton.classList.add('success');
                submitButton.style.backgroundColor = 'rgb(40, 167, 69)';
                submitButton.textContent = 'Success!';
            })
            .catch(error => {
                console.error('Error:', error);
                submitButton.classList.add('error');
                submitButton.textContent = 'Error';
            });
        } 
        else {
            if (!imgFiles.length > 0){
                alert("Please upload image file");
            }
            if (!targetMaskFiles.length > 0){
                alert("Please upload target mask file");
            }
            if (!totalMaskFiles.length > 0){
                alert("Please upload total mask file")
            }
            if (imgFiles.length != targetMaskFiles.length || imgFiles.length != totalMaskFiles.length){
                alert("Please upload equal number of files for both image and mask")
            }
            if (!imgOutputFolderPath){
                alert("Please enter Image folder path");
            }
            if (!targetMaskOutputFolderPath){
                alert("Please enter target mask folder path");
            }
            if (!totalMaskOutputFolderPath){
                alert("please enter total mask folder path")
            }
            if (!numAugmentations){
                alert("Please entter the number for augmentations");
            }
        }
    }


    function handleBothSubmit() {
        const tarJsonFile = document.getElementById('both-tarJsonFileInput').files[0];
        const totJsonFile = document.getElementById('both-totJsonFileInput').files[0];
        const imgFolderPath = document.getElementById('both-imgFolderInput').value;
        const targetMaskOutputFolderPath = document.getElementById('both-targetMaskFolderOutput').value;
        const totalMaskOutputFolderPath = document.getElementById('both-totalMaskFolderOutput').value;
        const numAugmentations = document.getElementById('both-numAugmentationsInput').value;
        const submitButton = document.getElementById('submitBoth');

        if (tarJsonFile && totJsonFile && imgFolderPath && targetMaskOutputFolderPath && totalMaskOutputFolderPath && numAugmentations) {
            const formData = new FormData();
            formData.append('tarJsonFile', tarJsonFile);
            formData.append('totJsonFile', totJsonFile)
            formData.append('imgFolderPath', imgFolderPath);
            formData.append('targetMaskOutputFolderPath', targetMaskOutputFolderPath);
            formData.append('totalMaskOutputFolderPath', totalMaskOutputFolderPath);
            formData.append('numAugmentations', numAugmentations);

            fetch('/processBoth', {
                method: 'POST',
                body: formData
            })
            .then(response => response.text())
            .then(data => {
                console.log('Success:', data);
                submitButton.classList.add('success');
                submitButton.style.backgroundColor = 'rgb(40, 167, 69)';
                submitButton.textContent = 'Success!';
            })
            .catch(error => {
                console.error('Error:', error);
                submitButton.classList.add('error');
                submitButton.textContent = 'Error';
            });
        } 
        else {
            if (!tarJsonFile){
                alert("Please upload json file for target masks")
            }
            if (!tarJsonFile){
                alert("Please upload json file for total masks")
            }
            if (!imgFolderPath){
                alert("Please enter Image folder path")
            }
            if (!targetMaskOutputFolderPath){
                alert("Please enter target mask folder path")
            }
            if (!totalMaskOutputFolderPath){
                alert("Please enter total mask folder path")
            }
            if (!numAugmentations){
                alert("Please entter the number for augmentations")
            }
        }
    }
});
