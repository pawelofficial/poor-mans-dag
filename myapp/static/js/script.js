document.addEventListener('DOMContentLoaded', (event) => {
    let selectedColor = document.getElementById('colorPicker').value;  // Default color from color picker
    document.getElementById('colorPicker').addEventListener('input', (event) => {
        selectedColor = event.target.value;  // Update color from color picker
    });
    document.querySelectorAll('.colorButton').forEach((button) => {
        button.addEventListener('click', (event) => {
            selectedColor = event.target.value;  // Update color from button
        });
    });
    document.querySelectorAll('span').forEach((element) => {
        element.addEventListener('click', (event) => {
            event.target.style.color = selectedColor;
            const clickedString = event.target.innerText;
            fetch('/process_click', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ clicked_string: clickedString }),
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                // Check which option is selected
                const highlightOption = document.querySelector('input[name="highlightOption"]:checked').value;
                // Highlight the appropriate elements
                let elementsToHighlight = [];
                if (highlightOption === 'parents') {
                    elementsToHighlight = data.clicked_parents;
                } else if (highlightOption === 'descendants') {
                    elementsToHighlight = data.clicked_descendants;
                } else if (highlightOption === 'both') {
                    elementsToHighlight = [...data.clicked_parents, ...data.clicked_descendants];
                }
                elementsToHighlight.forEach(element => {
                    document.querySelectorAll('span').forEach((span) => {
                        if (span.innerText.includes(element)) {
                            span.style.color = selectedColor;
                        }
                    });
                });
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        });
    });
});